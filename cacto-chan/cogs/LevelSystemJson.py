
# Imports

import discord
import os
import json
import asyncio
from discord.ext import commands


# Level System
class levels(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.client.loop.create_task(self.save_users())

        with open(os.path.join(os.path.dirname(__file__), "UserLevelsData.json"), "r") as f:
            self.users = json.load(f)

    @commands.Cog.listener()
    async def onready(self):
        print('Level System is now online')

    async def save_users(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            with open(os.path.join(os.path.dirname(__file__), "UserLevelsData.json"), "w") as f:
                json.dump(self.users, f, indent=4)

            await asyncio.sleep(5)

    def lvl_up(self, author_id):
        cur_exp = self.users[author_id]["Exp"]
        cur_lvl = self.users[author_id]["Level"]

        if cur_exp >= round((4 * (cur_lvl ** 3)) / 5):
            self.users[author_id]["Level"] += 1
            return True

        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.author.bot == True:
            return

        author_id = str(message.author.id)

        if author_id not in self.users:
            self.users[author_id] = {}
            self.users[author_id]["Level"] = 1
            self.users[author_id]["Exp"] = 0

        self.users[author_id]["Exp"] += 1

        if self.lvl_up(author_id):
            await message.channel.send(f"Congrats {message.author.mention}! You leveled up to {self.users[author_id]['Level']}")


    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)

        if member_id not in self.users:
            await ctx.send("You haven't talked enough to gain a level yet")

        else:
            cur_lvl = self.users[member_id]["Level"]
            cur_exp = self.users[member_id]["Exp"]
            total_exp = round((4 * (cur_lvl ** 3)) / 5)

            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

            embed.set_author(name=f"Level - {member}", icon_url=self.client.user.avatar_url)

            embed.add_field(name="Level", value=self.users[member_id]["Level"])
            embed.add_field(name="XP", value=(f"{cur_exp} / {total_exp}"))

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(levels(client))
