# Imports

import discord
import random
import asyncio
import json
import os
import sys, traceback
from itertools import cycle
from random import randint
from discord.ext import commands


# Cog class for Moderation Commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Unban command

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *,  member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name}#{user.discriminator} has been unbanned. ')
                return
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, you are not allowed to use this command.')

    
    # Kick command

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked.')
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, you are not allowed to use this command.')
    

    # Ban command

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned.')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, you are not allowed to use this command.')
    

    # Deleting messages command

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Cleared {amount} messages.')

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, you are not allowed to use this command.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the number of messages you want to clear.')
    
    
    # Setting up a mute role command

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def muterole(self, ctx, *, rolename = None):
        if rolename == None:
            exist_check = discord.utils.get(ctx.guild.roles, name="Muted")
            if exist_check == None:
                Guild = ctx.guild
                await Guild.create_role(name="Muted")
                await ctx.send(f"Added **Muted** Role")
                print("Here if")
            else:
                await ctx.send(f"There is already a **Muted** Role.")
                print("Here else")

        else:
            exist_check = discord.utils.get(ctx.guild.roles, name=rolename)
            if exist_check == None:
                Guild = ctx.guild
                await Guild.create_role(name=rolename)
                await ctx.send(f"Added **{rolename}** Role")
                print("Here if2")
            else:
                await ctx.send(f"There is already a **{rolename}** Role.")

    @muterole.error
    async def muterole_erorr(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, you are not allowed to use this command.")


    # Mute command

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member = None, mute_minutes: int = 0, *, reason: str = "None"):

        muted_role = discord.utils.get(ctx.guild.roles, name="muted")
        exist_check = discord.utils.get(ctx.guild.roles, name="muted")
        if exist_check == None:
            await ctx.send("there is no muted role")
            return

        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"{ctx.author.mention} has unmuted {member.mention}!")
            return

        elif member == None:
            await ctx.send("You need to mention the person you want to mute. You can't mute no one.")
            return

        elif member == ctx.author:
            await ctx.send("You can't mute yourself.")
            return

        elif self.client == member:  # To stop people from muting the bot it self
            embed = discord.Embed(title="You can't mute me fool, I'm a 2D anime waifu.")
            await ctx.send(embed=embed)
            return

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"{member.mention} has been muted by {ctx.author.mention} for: {reason}")

        if mute_minutes > 0:
            await asyncio.sleep(mute_minutes * 60)
            await member.remove_roles(muted_role, reason="time's up ")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, you are not allowed to use this command.")

    
    # warn command

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, msg, filename="warns.json"):
        memberid = member.id
        
        if ctx.author.id == memberid:
            await ctx.send("You can't warn yourself! Warn someone else.")
            return
        
        try:
            with open(os.path.join(os.path.dirname(__file__), filename), "r") as file:
                warn_amount_data = json.load(file)
                warn_amount = warn_amount_data[str(memberid)]["warn_amount"]
                warn_amount = warn_amount + 1
                for key in warn_amount_data:
                    if key == member.id:
                        return
                file.close()
                await ctx.send(f"{member.mention} has been warned!")

            warn_amount_data[str(memberid)] = {}
            warn_amount_data[str(memberid)]["warn_amount"] = warn_amount

            with open(os.path.join(os.path.dirname(__file__), "warns.json"), "w") as file:
                json.dump(warn_amount_data, file, indent=4)
                file.close()

        except Exception as e:
            # create a new variable for the person
            print(e)
            warn_amount = 1
            warn_amount_data[memberid] = {}
            warn_amount_data[memberid]["warn_amount"] = warn_amount
            await ctx.send(f"{member.mention} has been warned!")

        with open(os.path.join(os.path.dirname(__file__), "warns.json"), "w") as file:
            json.dump(warn_amount_data, file, indent=4)
            file.close()
        
    @warn.error
    async def on_warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, you are not allowed to use this command.")

def setup(client):
    client.add_cog(Moderation(client))