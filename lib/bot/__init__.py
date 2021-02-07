

from asyncio import sleep
from datetime import datetime
from glob import glob
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown, NotOwner, BotMissingPermissions, MissingPermissions, CheckFailure)
from discord.ext.commands import when_mentioned_or, command, has_permissions

from ..db import db
from ..utils.paginator import HelpPaginator, CannotPaginate

OWNER_IDS = [588473881120079872 ,692083694994849843 ,456456900414799873 , 451707918320926733,692083694994849843]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument,BotMissingPermissions, MissingPermissions )


def get_prefix(bot, message):
	prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
	if prefix:
		extras = ('t! ', 't!', 'T! ', 'T!',f'{prefix} ',f'{prefix}')
		
	else:
		db.execute('UPDATE guilds SET Prefix  = ? WHERE GuildID = ?', "+", message.guild.id)
		prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
		extras = (f'{prefix} ',f'{prefix}', 't! ', 't!', 'T! ', 'T!')
	
	return when_mentioned_or(*extras)(bot, message)



class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f" {cog} cog ready")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
	def __init__(self):
                intents = discord.Intents.default()
                intents.members = True
                intents.presences = True
                self.ready = False
                self.cogs_ready = Ready()
                self.guild = None
                self.scheduler = AsyncIOScheduler()
				
				
                
                db.autosave(self.scheduler)
                super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS, intents=intents, case_insensitive = True)

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f" {cog} cog loaded")

		print("setup complete")

	def update_db(self):
		db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
					 ((guild.id,) for guild in self.guilds))

		db.multiexec("INSERT OR IGNORE INTO permission (guildId) VALUES (?)",
					 ((guild.id,) for guild in self.guilds))
		db.multiexec("INSERT OR IGNORE INTO shoob (guildid) VALUES (?)",
					 ((guild.id,) for guild in self.guilds))

		db.multiexec("INSERT OR IGNORE INTO captcha (guid) VALUES (?)",
					 ((guild.id,) for guild in self.guilds))

		db.multiexec("INSERT OR IGNORE INTO boost (gu_id) VALUES (?)",
					 ((guild.id,) for guild in self.guilds))

		db.multiexec("INSERT OR IGNORE INTO guild_counters (guilds) VALUES (?)",
					 ((guild.id,) for guild in self.guilds))


		entries = [cmd.root_parent.name.lower() if cmd.parent else cmd.name.lower() for cmd in self.commands if not cmd.hidden]


		db.multiexec('INSERT OR IGNORE INTO global_counters (command) VALUES (?)',
		              ((cmd,) for cmd in entries))

		to_remove = []
		stored_guilds = db.column("SELECT GUILDID FROM guilds")
		for id_ in stored_guilds:
			if not self.get_guild(id_):
				to_remove.append(id_)

		db.multiexec("DELETE FROM guilds WHERE GUILDID = ?",
					 ((id_,) for id_ in to_remove))
		db.multiexec("DELETE FROM permission WHERE guildId = ?",
		             ((id_,) for id_ in to_remove))
		db.multiexec("DELETE FROM shoob WHERE guildid = ?",
		             ((id_,) for id_ in to_remove))
		db.multiexec("DELETE FROM captcha WHERE guid = ?",
					 ((id_,) for id_ in to_remove))

		db.multiexec("DELETE FROM boost WHERE gu_id = ?",
					 ((id_,) for id_ in to_remove))
		
		db.multiexec("DELETE FROM guild_counters WHERE guilds = ?",
					 ((id_,) for id_ in to_remove))


		entries = [cmd.root_parent.name.lower() if cmd.parent else cmd.name.lower() for cmd in self.commands if cmd.hidden]


		db.multiexec("DELETE FROM global_counters WHERE command = ?",
					 ((cmd,) for cmd in entries))
		

		db.commit()

	def run(self, version):
		self.VERSION = version

		print("running setup...")
		self.setup()

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("running bot...")
		super().run(self.TOKEN, reconnect=True)

	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=Context)

		if ctx.command is not None and ctx.guild is not None:
			if self.ready:
				await self.invoke(ctx)

			else:
				await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")



	async def on_connect(self):
		print(" bot connected")
		self.update_db()

	async def on_disconnect(self):
		print("bot disconnected")

	# async def on_error(self, err, *args, **kwargs):
	# 	if err == "on_command_error":
	# 		await args[0].send("Something went wrong.")

	# 	await self.stdout.send("An error occured.")
	# 	raise

	async def on_command_error(self, ctx, exc):
		if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			entity =  ctx.command
			p = await HelpPaginator.from_command(ctx, entity)
			



		elif isinstance(exc, NotOwner):
			await ctx.send("Only bot owner can use this command")
		elif isinstance(exc, CheckFailure):
			await ctx.send('that command has been disabled')

		elif isinstance(exc, CommandOnCooldown):
			await ctx.send(f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} secs.")

		elif hasattr(exc, "original"):
			if isinstance(exc.original, HTTPException):
				try:

					await ctx.send("Unable to send message.")
				except:
					pass

			if isinstance(exc.original, Forbidden):
				try:
					
				    await ctx.send("I do not have permission to do that.")
				except:
					pass

			else:
				pass

		else:
			pass

	async def on_ready(self):
		if not self.ready:
		
			self.scheduler.start()
			

			

		
			while not self.cogs_ready.all_ready():
				await sleep(0.5)

			self.ready = True
			print(" bot ready")
			

			await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= f'+help | rom rom ji sabko'))

		else:
			print("bot reconnected")
		
			await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= f'Le thare server me peshab krdiya'))

	async def on_message(self, message):
		if not message.author.bot:
			if isinstance(message.channel, DMChannel):
				pass 
				# if len(message.content) < 50:
				# 	await message.channel.send("Your message should be at least 50 characters in length.")

				# else:
				# 	member = self.guild.get_member(message.author.id)
				# 	embed = Embed(title="Modmail",
				# 				  colour=member.colour,
				# 				  timestamp=datetime.utcnow())

				# 	embed.set_thumbnail(url=member.avatar_url)

				# 	fields = [("Member", member.display_name, False),
				# 			  ("Message", message.content, False)]

				# 	for name, value, inline in fields:
				# 		embed.add_field(name=name, value=value, inline=inline)
					
				# 	mod = self.get_cog("Mod")
				# 	await mod.log_channel.send(embed=embed)
				# 	await message.channel.send("Message relayed to moderators.")

			else:
				await self.process_commands(message)


bot = Bot()
