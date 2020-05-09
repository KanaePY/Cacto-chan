import discord
from discord.ext import commands
import random
from random import randint


# Cogs
class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def onready(self):
        print('Cogs are now online')

    @commands.command()
    async def test(self, ctx):
        await ctx.send(f'ye this bot works!')


def setup(client):
    client.add_cog(Example(client))
