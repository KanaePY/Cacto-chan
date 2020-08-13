
# Imports

import discord
import os
import asyncio
import asyncpg
import random
from random import randint
from discord.ext import commands
from discord.ext.commands import BucketType, CooldownMapping


# Level System

class levels(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cooldown = CooldownMapping.from_cooldown(1, 35, BucketType.member)

    @commands.Cog.listener()
    async def onready(self):
        print('Level System is now online')

    async def lvl_up(self, user):
        cur_exp = user['exp']
        cur_lvl = user['lvl']
        
        user_2 = await self.client.pg_con.fetch("SELECT * FROM users2 WHERE user_id = $1", user['user_id'])
        cur_cacti = user_2[0]['cacti']
        
        if cur_exp >= round((4 * (cur_lvl ** 3)) / 5):
            await self.client.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 and guild_id = $3",
                                             cur_lvl + 1, user['user_id'], user['guild_id'])
            
            await self.client.pg_con.execute("UPDATE users2 SET cacti = $1 WHERE user_id = $2", cur_cacti + (500 * cur_lvl), user['user_id'])
            
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.author.bot == True:
            return

        bucket = self.cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after:
            # we're on cooldown, retry_after is the number of seconds left
            return

        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)

        if not user:
            await self.client.pg_con.execute(f"INSERT INTO users (user_id, guild_id, lvl, exp) VALUES ($1, $2, 1, 0)",
                                          author_id, guild_id)

        user = await self.client.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)

        await self.client.pg_con.execute("UPDATE users SET exp = $1 WHERE user_id = $2 and guild_id = $3", user['exp'] + 1,
                                      author_id, guild_id)

        if await self.lvl_up(user):
            await message.channel.send(f"Congrats {message.author.mention}! You leveled up to {user['lvl'] + 1}")


    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id,
                                           guild_id)

        cur_exp = user[0]['exp']
        cur_lvl = user[0]['lvl']

        if not user:
                await ctx.send(f"Member has not talked enough to gain a level yet.")

        else:
            total_exp = round((4 * (cur_lvl ** 3)) / 5)

            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

            embed.set_author(name=f"Level - {member}", icon_url=self.client.user.avatar_url)

            embed.add_field(name="Level", value=user[0]["lvl"])
            embed.add_field(name="XP", value=(f"{cur_exp} / {total_exp}"))

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(levels(client))
