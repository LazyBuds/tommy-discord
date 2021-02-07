from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional
import discord
from discord import Spotify
import textwrap
import pendulum
from discord import Embed, Member, DMChannel
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions, cooldown, BucketType
from discord.ext import commands
import re
import asyncio

from ..db import db



time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(f"{value} is an invalid time key! h|m|s|d are valid arguments")
            except ValueError:
                raise commands.BadArgument(f"{key} is not a number!")
        return time


class Mod(Cog):
	def __init__(self, bot):
		self.bot = bot

		self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
		self.links_allowed = (711223407911370812, 711246048756236348, 714910677029879898)
		self.images_allowed = (711223407911370812, 711246048756236348)

	def custom_check():
		def predicate(ctx):
			
			command  =  db.field("SELECT commandname FROM command WHERE channelid = ?", ctx.channel.id)
			if command is not None:
				command.split(',')
				if  len(command)> 1 and ctx.command.name in command :
					return 
				elif ctx.command.name in command :
					return
			return True
		return commands.check(predicate)

	# async def kick_members(self, message, targets, reason):
	# 	for target in targets:
	# 		if (message.guild.me.top_role.position > target.top_role.position 
	# 			and not target.guild_permissions.administrator):
	# 			await target.kick(reason=reason)

	# 			embed = Embed(title="Member kicked",
	# 						colour=0xDD2222,
	# 						timestamp=datetime.utcnow())

	# 			embed.set_thumbnail(url=target.avatar_url)

	# 			fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
	# 					("Actioned by", message.author.display_name, False),
	# 					("Reason", reason, False)]

	# 			for name, value, inline in fields:
	# 				embed.add_field(name=name, value=value, inline=inline)
	# 			rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", target.guild.id)
	# 			logchannel = self.bot.get_channel(rohan)
	# 			if logchannel != None:
	# 				await logchannel.send(embed=embed)
					
	@command(name = 'voicekick', aliases  = ['vk'], description = 'voicekick someone', usage = '+vk <user>')
	@custom_check()
	@bot_has_permissions(manage_channels=True)
	@has_permissions(manage_channels=True)
	async def voicekick (self, ctx,member : discord.Member = None, reason= None):
		member = member or ctx.author
		await member.move_to(channel = None)
		embed = Embed(title="Member voice kicked",
					  colour=0xDD2222,
		 			  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=member.avatar_url)

		fields = [("Member", f"{member.name} a.k.a. {member.display_name}", False),
				("Actioned by", ctx.author.display_name, False),
				("Reason", reason, False)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", ctx.guild.id)
		logchannel = self.bot.get_channel(rohan)
		if logchannel != None:
			await logchannel.send(embed=embed)
			await ctx.send("Action complete.")
		else :
			await ctx.send(embed=embed)
		

	@voicekick.error
	async def voicekick_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")


	# @command(name = 'dehoist')
	# async def dehoist(self,ctx):
	# 	unhoists = 0

	# 	async with ctx.channel.typing():
	# 		for member in ctx.guild.members:
	# 			try:
	# 				if(match:= re.match("[^A-Za-z]+", member.display_name)) is not None:
	# 					await member.edit(nick = member.display_name.replace(match.group(),"",1))
	# 					unhoists +=1
	# 			except discord.Forbidden:
	# 				pass

	@command(name="kick", description = 'kick someone', usage = '+kick <user> <reason>')
	@custom_check()
	@bot_has_permissions(kick_members=True)
	@has_permissions(kick_members=True)
	async def kick_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
		if not len(targets):
			await ctx.send("One or more required arguments are missing.")

		else:
			for target in targets:
				if (ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissions.administrator):
					try:
						await target.send(f'you have been kicked in {ctx.guild.name} for `{reason}`')
					except:
						pass
					await target.kick(reason=reason)

					embed = Embed(title="Member kicked",
								colour=0xDD2222,
								timestamp=datetime.utcnow())

					embed.set_thumbnail(url=target.avatar_url)

					fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
							("Actioned by", ctx.author.display_name, False),
							("Reason", reason, False)]

					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
					rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", target.guild.id)
					logchannel = self.bot.get_channel(rohan)
					if logchannel != None:
						await logchannel.send(embed=embed)
						await ctx.send("Action complete.")
					else :
						await ctx.send(embed=embed)

				else :
					await ctx.send('user cannot be kicked')
				
				


	@kick_command.error
	async def kick_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")



	# @command(name = 'afk')
	# async def afk(self,ctx , *, reason):
	# 	ok = db.field

	# async def ban_members(self, message, targets, reason):
	# 	for target in targets:
	# 		if (message.guild.me.top_role.position > target.top_role.position 
	# 			and not target.guild_permissions.administrator):
	# 			await target.ban(reason=reason)

	# 			embed = Embed(title="Member banned",
	# 						  colour=0xDD2222,
	# 						  timestamp=datetime.utcnow())

	# 			embed.set_thumbnail(url=target.avatar_url)

	# 			fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
	# 					  ("Actioned by", message.author.display_name, False),
	# 					  ("Reason", reason, False)]

	# 			for name, value, inline in fields:
	# 				embed.add_field(name=name, value=value, inline=inline)

	# 			rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", target.guild.id)
	# 			logchannel = self.bot.get_channel(rohan)
	# 			if logchannel != None:
	# 				await logchannel.send(embed=embed)

	@command(name="ban", description  = 'ban someone', usage = '+ban <user> reason')
	@custom_check()
	@bot_has_permissions(ban_members=True)
	@has_permissions(ban_members=True)
	async def ban_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
		if not len(targets):
			await ctx.send("One or more required arguments are missing.")

		else:
			for target in targets:
				if (ctx.guild.me.top_role.position > target.top_role.position 
					and not target.guild_permissions.administrator):
					try:
						await target.send(f'you have been banned in {ctx.guild.name} for `{reason}`')
					except :
						pass
					await target.ban(reason=reason)

					embed = Embed(title="Member banned",
								colour=0xDD2222,
								timestamp=datetime.utcnow())

					embed.set_thumbnail(url=target.avatar_url)

					fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
							("Actioned by", ctx.author.display_name, False),
							("Reason", reason, False)]

					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)

					rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", target.guild.id)
					logchannel = self.bot.get_channel(rohan)
					if logchannel != None:
						await logchannel.send(embed=embed)
						await ctx.send("Action complete.")
					else :
						await ctx.send(embed=embed)

				else :
					await ctx.send('user cannot be banned')
			
		

	@ban_command.error
	async def ban_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")

	@command(name="clear", aliases=["purge"], description  = 'purge chat', usage = '+clear <user> <limit>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	@bot_has_permissions(manage_messages=True)
	@has_permissions(manage_messages=True)
	async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int] = 1):
		def _check(message):
			return not len(targets) or message.author in targets

		if 0 < limit <= 100:
			with ctx.channel.typing():
				await ctx.message.delete()
				deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14),
												  check=_check)

				await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)

		else:
			await ctx.send("The limit provided is not within acceptable bounds.")

	@clear_messages.error
	async def clear_messages_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")

	@commands.group(name = 'afk', description = 'let bot handle your pings when you are afk',invoke_without_command=True)
	@custom_check()
	@commands.guild_only()
	@commands.has_guild_permissions(manage_channels=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def afk(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send_help(str(ctx.command))
			
	@afk.command(name  ='dnd')
	@custom_check()
	@commands.guild_only()
	@commands.has_guild_permissions(manage_channels=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def dnd(self,ctx, *, reason = None ):
		try :

			ty = 'dnd'
			reason = reason or 'user is afk '
			ids = db.column("SELECT UserID FROM afk")
			if (ctx.author.id + ctx.guild.id) in ids :
				await ctx.send('user is already afk')
			else :
			
				db.execute("INSERT INTO afk (UserID,Guildid, afktype, afkreason) VALUES (?,?,?,?)", ctx.author.id + ctx.guild.id,  ctx.guild.id, ty, reason)
				await ctx.send(f'afk has been set to :- {reason}')
		except :
			pass

	@dnd.error
	async def dnd_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")


	@afk.command(name  ='spotify')
	@custom_check()
	@commands.guild_only()
	@commands.has_guild_permissions(manage_channels=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def spotifyy(self,ctx, *, reason = None ):
		try :

			ty = 'spotify'
			reason = reason or 'user is afk '
			ids = db.column("SELECT UserID FROM afk")
			if (ctx.author.id + ctx.guild.id) in ids :
				await ctx.send('user is already afk')
			else :
			
				db.execute("INSERT INTO afk (UserID,Guildid, afktype, afkreason) VALUES (?,?,?,?)", ctx.author.id + ctx.guild.id,  ctx.guild.id, ty, reason)
				await ctx.send(f'afk has been set to :- {reason}')
			
		except :
			pass

	@spotifyy.error
	async def spotify_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")
		# ids = db.column("SELECT UserID FROM afk")
		# if ctx.author.id in ids :
		# check2 = db.field('SELECT  FROM command WHERE channelid = ?', ctx.channel.id)
		# db.execute('UPDATE afk SET afktype =?,afkreason =?,')
			
		# 	await ctx.send(f'afk has been set to :- {reason}')
		# else : 
		# 	db.execute("INSERT INTO afk (UserID, Guildid, afktype, afkreason) VALUES (?,?,?,?)", ctx.author.id, ctx.guild.id, ty, reason)
		


        #         if check2 is  None :
        #             db.execute('UPDATE command SET commandname = ? WHERE channelid = ?',command, ctx.channel.id)
        #             await ctx.send('command has been disabled')
        #         elif check2 is not None :
        #             newcheck = check2.split(",")
	
# newcheck = check2.split(",")
#                     if len(newcheck) > 1 :
#                         if command in newcheck :
                         
#                             await ctx.send('command is already disabled')
#                         else :
#                             newcheck.append(command)
#                             newcheck2 = ','.join(newcheck)
#                             db.execute('UPDATE command SET commandname = ? WHERE channelid = ?',newcheck2, ctx.channel.id)
#                             await ctx.send('command has been disabled')
#                     else : 
#                         if command in newcheck:
#                             await ctx.send('that command is already disabled')
                            
#                         else :
                            
#                             newcheck.append(command)
#                             newcheck2 = ','.join(newcheck)
#                             db.execute('UPDATE command SET commandname = ? WHERE channelid = ?',newcheck2, ctx.channel.id)
#                             await ctx.send('that command has been disabled')

	@Cog.listener()
	async def on_message(self, message):


		if isinstance(message.channel, DMChannel): 
			pass
		else:

			ids = db.column("SELECT UserID FROM afk")
			
			
			prefix = db.field('SELECT Prefix FROM guilds WHERE GuildID = ?', message.guild.id)
			if (message.author.id + message.guild.id) in ids and not message.content.startswith(f'{prefix}afk') :
				guil = db.field("SELECT Guildid FROM afk WHERE UserID  =?", message.author.id+message.guild.id)
				if guil == message.guild.id:
					db.execute("DELETE FROM afk WHERE UserID = ?", message.author.id + message.guild.id)
					await message.channel.send(f'I removed your afk {message.author.mention}')
				

			
			if message.mentions :
				for mention in message.mentions :
					if mention.id + message.guild.id  in ids and message.author.id + message.guild.id not in ids:
						gui = db.field("SELECT Guildid FROM afk WHERE UserID  =?", mention.id + mention.guild.id)
							
						if gui == message.guild.id:
							afktype  = db.field("SELECT afktype FROM afk WHERE UserID  = ?",  mention.id + mention.guild.id)
							if afktype =='dnd':

								reason  = db.field("SELECT afkreason FROM afk WHERE UserID  = ?", mention.id + mention.guild.id)
								
								
								
								await message.channel.send(f"`The user is currently AFK:` {reason}")
							elif afktype =='spotify':
								for activity in mention.activities:
									if isinstance(activity, Spotify):
										em = Embed(color=discord.Color.dark_green())
										em.title = f'{mention.name} is listening to: {activity.title}'
										em.set_thumbnail(url=activity.album_cover_url)
										em.description = f"**Song Name**: {activity.title}\n**Song Artist**: {activity.artist}\n**Song Album**: {activity.album}\n**Song Length**: {pendulum.duration(seconds=activity.duration.total_seconds()).in_words(locale='en')}"
										await message.channel.send(embed=em)
										break
								else:
									reason  = db.field("SELECT afkreason FROM afk WHERE UserID  = ?", mention.id + mention.guild.id )
									await message.channel.send(f"`The user is currently AFK:` {reason}")
									

		



		




	# async def mute_members(self, message, targets, time : TimeConverter , reason):
	# 	unmutes = []
	# 	rohan = db.field("SELECT Muterole FROM permission WHERE GuildID = ?", message.guild.id)
	# 	muterole = self.bot.guild.get_role(rohan)
	# 	if rohan != None :

	# 		for target in targets:
				
	# 			if not muterole in target.roles:
	# 				if message.guild.me.top_role.position > target.top_role.position:
	# 					role_ids = ",".join([str(r.id) for r in target.roles])
	# 					end_time = datetime.utcnow() + timedelta(seconds=time) if time else None

						

	# 					await target.edit(roles=[muterole])

	# 					embed = Embed(title="Member muted",
	# 								colour=0xDD2222,
	# 								timestamp=datetime.utcnow())

	# 					embed.set_thumbnail(url=target.avatar_url)

	# 					fields = [("Member", target.display_name, False),
	# 							("Actioned by", message.author.display_name, False),
	# 							("Duration", f"{time:,} seconds" if time else "Indefinite", False),
	# 							("Reason", reason, False)]

	# 					for name, value, inline in fields:
	# 						embed.add_field(name=name, value=value, inline=inline)
	# 					db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
	# 							target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())
	# 					rohann = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", target.guild.id)
	# 					logchannel = self.bot.get_channel(rohann)
	# 					if logchannel != None:
	# 						await logchannel.send(embed=embed)

	# 					if time:
	# 						unmutes.append(target)

	# 	else :
	# 		await message.channel.send('user is already muted')

	# 	return unmutes


	# async def unmute_members(self, guild, targets, *, reason="Mute time expired."):
	# 	rohan = db.field("SELECT Muterole FROM permission WHERE GuildID = ?", guild.id)

	# 	muterole = self.bot.guild.get_role(rohan) or self.bot.guild.get_role("Muted") or self.bot.guild.get_role("muted")
	# 	for target in targets:
	# 		if muterole in target.roles:
	# 			role_ids = db.field("SELECT RoleIDs FROM mutes WHERE UserID = ?", target.id)
	# 			roles = [guild.get_role(int(id_)) for id_ in role_ids.split(",") if len(id_)]

	# 			db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)
	# 			if role_ids != None:

	# 				await target.edit(roles=roles)

	# 				embed = Embed(title="Member unmuted",
	# 							colour=0xDD2222,
	# 							timestamp=datetime.utcnow())

	# 				embed.set_thumbnail(url=target.avatar_url)

	# 				fields = [("Member", target.display_name, False),
	# 						("Reason", reason, False)]

	# 				for name, value, inline in fields:
	# 					embed.add_field(name=name, value=value, inline=inline)
	# 				rohann = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", target.guild.id)
	# 				logchannel = self.bot.get_channel(rohann)
	# 				if logchannel != None:
	# 					await logchannel.send(embed=embed)
	# 				else :
	# 					pass
			
	# 			else :
	# 				pass
	# 		else :
	# 			pass


	# @command(name="mute", description = 'mute someone', usage = '+mute <user> <time> <reason>')
	# @bot_has_permissions(manage_roles=True)
	# @has_permissions(manage_roles=True, manage_guild=True)
	# async def mute_command(self, ctx, targets: Greedy[Member], time: TimeConverter, *,
	# 					   reason: Optional[str] = "No reason provided."):
	# 	'''+mute @Rohan#7140 1h spam'''
	# 	if not len(targets):
	# 		await ctx.send("One or more required arguments are missing.")

	# 	else:
			
	# 		unmutes = []
	# 		rohan = db.field("SELECT Muterole FROM permission WHERE GuildID = ?", ctx.guild.id)
	# 		muterole = ctx.bot.guild.get_role(rohan) or ctx.bot.guild.get_role("Muted") or ctx.bot.guild.get_role("muted")

	# 		for target in targets:
				
	# 			if not muterole in target.roles:
	# 				if ctx.guild.me.top_role.position > target.top_role.position:
	# 					role_ids = ",".join([str(r.id) for r in target.roles])
	# 					end_time = datetime.utcnow() + timedelta(seconds=time) if time else None

	# 					# try :
	# 					await target.edit(roles=[muterole])
					
			


	# 					embed = Embed(title="Member muted",
	# 								colour=0xDD2222,
	# 								timestamp=datetime.utcnow())

	# 					embed.set_thumbnail(url=target.avatar_url)

	# 					fields = [("Member", target.display_name, False),
	# 							("Actioned by", ctx.author.display_name, False),
	# 							("Duration", f"{time:,} seconds" if time else "Indefinite", False),
	# 							("Reason", reason, False)]

	# 					for name, value, inline in fields:
	# 						embed.add_field(name=name, value=value, inline=inline)
	# 					db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
	# 							target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())
	# 					rohann = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", target.guild.id)
	# 					logchannel = self.bot.get_channel(rohann)
	# 					if time:
	# 						unmutes.append(target)
	# 					if logchannel != None:
	# 						await logchannel.send(embed=embed)
	# 						await ctx.send("Action complete.")
	# 					else :
	# 						await ctx.send(embed=embed)
	# 					# except :
	# 					# 	await ctx.send('set mute role first')

	# 				else :
	# 					await ctx.send('user cannot be muted')
						

						
							
	# 			else :
	# 				await ctx.channel.send('user is already muted')

		
			

	# 		if len(unmutes):
	# 			await sleep(time)
	# 			await self.unmute_members(ctx.guild, targets)

	# @mute_command.error
	# async def mute_command_error(self, ctx, exc):
	# 	if isinstance(exc, CheckFailure):
	# 		await ctx.send("Insufficient permissions to perform that task.")

	
		

	# @command(name="unmute", description  = 'unmute someone', usage = '+unmute <user> <reason>')
	# @bot_has_permissions(manage_roles=True)
	# @has_permissions(manage_roles=True, manage_guild=True)
	# async def unmute_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
	# 	if not len(targets):
	# 		await ctx.send("One or more required arguments is missing.")

	# 	else:
	# 		rohan = db.field("SELECT Muterole FROM permission WHERE GuildID = ?", ctx.guild.id)
	# 		muterole = self.bot.guild.get_role(rohan) or ctx.bot.guild.get_role("Muted") or ctx.bot.guild.get_role("muted")
	# 		for target in targets: 
	# 			if muterole in target.roles:
	# 				role_ids = db.field("SELECT RoleIDs FROM mutes WHERE UserID = ?", target.id)
	# 				rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", target.guild.id)
	# 				if role_ids != None:
	# 					roles = [ctx.guild.get_role(int(id_)) for id_ in role_ids.split(",") if len(id_)]
	# 					db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)
	# 					await target.edit(roles=roles)
						
	# 				else :
	# 					await target.remove_roles(muterole) 
		

					

	# 				embed = Embed(title="Member unmuted",
	# 							colour=0xDD2222,
	# 							timestamp=datetime.utcnow())

	# 				embed.set_thumbnail(url=target.avatar_url)

	# 				fields = [("Member", target.display_name, False),
	# 						("Reason", reason, False)]

	# 				for name, value, inline in fields:
	# 					embed.add_field(name=name, value=value, inline=inline)
	# 				rohann = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", target.guild.id)
	# 				logchannel = self.bot.get_channel(rohann)
	# 				if logchannel != None:
	# 					await logchannel.send(embed=embed)
	# 					await ctx.send("Action complete.")
	# 				else :
						
	# 					await ctx.send(embed=embed)
	# 			else :
	# 				await ctx.channel.send('user is already unmuted')
					

	

	# @command(name="addprofanity", aliases=["addswears", "addcurses"])
	# @has_permissions(manage_guild=True)
	# async def add_profanity(self, ctx, *words):
	# 	with open("./data/profanity.txt", "a", encoding="utf-8") as f:
	# 		f.write("".join([f"{w}\n" for w in words]))

	# 	profanity.load_censor_words_from_file("./data/profanity.txt")
	# 	await ctx.send("Action complete.")

	# @command(name="delprofanity", aliases=["delswears", "delcurses"])
	# @has_permissions(manage_guild=True)
	# async def remove_profanity(self, ctx, *words):
	# 	with open("./data/profanity.txt", "r", encoding="utf-8") as f:
	# 		stored = [w.strip() for w in f.readlines()]

	# 	with open("./data/profanity.txt", "w", encoding="utf-8") as f:
	# 		f.write("".join([f"{w}\n" for w in stored if w not in words]))

	# 	profanity.load_censor_words_from_file("./data/profanity.txt")
	# 	await ctx.send("Action complete.")

	@command(name = 'warn', description  = 'warn someone', usage  = '+warn <user> <reason>')
	@commands.guild_only()
	@custom_check()
	@commands.has_permissions(manage_guild = True)
	@bot_has_permissions(manage_guild = True)
	async def warn (self, ctx, target : Member , *, reason):
		embed = Embed(description=f"***{target} has been warned***,**{reason}**")
		await ctx.send(embed=embed)
		try :
			await target.send(f"You've been warned in {ctx.guild.name} for; `{reason}`")
		except :
			pass
		
		embedd = Embed(title="Member warned",
							colour=0xDD2222,
							timestamp=datetime.utcnow())

		embedd.set_thumbnail(url=target.avatar_url)

		fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
				("Actioned by", ctx.author.display_name, False),
				("Reason", reason, False)]

		for name, value, inline in fields:
			embedd.add_field(name=name, value=value, inline=inline)

		rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", target.guild.id)
		logchannel = self.bot.get_channel(rohan)
		if logchannel != None:
			await logchannel.send(embed=embedd)
	
	@warn.error
	async def warn_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")

	@commands.command(
        name="unban",
        description="A command which unbans a given user",
        usage="<user> [reason]",
    )
	@commands.guild_only()
	@custom_check()
	@bot_has_permissions(ban_members=True)
	@has_permissions(ban_members=True)
	
	async def unban(self, ctx, target, *, reason=None):
		# try:
			member = await self.bot.fetch_user(int(target))
			await ctx.guild.unban(member, reason=reason)
			embed = Embed(title="Member unbanned",
							colour=0xDD2222,
							timestamp=datetime.utcnow())

			

			fields = [("Member", f"{member.name}", False),
					("Actioned by", ctx.author.display_name, False),
					("Reason", reason, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", ctx.guild.id)
			logchannel = self.bot.get_channel(rohan)
			if logchannel != None:
				await logchannel.send(embed=embed)
				await ctx.send("Action complete.")
			else :
				await ctx.send(embed=embed)
		# except :
		# 	await ctx.send('Member is not banned')

	@unban.error
	async def unban_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")




	


 


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			
		

			self.bot.cogs_ready.ready_up("mod")

	# @Cog.listener()
	# async def on_message(self, message):
	# 	def _check(m):
	# 		return (m.author == message.author
	# 				and len(m.mentions)
	# 				and (datetime.utcnow()-m.created_at).seconds < 60)

	# 	if not message.author.bot:
	# 		# if len(list(filter(lambda m: _check(m), self.bot.cached_messages))) >= 3:
	# 		# 	await message.channel.send("Don't spam mentions!", delete_after=10)
	# 		# 	unmutes = await self.mute_members(message, [message.author], 5, reason="Mention spam")

	# 			# if len(unmutes):
	# 			# 	await sleep(5)
	# 			# 	await self.unmute_members(message.guild, [message.author])

	# 		if profanity.contains_profanity(message.content):
	# 			await message.delete()
	# 			await message.channel.send("You can't use that word here.", delete_after=10)

			# #XX commented out so it doesn't interfere with the rest of the server while recording
			# elif message.channel.id not in self.links_allowed and search(self.url_regex, message.content):
			# 	await message.delete()
			# 	await message.channel.send("You can't send links in this channel.", delete_after=10)

			# elif (message.channel.id not in self.images_allowed
			#     and any([hasattr(a, "width") for a in message.attachments])):
			# 	await message.delete()
			# 	await message.channel.send("You can't send images here.", delete_after=10)


def setup(bot):
	bot.add_cog(Mod(bot))
