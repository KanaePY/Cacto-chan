
# Imports

import discord
import os
import asyncio
import asyncpg
import random
from random import randint
from discord.ext import commands
from discord.ext.commands import BucketType, CooldownMapping

# Economy System

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def onready(self):
        print('Economy System is now online')

    
    # Not Needed
    '''
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == True:
            return
        if message.author == self.client.user:
            return
        author_id = str(message.author.id)
        user = await self.client.pg_con.fetch("SELECT * FROM users2 WHERE user_id = $1", author_id)    
    '''


    @commands.command(aliases=["cactus", "balance"])
    async def cacti(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)

        user = await self.client.pg_con.fetch("SELECT * FROM users2 WHERE user_id = $1", member_id,)

        cacti = user[0]['cacti']

        if not user:
            await ctx.send(f"You just set up your Cacti Wallet. You now have 1000 Cacti as a starting bonus.")
            await self.client.pg_con.execute(f"INSERT INTO users2 (user_id, cacti) VALUES($1, 1000)", member_id)

        if cacti == 0:
            await ctx.send(f"You have 0 cacti. You can type c!daily to get some")

        else:
            await ctx.send(f"You have {cacti} cacti. Currently you can't do anything with it.")

    @commands.command(aliases=['transfer'])
    async def give(self, ctx, member:discord.Member, amount: int):
        user1_id = str(ctx.author.id)
        print("here 1")
        print(f"{member.id}")
        print(type(amount))
        user2_id = str(member.id)

        user1 = await self.client.pg_con.fetch("SELECT * FROM users2 WHERE user_id = $1", user1_id)
        print(user1)
        cacti_1 = user1[0]['cacti']

        user2 = await self.client.pg_con.fetch("SELECT * FROM users2 WHERE user_id = $1", user2_id)
        print(user2)
        cacti_2 = user2[0]['cacti']

        if user1_id == user2_id:
            await ctx.send(f"You can't transfer money to yourself dummy!")
            return

        if not user2:
            await ctx.send(f"The person you tried to mention has not set his Cacti Wallet. yet. Type c!cacti to set up Cacti Wallet")

        if not user1:
            await ctx.send(f"You haven't set up your Cacti Wallet yet. Type c!cacti to set up Cacti Wallet")

        if cacti_1 < amount:
            await ctx.send(f"You have insufficient cacti")
            return

        else:
            await self.client.pg_con.execute("UPDATE users2 SET cacti = $1 WHERE user_id = $2", cacti_1 - amount,
                                             user1_id)

            await self.client.pg_con.execute("UPDATE users2 SET cacti = $1 WHERE user_id = $2", cacti_2 + amount,
                                             user2_id)


    @commands.command()
    @commands.cooldown(1, 86400, BucketType.member)
    async def daily(self, ctx):
        member_id = str(ctx.author.id)
        user = await self.client.pg_con.fetch("SELECT * FROM users2 WHERE user_id = $1", member_id)
        cacti = user[0]['cacti']
        daily_amount = 1500

        if not user:
            ctx.send(f"You haven't set up your Cacti Wallet yet! Type c!cacti to set up your Cacti Wallet.")
            return

        await self.client.pg_con.execute("UPDATE users2 SET cacti = $1 WHERE user_id = $2", cacti + daily_amount, member_id)
        await ctx.send("You just claimed 1500 <:cacti:737409831060897882> ! Use it Wisely. Come back after 24 hours to get more")
    
    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Wait %.1fh before you can use this command again" % (error.retry_after / 3600))

    
    @commands.command(aliases=["cf"])
    async def coinflip(self, ctx, amount: int = 100, side: str = "head"):
        member_id = str(ctx.author.id)
        user = await self.client.pg_con.fetch("SELECT * FROM users2 WHERE user_id = $1", member_id)
        cacti = user[0]['cacti']

        if not user:
            ctx.send(f"You haven't set up your Cacti Wallet yet! Type c!cacti to set up your Cacti Wallet.")
            return

        if cacti < amount:
            if cacti == 0:
                await ctx.send(f"You have 0 cacti. do c!daily to get some more cacti!")
                return

            else:
                await ctx.send(f"You have insufficient cacti.")
                return

        else:
            rolled = randint(1, 2)
            if rolled == 1:
                if "head" in side.lower():
                    win = True

                elif "tail" in side.lower():
                    win = False

                else:
                    await ctx.send(f"{side} is not valid! Either say heads or tails. The side is heads by default")
                    return

            if rolled == 2:
                if "head" in side.lower():
                    win = False

                elif "tail" in side.lower():
                    win = True

                else:
                    await ctx.send(f"{side} is not valid! Either say heads or tails. The side is heads by default")
                    return

            if win == True:
                await ctx.send(f"Congrats you won {amount * 2} cacti!")
                await self.client.pg_con.execute("UPDATE users2 SET cacti = $1 WHERE user_id = $2", cacti + amount, member_id)

            if win == False:
                await ctx.send(f"You lost {amount} cacti. Sowwy!")
                await self.client.pg_con.execute("UPDATE users2 SET cacti = $1 WHERE user_id = $2", cacti - amount, member_id)

def setup(client):
    client.add_cog(economy(client))