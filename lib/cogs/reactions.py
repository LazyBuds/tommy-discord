from datetime import datetime, timedelta

from discord import Embed
from discord.ext import commands
import re
import discord
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions

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





# Here are all the number emotes.
# 0⃣ 1️⃣ 2⃣ 3⃣ 4⃣ 5⃣ 6⃣ 7⃣ 8⃣ 9⃣

# numbers = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣",
# 		   "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟")

numbers = ("⬆️","⬇️")


class Reactions(Cog):
    
	def __init__(self, bot):
		self.bot = bot
		self.polls = []
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
			
			self.bot.cogs_ready.ready_up("reactions")

	

	


	

	@command(name="createpoll", aliases=["poll"], description = 'start a poll', usage = '+poll <time> <question>')
	@custom_check()
	# @has_permissions(manage_guild=True) new
	async def create_poll(self, ctx, time: TimeConverter, *, question:str):
		'''+poll 1m kya mai cute hu '''
		try:


		

                    embed = Embed(title="Poll",
                                            colour=ctx.author.colour,
                                            timestamp=datetime.utcnow())

                    embed.add_field(name = 'Question', value = question,inline = False)
                    embed.add_field(name = 'Time', value = time, inline = False)

                    message = await ctx.send(embed=embed)

                    for emoji in numbers:
                            await message.add_reaction(emoji)

                    self.polls.append((message.channel.id, message.id))

                    self.bot.scheduler.add_job(self.complete_poll, "date", run_date=datetime.now()+timedelta(seconds =time),args=[message.channel.id, message.id])
		except:
                    await ctx.send(f'type {ctx.prefix}help createpoll')


	async def complete_poll(self, channel_id, message_id):
                try:
                    message = await self.bot.get_channel(channel_id).fetch_message(message_id)

                    most_voted = max(message.reactions, key=lambda r: r.count)
                    for reaction in message.reactions :
                            if str(reaction.emoji) =='⬆️':
                                    x = reaction.count
                            if str(reaction.emoji) =='⬇️':
                                    y = reaction.count
                    if x == y :
                            await message.channel.send(" The results are in and oops it's a tie ")
                    else:
                            await message.channel.send(f"The results are in and option {most_voted.emoji} was the most popular with {most_voted.count-1:,} votes!")
                    self.polls.remove((message.channel.id, message.id))
                    await message.delete()
                except :
                    pass

	# @Cog.listener()
	# async def on_raw_reaction_add(self, payload):
	# 	if self.bot.ready and payload.message_id == self.reaction_message.id:
	# 		current_colours = filter(lambda r: r in self.colours.values(), payload.member.roles)
	# 		await payload.member.remove_roles(*current_colours, reason="Colour role reaction.")
	# 		await payload.member.add_roles(self.colours[payload.emoji.name], reason="Colour role reaction.")
	# 		await self.reaction_message.remove_reaction(payload.emoji, payload.member)

	# 	elif payload.message_id in (poll[1] for poll in self.polls):
	# 		message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

	# 		for reaction in message.reactions:
	# 			if (not payload.member.bot
	# 				and payload.member in await reaction.users().flatten()
	# 				and reaction.emoji != payload.emoji.name):
	# 				await message.remove_reaction(reaction.emoji, payload.member)

	# 	elif payload.emoji.name == "⭐":
	# 		message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

	# 		if not message.author.bot and payload.member.id != message.author.id:
	# 			msg_id, stars = db.record("SELECT StarMessageID, Stars FROM starboard WHERE RootMessageID = ?",
	# 									  message.id) or (None, 0)

	# 			embed = Embed(title="Starred message",
	# 						  colour=message.author.colour,
	# 						  timestamp=datetime.utcnow())

	# 			fields = [("Author", message.author.mention, False),
	# 					  ("Content", message.content or "See attachment", False),
	# 					  ("Stars", stars+1, False)]

	# 			for name, value, inline in fields:
	# 				embed.add_field(name=name, value=value, inline=inline)

	# 			if len(message.attachments):
	# 				embed.set_image(url=message.attachments[0].url)

	# 			if not stars:
	# 				star_message = await self.starboard_channel.send(embed=embed)
	# 				db.execute("INSERT INTO starboard (RootMessageID, StarMessageID) VALUES (?, ?)",
	# 						   message.id, star_message.id)

	# 			else:
	# 				star_message = await self.starboard_channel.fetch_message(msg_id)
	# 				await star_message.edit(embed=embed)
	# 				db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE RootMessageID = ?", message.id)

	# 		else:
	# 			await message.remove_reaction(payload.emoji, payload.member)


def setup(bot):
	bot.add_cog(Reactions(bot))
