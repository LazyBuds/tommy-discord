from datetime import datetime
from typing import Optional
import discord
from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from discord.ext.commands import CheckFailure , BotMissingPermissions, MissingPermissions
from discord.ext import commands
import random
from discord import DMChannel
from ..db import db 

class Channels(Cog):
    def __init__(self, bot):
        self.bot = bot

    def custom_check():
        def predicate(ctx):
            cog = ctx.bot.get_cog("Fun") 
            command  =  db.field("SELECT commandname FROM command WHERE channelid = ?", ctx.channel.id)
            if command is not None:
                command.split(',')
                if  len(command)> 1 and ctx.command.name in command :
                    return 
                elif ctx.command.name in command :
                    return
            return True
        return commands.check(predicate)

    @Cog.listener()
    async def on_ready(self):
      if not self.bot.ready:
        self.bot.cogs_ready.ready_up("channels")

    @command(
        name="channelstats",
        aliases=["cs"],
        description="Sends a nice fancy embed with some channel stats",
        usage = '+channelstats'
    )
    @custom_check()

    
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channelstats(self, ctx, channel:discord.TextChannel = None):
        

        channel = channel or ctx.channel
        embed = discord.Embed(title=f"Stats for **{channel.name}**",
                                description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",
                                color= discord.Color.green())
        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=True)
        embed.add_field(name="Channel Id", value=channel.id, inline= True)
        embed.add_field(name="Channel Topic",value=f"{channel.topic if channel.topic else 'No topic.'}",inline=False)
        embed.add_field(name="Channel Position", value=channel.position + 1, inline=True)
        embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
        embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=True)
        embed.add_field(name="Channel is news?", value=channel.is_news(), inline=True)
        embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
        embed.add_field(name="Channel Permissions Synced",value=channel.permissions_synced,inline=True)
        embed.add_field(name="Channel Hash", value=hash(channel), inline=True)
        await ctx.send(embed=embed)
            
    @channelstats.error
    async def channelstats_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("bot require manage channel perms to run this command.")

    @commands.group(name = 'new', description = 'create new channels and categories',invoke_without_command=True)
    @commands.guild_only()
    @custom_check()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def new(self, ctx):
        
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    
        

    @new.command(
        name="category",
        description="Create a new category",
        usage="<role> <Category name>",
    )

    @commands.guild_only()
    @custom_check()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def category(self, ctx, role: discord.Role, *, name):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(f"Hey dude, I made {category.name} for ya!")

    @category.error
    async def new_error(self, ctx, exc):
        if isinstance(exc, BotMissingPermissions):
            await ctx.send("bot require manage channel perms to run this command.")
        elif isinstance(exc,MissingPermissions ):
            await ctx.send("user should have manage channel perms to run this command.")

    @new.command(
        name="channel",
        description="Create a new channel",
        usage="<role> <channel name>",
    )
    @commands.guild_only()
    @custom_check()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channel(self, ctx, role: discord.Role, *, name):
        
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        channel = await ctx.guild.create_text_channel(
            name=name,
            overwrites=overwrites,
            category=self.bot.get_channel(707945693582590005),
        )
        await ctx.send(f"Hey dude, I made {channel.name} for ya!")

    @channel.error
    async def channel_error(self, ctx, exc):
        if isinstance(exc, BotMissingPermissions):
            await ctx.send("bot require manage channel perms to run this command.")
        elif isinstance(exc,MissingPermissions ):
            await ctx.send("user should have manage channel perms to run this command.")

    @commands.group(name = 'delete', description = 'Delete channels and categories',invoke_without_command=True)
    @commands.guild_only()
    @custom_check()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def delete(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @delete.command(
        name="category", description="Delete a category", usage="<category> [reason]"
    )
    @commands.guild_only()
    @custom_check()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _category(self, ctx, category: discord.CategoryChannel, *, reason=None):
       
        await category.delete(reason=reason)
        await ctx.send(f"hey! I deleted {category.name} for you")

    @_category.error
    async def category_error(self, ctx, exc):
        if isinstance(exc, BotMissingPermissions):
            await ctx.send("bot require manage channel perms to run this command.")
        elif isinstance(exc,MissingPermissions ):
            await ctx.send("user should have manage channel perms to run this command.")

    @delete.command(
        name="channel", description="Delete a channel", usage="<channel> [reason]"
    )
    @commands.guild_only()
    @custom_check()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _channel(self, ctx, channel: discord.TextChannel = None, *, reason=None):
     
        channel = channel or ctx.channel
        await channel.delete(reason=reason)
        await ctx.send(f"hey! I deleted {channel.name} for you")



    @_channel.error
    async def delete_channel(self, ctx, exc):
        if isinstance(exc, BotMissingPermissions):
            await ctx.send("bot require manage channel perms to run this command.")
        elif isinstance(exc,MissingPermissions ):
            await ctx.send("user should have manage channel perms to run this command.")

    @commands.group(name  = 'shoob')
    @custom_check()
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def shoob(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @shoob.command(name = 't1')
    async def t1(self,ctx, *, role:discord.Role):
        
        db.execute('UPDATE shoob SET t1 = ? WHERE guildid = ?',role.id, ctx.guild.id)
        await ctx.send(f't1 ping role has been set to {role}')

    @shoob.command(name = 't2')
    async def t2(self,ctx, *, role:discord.Role ):
        
        db.execute('UPDATE shoob SET t2 = ? WHERE guildid = ?',role.id , ctx.guild.id)
        await ctx.send(f't2 ping role has been set to {role}')

    @shoob.command(name = 't3')
    async def t3(self,ctx, *, role:discord.Role):
        
        db.execute('UPDATE shoob SET t3 = ? WHERE guildid = ?',role.id, ctx.guild.id)
        await ctx.send(f't3 ping role has been set to {role}')

    @shoob.command(name = 't4')
    async def t4(self,ctx, *, role:discord.Role ):
      
        db.execute('UPDATE shoob SET t4 = ? WHERE guildid = ?',role.id , ctx.guild.id)
        await ctx.send(f't4 ping role has been set to {role}')

    @shoob.command(name = 't5')
    async def t5(self,ctx, *, role:discord.Role):
     
        db.execute('UPDATE shoob SET t5 = ? WHERE guildid = ?',role.id, ctx.guild.id)
        await ctx.send(f't5 ping role has been set to {role}')


    @shoob.command(name = 't6')
    async def t6(self,ctx, *, role:discord.Role):
      
        db.execute('UPDATE shoob SET t6 = ? WHERE  guildid = ?',role.id, ctx.guild.id)
        await ctx.send(f't6 ping role has been set to {role}')

    @shoob.command(name = 'rm', description = 'remove role from the cardping')
    async def rm(self,ctx, tier):
        db.execute(f'UPDATE shoob SET {tier} = NULL WHERE guildid =?',ctx.guild.id)
        await ctx.send(f'{tier} role ping has been removed')
        


    @shoob.command(name = 'cardping')
    async def cardping(self,ctx):
        t1 = db.field("SELECT t1 FROM shoob WHERE guildid = ?", ctx.guild.id) 
        t2 = db.field("SELECT t2 FROM shoob WHERE guildid = ?", ctx.guild.id)
        t3 = db.field("SELECT t3 FROM shoob WHERE guildid = ?", ctx.guild.id)
        t4 = db.field("SELECT t4 FROM shoob WHERE guildid = ?", ctx.guild.id)
        t5 = db.field("SELECT t5 FROM shoob WHERE guildid = ?", ctx.guild.id)
        t6 = db.field("SELECT t6 FROM shoob WHERE guildid = ?", ctx.guild.id)
        if t1 is None :
            t1 =='None'
        else :
            t1 = f'<@&{t1}>'
        if t2 is None :
            t2 =='None'
        else  :
            t2 = f'<@&{t2}>'

        if t3 is None :
            t3 =='None'
        else :
            t3 = f'<@&{t3}>'

        if t4 is None :
            t4 =='None'
        else :
            t4 = f'<@&{t4}>'
            
        if t5 is None :
            t5 =='None'
        else :
            t5 = f'<@&{t5}>'
        if t6 is None :
            t6 =='none'
        else :
            t6 = f'<@&{t6}>'

        embed = discord.Embed(description = f" \n**T1 ping role** -  {t1} \n**T2 ping role** -  {t2} \n**T3 ping role** -  {t3} \n**T4 ping role** -  {t4} \n**T5 ping role** -  {t5} \n**T6 ping role** -  {t6} \n" , color=discord.Color(0x303136))
        embed.set_author(name = f'{ctx.guild.name} card ping', icon_url = ctx.guild.icon_url)
        

        await ctx.send(embed=embed)


    @shoob.error
    async def shoob_error(self, ctx, exc):
        if isinstance(exc, BotMissingPermissions):
            await ctx.send("bot require manage roles perms to run this command.")
        elif isinstance(exc,MissingPermissions ):
            await ctx.send("user should have manage roles perms to run this command.")


    




    @Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, DMChannel):
            return
        t1 = db.field("SELECT t1 FROM shoob WHERE guildid = ?", message.guild.id)
        t2 = db.field("SELECT t2 FROM shoob WHERE guildid = ?", message.guild.id)
        t3 = db.field("SELECT t3 FROM shoob WHERE guildid = ?", message.guild.id)
        t4 = db.field("SELECT t4 FROM shoob WHERE guildid = ?", message.guild.id)
        t5 = db.field("SELECT t5 FROM shoob WHERE guildid = ?", message.guild.id)
        t6 = db.field("SELECT t6 FROM shoob WHERE guildid = ?", message.guild.id)
        
        # rohan = db.field("SELECT Muterole FROM permission WHERE GuildID = ?", guild.id)

		# muterole = self.bot.guild.get_role(rohan)
      
        try :
            if message.embeds :
                embed = message.embeds[0]
                if embed.title[-7:] == "Tier: 1":

                    role  = message.channel.guild.get_role(t1)
                    

                    
                    
                  
                    
                    await message.channel.send(f'`{embed.title}` has appeared {role.mention} ')
                    
                if embed.title[-7:] == "Tier: 2":
                    role  = message.channel.guild.get_role(t2)
                    
                    
                    
                    await message.channel.send(f'`{embed.title}` has appeared {role.mention} ')

                if embed.title[-7:] == "Tier: 3":
                    role  = message.channel.guild.get_role(t3)
                    
                    
                    
                    await message.channel.send(f'`{embed.title}` has appeared {role.mention} ')


                if embed.title[-7:] == "Tier: 4":
                    role  = message.channel.guild.get_role(t4)
                    
                    
                    
                    await message.channel.send(f'`{embed.title}` has appeared {role.mention} ')

                if embed.title[-7:] == "Tier: 5":
                    role  = message.channel.guild.get_role(t5)
                    
                    
                    
                    await message.channel.send(f'`{embed.title}` has appeared {role.mention} ')


                if embed.title[-7:] == "Tier: 6":
                    role  = message.channel.guild.get_role(t6)
                    
                    
                    
                    await message.channel.send(f'`{embed.title}` has appeared {role.mention} ')

        except :
            pass


def setup(bot):
    bot.add_cog(Channels(bot))
