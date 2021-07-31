import discord
from discord.ext import commands
import json
from datetime import datetime
import os
import random

os.chdir(r'C:\Users\Anwender\PycharmProjects\Normalo-Bot')


class levels(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('users.json', 'r')as f:
            users = json.load(f)

        await self.update_data(users, member)

        with open('users.json', 'w')as f:
            json.dump(users, f)

    @commands.Cog.listener()
    async def on_message(self, message):
      if not message.author.bot:
        with open('users.json','r')as f:
            users = json.load(f)
        await self.update_data(users, message.author)
        if(users[str(message.author.id)]['LastMessage'] < await self.to_integer(datetime.now())):
            await self.add_experience(users, message.author)
        await self.level_up(users, message.author, message.channel)


        with open('users.json', 'w')as f:
            json.dump(users, f)

    async def update_data(self, users, user):
        if not str(user.id) in users:
            users[str(user.id)] = {}
            users[str(user.id)]['experience'] = 0
            users[str(user.id)]['level'] = 0
            users[str(user.id)]['LastMessage'] = await self.to_integer(datetime.now())

    async def add_experience(self, users, user):
        users[str(user.id)]['experience'] += random.randint(15,25)
        users[str(user.id)]['LastMessage'] = await self.to_integer(datetime.now())


    async def level_up(self, users, user,message):
        experience = users[str(user.id)]['experience']
        lvl = users[str(user.id)]['level']
        lvl_end = 5 * (lvl ** 2) + (50 * lvl) + 100
        print(user)
        print(f"Level:{lvl}")
        print(f"experience:{experience}")
        print(f"lvl_end: {lvl_end} ")



        if lvl_end <= experience:
            channel=self.client.get_channel(810855960133894154)
            await channel.send('{} has leveld up to level {}'.format(user.mention, lvl+1))
            users[str(user.id)]['level'] = lvl+1
            users[str(user.id)]['experience'] -= lvl_end



    async def to_integer(self, dt_time):
        answer = 100000000 * dt_time.year + 1000000 * dt_time.month + 10000 * dt_time.day + 100 * dt_time.hour + dt_time.minute
        return int(answer)

    @commands.command()
    async def rank(self,ctx, user: discord.Member = None):
        with open('users.json','r')as f:
            users = json.load(f)

        if user is None:
            if not str(ctx.author.id) in users:
                users[str(ctx.author.id)] = {}
                users[str(ctx.author.id)]['experience'] = 0
                users[str(ctx.author.id)]['level'] = 0
                users[str(ctx.author.id)]['LastMessage'] = await self.to_integer(datetime.now())
            user=ctx.author
            lvl = int(users[str(ctx.author.id)]['level'])
            exp = int(5 * (lvl ** 2) + (50 * lvl) + 100)
            embed = discord.Embed(Title=f"**{user}'s Rang**",Description=f"Experience: {lvl}/{5 * (lvl ** 2) + (50 * lvl) + 100}", color=0x0091ff)
            embed.set_thumbnail(url=f"{user.avatar_url}")
            embed.add_field(name=f"**{user}'s Rang**", value="💪  ", inline=False)
            embed.add_field(name="Level", value=f"**{users[str(user.id)]['level']}**", inline=True)
            embed.add_field(name="Experience", value=f"**{str(int(users[str(user.id)]['experience']))} / {exp}**",inline=True)
            embed.set_footer(text="Type more to level up!\nSpam is useless")
            await ctx.send(embed=embed)

        else:
            if not str(user.id) in users:
                users[str(user.id)] = {}
                users[str(user.id)]['experience'] = 0
                users[str(user.id)]['level'] = 0
                users[str(user.id)]['LastMessage'] = await self.to_integer(datetime.now())
            lvl = int(users[str(user.id)]['level'])
            exp=int(5 * (lvl ** 2) + (50 * lvl) + 100)
            embed=discord.Embed(Title=f"**{user}'s Rang**",Description=f"Experience: {lvl}/{5 * (lvl ** 2) + (50 * lvl) + 100}",color=0x0091ff)
            embed.set_thumbnail(url=f"{user.avatar_url}")
            embed.add_field(name=f"**{user}'s Rang**", value="💪  ", inline=False)
            embed.add_field(name="Level",value=f"**{users[str(user.id)]['level']}**",inline=True)
            embed.add_field(name="Experience", value=f"**{str(int(users[str(user.id)]['experience']))} / {exp}**", inline=True)
            embed.set_footer(text="Type more to level up!\nSpam is useless")
            await ctx.send(embed=embed)
                #await ctx.send(f"**{user}** hat das Level : {users[str(user.id)]['level']}. Es fehlen noch {(5 * (lvl ** 2) + (50 * lvl) + 100) - int(users[str(user.id)]['experience'])}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_exp(self, ctx, user: discord.Member,nummer:int):
        with open('users.json', 'r')as f:
            users = json.load(f)
        if not ctx.author.bot:
            users[str(user.id)]['experience']+=int(nummer)
            await ctx.send("exp added")
        with open('users.json', 'w')as f:
            json.dump(users, f)

    @commands.command()
    async def add_lvl(self, ctx, user: discord.Member,nummer:int):
        with open('users.json', 'r')as f:
            users = json.load(f)
        if not ctx.author.bot:
            users[str(user.id)]['level'] += int(nummer)
            await ctx.send("level added")
        with open('users.json', 'w')as f:
            json.dump(users, f)

    @commands.command()
    async def add_database(self,ctx, user: discord.Member):
        with open('users.json', 'r')as f:
            users = json.load(f)
        if not str(user.id) in users:
            users[str(user.id)] = {}
            users[str(user.id)]['experience'] = 0
            users[str(user.id)]['level'] = 0
            users[str(user.id)]['LastMessage'] = await self.to_integer(datetime.now())
            await ctx.send("added to database!")
        else:
            await ctx.send("already in database!")

        with open('users.json', 'w')as f:
            json.dump(users, f)


def setup(client):
    client.add_cog(levels(client))
