from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog
import discord
from discord.ext.commands import command 
from discord.errors import HTTPException, Forbidden
from ..db import db

class Log(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			# rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", self.guild.id)
			# self.log_channel = self.bot.get_channel(rohan)
			self.bot.cogs_ready.ready_up("log")

	# @Cog.listener()
	# async def on_user_update(self, before, after):
	#  	if before.name != after.name:
	# 		 rohann = db.field("SELECT Logchannel FROM guilds WHERE GuildID =?",.guild.id)
	# 		 logchannel = self.bot.get_channel(rohann)
	# 		 embed = Embed(title=f"{before.name}#{before.discriminator} Username change",
	# 		               colour=after.colour,
	# 					   timestamp=datetime.utcnow())
						   
	# 		 fields = [("Before", before.name, False),
	# 		 ("After", after.name, False)]
	# 		 for name, value, inline in fields:
	# 			  embed.add_field(name=name, value=value, inline=inline)

			
	# 		 await logchannel.send(embed=embed)
				 

	#  	if before.discriminator != after.discriminator:
	#  		embed = Embed(title=f"{before.name}#{before.discriminator} Discriminator change",
	#  					  colour=after.colour,
	#  					  timestamp=datetime.utcnow())

	#  		fields = [("Before", before.discriminator, False),
	#  				  ("After", after.discriminator, False)]

	#  		for name, value, inline in fields:
	#  			embed.add_field(name=name, value=value, inline=inline)
				
	#  		rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", after.guild.id)
	#  		logchannel = self.bot.get_channel(rohan)

	#  		await logchannel.send(embed=embed)

	#  	if before.avatar_url != after.avatar_url:
	#  		embed = Embed(title=f"{before.name}#{before.discriminator} Avatar change ",
	#  					  description="New image is below, old to the right.",
	#  					   colour= 0xDD222,
	#  					  timestamp=datetime.utcnow())

	#  		embed.set_thumbnail(url=before.avatar_url)
	#  		embed.set_image(url=after.avatar_url)

	#  		rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", after.guild.id)
	#  		logchannel = self.bot.get_channel(rohan)


	#  		await logchannel.send(embed=embed)

	@Cog.listener()
	async def on_member_update(self, before, after):

		try: 

			if before.display_name != after.display_name:
				embed = Embed(title=f"{before.name}#{before.discriminator} Nickname change",
							colour=after.colour,
							timestamp=datetime.utcnow())
							
				fields = [("Before", before.display_name, False),
						("After", after.display_name, False)]
				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)
				rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", before.guild.id)
				logchannel = self.bot.get_channel(rohan)
				if logchannel is not None:
					await logchannel.send(embed=embed)
					
			elif before.roles != after.roles:
				embed = Embed(title=f"{before.name}#{before.discriminator} Role updates",
							colour=after.colour,
							timestamp=datetime.utcnow())
							
				fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
						("After", ", ".join([r.mention for r in after.roles]), False)]
						
				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)
				rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", before.guild.id)
				logchannel = self.bot.get_channel(rohan)
				if logchannel is not None:
					await logchannel.send(embed=embed)


		except discord.Forbidden:
                        pass


	# @on_member_update.error
	# async def member_update(self, ctx, exc):
	# 	if isinstance(exc, Forbidden):
	# 		pass


	@Cog.listener()
	async def on_message_edit(self, before, after):
                try :
                        if not after.author.bot:
                                if before.content != after.content:
                                        embed = Embed(title="Message edit",
                                                      description=f"Edit by {after.author.display_name}.",
                                                                  colour=after.author.colour,
                                                                  timestamp=datetime.utcnow())
                                        if len(before.content)>0 and len(after.content)>0 :
                                                                  
                                                fields = [("Before", before.content, False),
                                                          ("After", after.content, False)]
                                                                  
                                                for name, value, inline in fields:
                                                        embed.add_field(name=name, value=value, inline=inline)
                                                rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", before.guild.id)
                                                if rohan is not None:
                                                        logchannel = self.bot.get_channel(rohan)
                                                        if logchannel is not None :
                                                                await logchannel.send(embed=embed)
                except discord.Forbidden:
                        pass
					
	@Cog.listener()
	async def on_message_delete(self, message):
                try :
                        
                        if not message.author.bot:
                                embed = Embed(title="Message deletion",
                                              description=f"Action by {message.author.display_name}.",
                                                          colour=message.author.colour,
                                                          timestamp=datetime.utcnow())
                                if 1024> len(message.content) >0 :
                                                          
                                        fields = [("Content", message.content, False)]
                                        for name, value, inline in fields:
                                                embed.add_field(name=name, value=value, inline=inline)
                                        try:
                                                rohan = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", message.guild.id)
                                                if rohan is not None :
                                                        logchannel = self.bot.get_channel(rohan)
                                                        if logchannel is not None:
                                                                await logchannel.send(embed=embed)
                                        except:
                                                pass
                except discord.Forbidden:
                        pass


def setup(bot):
	bot.add_cog(Log(bot))
