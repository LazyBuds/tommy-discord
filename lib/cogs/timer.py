from discord.ext import tasks
from discord.ext.commands import Cog, command , bot_has_guild_permissions, has_permissions , BotMissingPermissions, MissingPermissions
from discord.ext import commands 
from random import choice 
from discord.errors import HTTPException, Forbidden
import discord
import datetime
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
start_time = time.time()
from ..db import db

class Timer(Cog):
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

       

    @custom_check()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_guild_permissions(manage_channels=True)
    @command(name="lockdown", aliases = ["lock"], description = 'lock and unlock a channel', usage = '+lock <channel>')
    async def lockdown(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"I have put `{channel.name}` on lockdown.")
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have put `{channel.name}` on lockdown.")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have removed `{channel.name}` from lockdown.")


    @lockdown.error
    async def lockdown_(self, ctx, exc):
        if isinstance(exc, BotMissingPermissions):
            await ctx.send("bot require manage channel perms to run this command.")
        elif isinstance(exc,MissingPermissions ):
            await ctx.send("user should have manage channel perms to run this command.")
        elif isinstance(exec, Forbidden):
            await ctx.send('I do not have permission to do that')


    @commands.command(pass_context=True, description = 'check bot uptime', usage = '+uptime')
    @custom_check()
    async def uptime(self, ctx):
        

        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=ctx.message.author.top_role.colour)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="Mady be love | Tommy")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)


    @command(name = 'template',description = 'Send us meme templates ', usage = '+template <link>')
    @custom_check()
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def template(self, ctx, *, link: str):
      

        e = discord.Embed(title="template", colour=0x00FF00)
        channel = self.bot.get_channel(714910677029879898)
        if channel is None:
            return
        e.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        e.description = link
        e.timestamp = ctx.message.created_at

        if ctx.guild is not None:
            e.add_field(
                name="Server",
                value=f"{ctx.guild.name} (ID: {ctx.guild.id})",
                inline=False,
            )

        e.add_field(
            name="Channel", value=f"{ctx.channel} (ID: {ctx.channel.id})", inline=False
        )
        e.set_footer(text=f"Author ID: {ctx.author.id}")

        await channel.send(embed=e)
        await ctx.send("Successfully sent feedback")


    


    @command(name = 'feedback',description = 'Gives feedback about the bot.', usage = '+feedback <content>')
    @custom_check()
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def feedback(self, ctx, *, content: str):
      

        e = discord.Embed(title="Feedback", colour=0x00FF00)
        channel = self.bot.get_channel(714910677029879898)
        if channel is None:
            return

        e.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        e.description = content
        e.timestamp = ctx.message.created_at

        if ctx.guild is not None:
            e.add_field(
                name="Server",
                value=f"{ctx.guild.name} (ID: {ctx.guild.id})",
                inline=False,
            )

        e.add_field(
            name="Channel", value=f"{ctx.channel} (ID: {ctx.channel.id})", inline=False
        )
        e.set_footer(text=f"Author ID: {ctx.author.id}")

        await channel.send(embed=e)
        await ctx.send("Successfully sent feedback")
        

    @command(name = 'suggestion',description = 'Give suggestions on the bot.', usage = '+suggestion <content>')
    @custom_check()
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def suggestion(self, ctx, *, content: str):
      

        e = discord.Embed(title="Suggestion", colour=0x00FF00)
        channel = self.bot.get_channel(772866944076087326)
        if channel is None:
            return

        e.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        e.description = content
        e.timestamp = ctx.message.created_at

        if ctx.guild is not None:
            e.add_field(
                name="Server",
                value=f"{ctx.guild.name} (ID: {ctx.guild.id})",
                inline=False,
            )

        e.add_field(
            name="Channel", value=f"{ctx.channel} (ID: {ctx.channel.id})", inline=False
        )
        e.set_footer(text=f"Author ID: {ctx.author.id}")

        await channel.send(embed=e)
        await ctx.send("Successfully sent suggestion")
        

    @command(name = 'pm', hidden=True)
    @custom_check()
    @commands.is_owner()
    async def pm(self, ctx, user_id: int, *, content: str):
        user = self.bot.get_user(user_id)

        fmt = (
            content
            + "\n\n*This is a DM sent because you had previously requested feedback or you reported a bug"
            " in a command you used*"
        )
        try:
            await user.send(fmt)
        except discord.Forbidden:
            await ctx.send("This user might be having DMs blocked or it's a bot account...") 
        else:
            await ctx.send("PM successfully sent.")
            


    
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("timer")
         


def setup(bot) :
    
    bot.add_cog(Timer(bot)) 
  
