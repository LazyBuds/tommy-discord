from datetime import datetime, timedelta
from typing import Optional
from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command , bot_has_permissions , has_permissions
from discord.ext.commands import CheckFailure
from discord.ext import commands
import platform
import discord
from time import time
import psutil 
import os 
from psutil import Process, virtual_memory
from lib import bot
from datetime import datetime
from ..db import db



class Infos(Cog):
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

	@command(name="userinfo", aliases=["memberinfo", "ui", "mi"], description  = 'display user stats')
	@custom_check()
	
	async def user_info(self, ctx, target: Optional[Member]):
		target = target or ctx.author

		embed = Embed(title="User information",
					  colour=target.colour,
					  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=target.avatar_url)

		fields = [("Name", str(target), True),
				  ("ID", target.id, True),
				  ("Bot?", target.bot, True),
				  ("Top role", target.top_role.mention, True),
				  ("Status", str(target.status).title(), True),
				  ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
				  ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Boosted", bool(target.premium_since), True)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)

	@command(name="serverinfo", aliases=["guildinfo", "si", "gi"], description  = 'display guild stats')
	@custom_check()
	@has_permissions(manage_channels=True)
	@bot_has_permissions(manage_channels=True)
	async def server_info(self, ctx):
		embed = Embed(title="Server information",
					  colour=ctx.guild.owner.colour,
					  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=ctx.guild.icon_url)

		statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

		fields = [("ID", ctx.guild.id, True),
				  ("Owner", ctx.guild.owner, True),
				  ("Region", ctx.guild.region, True),
				  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Members", len(ctx.guild.members), True),
				  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Banned members", len(await ctx.guild.bans()), True),
				  ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
				  ("Text channels", len(ctx.guild.text_channels), True),
				  ("Voice channels", len(ctx.guild.voice_channels), True),
				  ("Categories", len(ctx.guild.categories), True),
				  ("Roles", len(ctx.guild.roles), True),
				  ("Invites", len(await ctx.guild.invites()), True),
				  ("\u200b", "\u200b", True)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)
	@server_info.error
	async def serverstats_error(self, ctx, exc):
                if isinstance(exc, CheckFailure):
                        await ctx.send("bot require manage channel perms to run this command.")


	@command(name = "botinfo", aliases = ['bi', 'info'], description = 'display bot stats')
	@custom_check()
	async def stats(self, ctx):
		pythonVersion = platform.python_version()
		proc = Process()
		with proc.oneshot():
			uptime = timedelta(seconds=time()-proc.create_time())
			cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
			mem_total = virtual_memory().total / (1024**2)
			mem_of_total = proc.memory_percent()
			mem_usage = mem_total * (mem_of_total / 100)

		dpyVersion = discord.__version__
		serverCount = len(self.bot.guilds)

	
		member_count = 0
		for guild in self.bot.guilds :
                        member_count += len(guild.members)
		embed = discord.Embed(title = f'{self.bot.user.name} Stats', description = '\uFEFF', colour = ctx.author.colour, timestamp = ctx.message.created_at)
		embed.add_field(name = 'Bot Version:', value = "`1.2.0`")
		embed.add_field(name = 'Python Version:', value = f"`{pythonVersion}`")
		embed.add_field(name = 'Discord.Py Version', value = f"`{dpyVersion}`")
		embed.add_field(name = 'Total Guilds:', value = f"`{serverCount}`")
		embed.add_field(name = 'Total Users:', value = f"`{member_count}`")
		embed.add_field(name = 'Uptime', value  = f'`{uptime}`')
		embed.add_field(name = 'CPU Time', value  = f'`{cpu_time}`')
		embed.add_field(name = 'Memory Usage ',value = f"`{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)`")
		embed.add_field(name = 'Bot Developer:', value = "`Rohan, Kartik, Sanket`", inline =  False)
		embed.set_footer(text = f"Made with love | {self.bot.user.name}")
		embed.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
		await ctx.send(embed = embed)
		
	# @command(name = 'emojistat')
	# async def emojistat(self, ctx, channel : discord.TextChannel=None):
	# 	if not channel:
	# 		return await ctx.send("prefill channel")
	# 	allemojis = [str(e) for e in ctx.guild.emojis]
	# 	dict = {}
	# 	async with ctx.typing():
	# 		async for message1 in ctx.channel.history(limit = 5000, oldest_first = False):
	# 			if message1.content in allemojis:
	# 				if message1.content in dict.keys():
	# 					dict[f"{message1.content}"] += 1
	# 				else:
	# 					dict[f"{message1.content}"] = 1
	# 			sorted_d = (sorted(dict.items(), key=operator.itemgetter(1),reverse=True))
	# 			pages = MenuPages(source=MySource2(list(sorted_d)), clear_reactions_after=True,timeout=300.0, delete_message_after=True)
	# 			await pages.start(ctx)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("infos")


def setup(bot):
	bot.add_cog(Infos(bot))
