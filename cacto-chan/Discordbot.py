# Remember to add Json to muterole command


# Imports

import os
import discord
import discord.ext
import json
import random
import sys, traceback
import asyncio
import asyncpg
from random import randint
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle


# Getting prefix function

def get_prefix(client, message):
    with open(os.path.join(os.path.dirname(__file__), "prefixes.json"), "r") as f:
        prefixes = json.load(f)
        f.close()

    return prefixes[str(message.guild.id)]


# Commands Prefix
client = commands.Bot(command_prefix=get_prefix)


# Writing default prefix for server

@client.event
async def on_guild_join(guild):
    with open(os.path.join(os.path.dirname(__file__), "prefixes.json"), "r") as f:
        prefixes = json.load(f)
        f.close()

    prefixes[str(guild.id)] = 'c!'

    with open(os.path.join(os.path.dirname(__file__), "prefixes.json"), "w") as f:
        json.dump(prefixes, f, indent=4)
        f.close()


# Removing useless data

@client.event
async def on_guild_remove(guild):
    with open(os.path.join(os.path.dirname(__file__), "prefixes.json",), "r") as f:
        prefixes = json.load(f)
        f.close()
    with open(os.path.join(os.path.dirname(__file__), "guild.data.json", ), "r") as e:
        join_message = json.load(e)
        f.close()
    with open(os.path.join(os.path.dirname(__file__), "guild.data2.json", ), "r") as i:
        leave_message = json.load(i)
        f.close()

    prefixes.pop(str(guild.id))
    join_message.pop(str(guild.id))
    leave_message.pop(str(guild.id))

    with open(os.path.join(os.path.dirname(__file__), "prefixes.json"), "w") as f:
        json.dump(prefixes, f, indent=4)
        f.close()
    with open(os.path.join(os.path.dirname(__file__), "guild_data.json"), "w") as e:
        json.dump(join_message, e, indent=4)
        f.close()
    with open(os.path.join(os.path.dirname(__file__), "guild_data2.json"), "w") as i:
        json.dump(leave_message, i, indent=4)
        f.close()


# Changing prefix command

@client.command()
@commands.has_permissions(manage_guild=True)
async def changeprefix(ctx, prefix):
    with open(os.path.join(os.path.dirname(__file__), "prefixes.json"), "r") as f:
        prefixes = json.load(f)
        f.close()

    prefixes[str(ctx.guild.id)] = prefix

    with open(os.path.join(os.path.dirname(__file__), "prefixes.json"), "w") as f:
        json.dump(prefixes, f, indent=4)
        f.close()
    await ctx.send(f'Prefix has been changes to {prefix}')


# Insufficient Permissions

@changeprefix.error
async def changeprefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, you are not allowed to use this command.')


# Creating a welcome channel for members

@client.command(aliases=['welcomecreate', 'wc'])
async def wcreate(ctx, *, msg, filename="guild_data.json"):
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as file:
        channelid = ctx.channel.id
        join_messages = json.load(file)
        print(channelid)
        file.close()

    join_messages[str(ctx.guild.id)] = {}
    join_messages[str(ctx.guild.id)]["channel_id"] = ctx.channel.id
    join_messages[str(ctx.guild.id)]["join_message"] = f"{msg}"

    with open(os.path.join(os.path.dirname(__file__), filename), "w") as file:
        json.dump(join_messages, file, indent=4)
        file.close()


# Insufficient permission

@wcreate.error
async def wcreate_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, you are not allowed to use this command.')

# Creating a leave channel for members

@client.command(aliases=['leavecreate', 'lc'])
@commands.has_permissions(manage_guild=True)
async def lcreate(ctx, *, msg, filename="guild_data2.json"):
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as file:
        channelid = ctx.channel.id
        leave_messages = json.load(file)
        print(channelid)
        file.close()

    leave_messages[str(ctx.guild.id)] = {}
    leave_messages[str(ctx.guild.id)]["channel_id"] = ctx.channel.id
    leave_messages[str(ctx.guild.id)]["leave_message"] = f"{msg}"

    with open(os.path.join(os.path.dirname(__file__), filename), "w") as file:
        json.dump(leave_messages, file, indent=4)
        file.close()


# Insufficient permission

@lcreate.error
async def lcreate_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, you are not allowed to use this command.')

# Leave event

@client.event
async def on_member_remove(member, filename="guild_data2.json"):
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as file:
        data = json.load(file)
        guildid = member.guild.id
        channelid = data[str(guildid)]["channel_id"]
        leave_message = data[str(guildid)]["leave_message"]
        print(f"{guildid} and {channelid} and {leave_message}")
        channel = client.get_channel(channelid)
        await channel.send(f"{member.mention} {leave_message}.")
        file.close()


# Join event

@client.event
async def on_member_join(member, filename="guild_data.json"):
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as file:
        data = json.load(file)
        guildid = member.guild.id
        channelid = data[str(guildid)]["channel_id"]
        join_message = data[str(guildid)]["join_message"]
        print(f"{guildid} and {channelid} and {join_message}")
        channel = client.get_channel(channelid)
        await channel.send(f"{join_message} {member.mention}!")
        file.close()


# Old status changing function

'''
    Status = cycle(['Status1', "Status2"])

    # Changing status loop
    @tasks.loop(seconds=3)
    async def change_status():
        activity = discord.Game(name=(next(Status)))
        await client.change_presence(activity=activity)
    '''


# Discord bot status and presence

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    activity = discord.Game(name="With Cactus")
    await client.change_presence(activity=activity)
    print('Online now!')

# Loading cogs

@client.command()
async def load(ctx, extension):
    if ctx.author.id == 238243351608950784:
        client.load_extension(f'cogs.{extension}')
    else:
        return


# Unloading cogs

@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 238243351608950784:
        client.unload_extension(f'cogs.{extension}')
    else:
        return

# Loading Cogs automatically on start up

initial_extensions = ["cogs.Moderation","cogs.Misc", "cogs.LevelSystemDB", "cogs.EconomySystemDB"]


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


# Creating a DataBase Pool Function

p = open("password.txt")

async def create_db_pool():
    client.pg_con = await asyncpg.create_pool(database="DiscordBot-DB", user="postgres", password=w.read())

# Looping the DataBase Pool Function

client.loop.run_until_complete(create_db_pool())


# Discord token

f = open("Discord Token.txt", "r")

client.run(f.read())
