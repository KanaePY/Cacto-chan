
# Imports

import discord
import random
from random import randint
from discord.ext import commands


# Cog class for misc commands

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    # To tell cogs are online

    @commands.Cog.listener()
    async def onready(self):
        print('Cogs are now online')

    # Ping command

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f':ping_pong: Pong! {round(self.client.latency * 1000)}ms :ping_pong: ')
    
    # Gay measuring command

    @commands.command()
    async def howgay(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        if member.id == 452474671712174091:
            embed = discord.Embed(title=f"{member.name}'s Gayness", color=0xffc0cb)
            embed.add_field(name="How gay?",
                            value=f":rainbow_flag: {member.name} is {randint(45, 100)}% gay :rainbow_flag:")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"{member.name}'s Gayness", color=0xffc0cb)
            embed.add_field(name="How gay?",
                            value=f":rainbow_flag: {member.name} is {randint(0, 100)}% gay :rainbow_flag:")
            await ctx.send(embed=embed)

    # PP command

    @commands.command()
    async def pp(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        print(user)

        if user.id == 238243351608950784:
            await ctx.send('8' + '=' * randint(5, 10) + 'D')

        elif user.id == 452474671712174091:
            await ctx.send('8' + '=' * randint(0, 7) + 'D')

        elif user.id == 576785017255100417:
            await ctx.send('8' + '=' * randint(0, 7) + 'D')

        elif user.id == 340879927647666176:
            await ctx.send('8D')
            await ctx.send("Soge is virus's waifu no boy")

        else:
            await ctx.send('8' + '=' * randint(0, 10) + 'D')

    # Spotify Status Reader

    @commands.command()
    @commands.guild_only()
    async def spotify(self, ctx, user: discord.Member = None):
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

    # 8 Ball command

    @commands.command(aliases=['8ball', '8B'])
    async def _8ball(self, ctx, *, question):
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
        await ctx.send(f':8ball: Question: {question} :8ball:\n:8ball: Answer: {random.choice(responses)} :8ball:')

    # User info command

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):

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
    
    # Misc reaction event

    @commands.Cog.listener()
    async def on_message(self, message):
        if "nabeel is gay" in message.content.lower():
            await message.add_reaction(":gaynabeel:703282548423393320")

        elif "nabeel gay" in message.content.lower():
            await message.add_reaction(":gaynabeel:703282548423393320")

        elif "nabeel haram" in message.content.lower():
            await message.add_reaction(":gaynabeel:703282548423393320")

        elif "gay nabeel" in message.content.lower():
            await message.add_reaction(":gaynabeel:703282548423393320")


def setup(client):
    client.add_cog(Misc(client))
