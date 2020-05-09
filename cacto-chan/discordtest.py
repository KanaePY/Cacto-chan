import os
import discord
import discord.ext
import json
from discord.ext import commands


client = commands.Bot(command_prefix='.')


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


# Creating a leave channel for members
@client.command(aliases=['leavecreate', 'lc'])
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
        await channel.send(f"{member.mention} {leave_message}")


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
        await channel.send(f"{join_message} {member.mention}")




def readJson(filename="guild_data.json"):
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as file:
        data = json.load(file)
        file.close()
        return data


client.run('NzA0ODQ1MDU0ODE2MTU3ODA3.XqjEKQ.89GGn6d3lEIJdiPGfvdy6_1BCBw')
