# Remember to add leveling system
# Remember to add economy and other misc commands
# Remember to better the insufficient permissions line


# Imports

import os
import discord
import discord.ext
import json
import random
from random import randint
#  from discord.ext import tasks
#  from itertools import cycle
from discord.ext import commands


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

    prefixes.pop(str(guild.id))

    with open(os.path.join(os.path.dirname(__file__), "prefixes.json"), "w") as f:
        json.dump(prefixes, f, indent=4)
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


# Removing useless data

@client.event
async def on_guild_remove(guild):
    with open(os.path.join(os.path.dirname(__file__), "guild.data.json", ), "r") as f:
        join_message = json.load(f)
        f.close()

    join_message.pop(str(guild.id))

    with open(os.path.join(os.path.dirname(__file__), "guild_data.json"), "w") as f:
        json.dump(join_message, f, indent=4)
        f.close()


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


# Removing useless data

@client.event
async def on_guild_remove(guild):
    with open(os.path.join(os.path.dirname(__file__), "guild.data2.json", ), "r") as f:
        leave_message = json.load(f)
        f.close()

    leave_message.pop(str(guild.id))

    with open(os.path.join(os.path.dirname(__file__), "guild_data2.json"), "w") as f:
        json.dump(leave_message, f, indent=4)
        f.close()


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


# Ping command

@client.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong! {round(client.latency * 1000)}ms :ping_pong: ')


# 8 Ball command

@client.command(aliases=['8ball', '8B'])
async def _8ball(ctx, *, question):
    responses = [f'It is certain...',
                 'It is decidedly so...',
                 'Without a doubt...',
                 'Yes - definitely...',
                 'You may rely on it...',
                 'As I see it, yes...',
                 'Most likely...',
                 'Outlook good...',
                 'Yes...',
                 'Signs point to yes...',
                 'Reply hazy, try again...',
                 'Ask again later...',
                 'Better not tell you now...',
                 'Cannot predict now...',
                 'Concentrate and ask again...',
                 'Do not count on it...',
                 'My reply is no...',
                 'My sources say no...',
                 'Outlook not so good...',
                 'Very doubtful...']
    await ctx.send(f':8ball: Question: {question} :8ball:\n:8ball: Answer: {random.choice(responses)} :8ball:') \



# Unban command

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *,  member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.name}#{user.discriminator} has been unbanned. ')
            return


# Insufficient permission

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, you are not allowed to use this command.')


# Kick command

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')


# Insufficient permission

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, you are not allowed to use this command.')


# Ban command

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


# Insufficient permission

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, you are not allowed to use this command.')


# Deleting messages command

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Cleared {amount} messages')


# Insufficient permission

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, you are not allowed to use this command.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the number of messages you want to clear.')


# Spotify Status Reader

@client.command()
@commands.guild_only()
async def spotify(ctx, user: discord.Member = None):
    user = user or ctx.author
    spot = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if spot is None:
        await ctx.send(f"{user.name} is not listening to Spotify")
        return
    embedspotify = discord.Embed(title=f"{user.name}'s Spotify", color=0x1eba10)
    embedspotify.add_field(name="Song", value=spot.title)
    embedspotify.add_field(name="Artist", value=spot.artist)
    embedspotify.add_field(name="Album", value=spot.album)
    embedspotify.set_thumbnail(url=spot.album_cover_url)
    await ctx.send(embed=embedspotify)


# Fake warn command

@client.command()
async def warn(ctx, reason: str, member: discord.Member = None):
    member = ctx.author if not member else member
    await ctx.send(f'/warn {member} {reason} ')


# PP command

@client.command()
async def pp(ctx, user: discord.Member = None):
    user = user or ctx.author
    print(user)

    if user.id == 238243351608950784:
        await ctx.send('8' + '=' * randint(5, 10) + 'D')

    elif user.id == 452474671712174091:
        await ctx.send('8' + '=' * randint(0, 5) + 'D')

    elif user.id == 576785017255100417:
        await ctx.send('8' + '=' * randint(0, 5) + 'D')

    elif user.id == 340879927647666176:
        await ctx.send('8D')
        await ctx.send("Soge is virus's waifu no boy")

    else:
        await ctx.send('8' + '=' * randint(0, 10) + 'D')


# User info command

@client.command()
async def userinfo(ctx, member: discord.Member = None):

    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild name:", value=member.display_name)

    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)

    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)


# Gay measuring command

@client.command()
async def howgay(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    if member.id == 452474671712174091:
        embed = discord.Embed(title=f"{member.name}'s Gayness", color=0xffc0cb)
        embed.add_field(name="How gay?", value=f":rainbow_flag: {member.name} is {randint(65,100)}% gay :rainbow_flag: ")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{member.name}'s Gayness", color=0xffc0cb)
        embed.add_field(name="How gay?", value=f":rainbow_flag: {member.name} is {randint(0, 100)}% gay :rainbow_flag: ")
        await ctx.send(embed=embed)

# Loading cogs

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


# Unloading cogs

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


# Finding cog file

for filename in os.listdir('./Discord bot/cogs'):
    if filename.endswith(f'.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# Discord token
client.run('Njk5MzkzMDM0NTM3OTI2NzEw.XpTw5Q.r-b2uk7ekySJ_bxLWgPZykBbASo')
