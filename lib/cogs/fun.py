from random import choice, randint
from typing import Optional
import textwrap
import requests
from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown
from discord.ext.commands import CheckFailure
from discord.ext import commands
import discord
# from bs4 import BeautifulSoup
import os
import json
import asyncpraw
import aiohttp
import base64
# import arrow
import regex
import fs
import pendulum
from discord import Spotify
from io import BytesIO
import aiohttp
from discord.utils import get
import random
import re
import pyfiglet
import instagramy 
import asyncio
import tmdbsimple as tmdb
# from instascrape import Profile 

import secrets
from .. utils import lists, paginator,datpaginator,util
from ..db import db
hs_colors = {
    "aries": discord.Color.red(),
    "taurus": discord.Color.dark_teal(),
    "gemini": discord.Color.gold(),
    "cancer": discord.Color.greyple(),
    "leo": discord.Color.orange(),
    "virgo": discord.Color.green(),
    "libra": discord.Color.dark_teal(),
    "scorpio": discord.Color.dark_red(),
    "sagittarius": discord.Color.purple(),
    "capricorn": discord.Color.dark_green(),
    "aquarius": discord.Color.teal(),
    "pisces": discord.Color.blurple(),
}

class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot
		
		tmdb.API_KEY = '6324e26dd5474326e9c7803387edbc9e'

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


	@command(name = 'pickup-line', aliases = ['pickup'], description = 'pickup lines to impress e-girls')
	@custom_check()
	@cooldown(1, 30, BucketType.user)
	async def pickup(self, ctx):
		reddit  = asyncpraw.Reddit(client_id = 'Koj2wUuGJ06FNg', client_secret = "Z5CGO0EfLmQFpDJoe_rTt7FplE9rFw", user_agent = 'Tommy')
		subreddit = await reddit.subreddit("pickuplines")
		all_sub = []
	
		async for sub in subreddit.hot(limit=100):

	
			all_sub.append(sub)

		ran_sub = random.choice(all_sub)
		name = ran_sub.title
		url = ran_sub.selftext
		embed = discord.Embed(title = 'Pickup Lines', colour  = ctx.author.colour, description = f'**{name}** \n{url}')
		await ctx.send(embed = embed)
	

	


	@command(name="hello", aliases=["hi"], description = 'sirf hi hello bolta bot', usage = '+hello')
	@custom_check()
	async def say_hello(self, ctx):
		await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!")

	# @command(name="dice", aliases=["roll"])
	# @cooldown(1, 60, BucketType.user)
	# async def roll_dice(self, ctx, die_string: str):
	# 	dice, value = (int(term) for term in die_string.split("d"))

	# 	if dice <= 25:
	# 		rolls = [randint(1, value) for i in range(dice)]

	# 		await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

	# 	else:
	# 		await ctx.send("I can't roll that many dice. Please try a lower number.")

	# @command(name="slap", aliases=["hit"])
	# @cooldown(1, 30, BucketType.user)
	# async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
	# 	await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")

	# @slap_member.error
	# async def slap_member_error(self, ctx, exc):
	# 	if isinstance(exc, BadArgument):
	# 		await ctx.send("I can't find that member.")

	# @commands.command(name = 'urban')
	# async def urban(self, ctx, *, word):
	# 	'''Gets the definition of a word from Urban Dictionary.'''
	# 	async with aiohttp.ClientSession() as session:
	# 		async with session.get(f'http://api.urbandictionary.com/v0/define?term={word}') as resp:
	# 			r = await resp.json()
	# 			color = discord.Color(value=0x00ff00)
	# 			# 
	# 			lol = []
	# 			for x in r['list']:
	# 				lol.append(f"{x['definition']} \n\n*{x['example']}")
	# 				ud = datpaginator.DatPaginator(ctx, entries=lol, per_page=1)
					# await ud.run()

	
	@command(name = 'pp', description = 'Says the size of your penis', usage = '+pp')
	@custom_check()
	async def penis(self, ctx, user:discord.Member = None):

		
		user = user or ctx.author
		try:
			responses = ['Your penis: 8=D',
			            'Your penis: 8==D',
						'Your penis: 8===D',
						'Your penis: 8====D',
						'Your penis: 8=====D',
						'Your penis: 8======D',
						'Your penis: 8=======D',
						'Your penis: 8========D',
						'Your penis: 8=========D',
						'Your penis: 8==========D',
						'Your penis: 8============D',
						'Your penis: 8=============================D ']#new update 
			embed = discord.Embed(title=f"{user.name} penis size", description=f'{random.choice(responses)}', color=random.randint(0x000000, 0xffffff))
			await ctx.channel.send(embed=embed)
		except Exception as error:
			raise(error)


	@command(name = 'trump', description = "Ask Trump your own question.", usage = '+trump <question>')
	@custom_check()
	@cooldown(2, 10, BucketType.user)
	@commands.guild_only()
	async def asktrump(self, ctx, *, question):
		async with aiohttp.ClientSession() as cs:
			async with cs.get(f"https://api.whatdoestrumpthink.com/api/v1/quotes/personalized?q={question}") as res:
		
		

				resp = await res.json()
				em = discord.Embed(color=ctx.author.color, title="What did Trump say?")
				em.description = f"**You:** {question}\n\n**Trump:** {resp['message']}"
				em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
				await ctx.send(embed=em)

	@command(name= 'hack', pass_context=True, description = 'Hack somebody', usage = '+hack <user>')
	@custom_check()
	@commands.guild_only()
	@cooldown(3, 30, BucketType.user)
	async def hack(self, ctx, member:discord.Member = None):
	
		if not member:
			await ctx.send("Please mention a member")
			return
		passwords=['chorrachamaaroka','maigayhu','mujhebavaseerhai','iloveyoupooja','patanjalidantkaanti','showbobsandvegana','imissyoupinky','maitharkihu','maipedohu','saxwith69others','jaishreeram','allahhuakbhar','nitrodedokoi', 'padhkyarhamc', 'edharaatujhepassbtayu', 'desichora69', 'sapnachaudharyhotpics', 'serveradminhotpics','savitabhabhi','miabhabhi','devarbhabhi']
		fakeips=['154.2345.24.743','255.255. 255.0','356.653.56','101.12.8.6053','255.255. 255.0']
		embed = discord.Embed(title=f"**Hacking: {member}** 0%...", color=random.randint(0x000000, 0xffffff))
		m = await ctx.send(embed=embed)
		await asyncio.sleep(3)
		
		embed = discord.Embed(title=f"**Hacking: {member}** 19%",description = "Accessing Discord Files... [▓▓    ]", color=random.randint(0x000000, 0xffffff))
		await m.edit(embed=embed)
		await asyncio.sleep(2)
		embed = discord.Embed(title=f"**Hacking: {member}** 34%",description = "Accessing Discord Files... [▓▓▓   ]" , color=random.randint(0x000000, 0xffffff))
		await m.edit(embed=embed)
		await asyncio.sleep(2)
		embed = discord.Embed(title=f"**Hacking: {member}** 55%",description= "Accessing Discord Files... [▓▓▓▓▓ ]" , color=random.randint(0x000000, 0xffffff))
		await m.edit(embed=embed)
		await asyncio.sleep(2)
		embed = discord.Embed(title=f"**Hacking: {member}** 67%",description = "Accessing Discord Files COMPLETE! [▓▓▓▓▓▓]",  color=random.randint(0x000000, 0xffffff))
		await m.edit(embed=embed)
		await asyncio.sleep(2)
		embed = discord.Embed(title=f"**Hacking: {member}** 84%",description = "Retrieving Login Info... [▓▓▓    ]", color=random.randint(0x000000, 0xffffff))
		await m.edit(embed=embed)
		await asyncio.sleep(2)
		embed = discord.Embed(title=f"**Hacking: {member}** 99%",description = "Retrieving Login Info... [▓▓▓▓▓ ]", color=random.randint(0x000000, 0xffffff))
		await m.edit(embed=embed)
		await asyncio.sleep(2)
		embed = discord.Embed(title=f"**Hacking: {member}** 100%",description = "Retrieving Login Info... [▓▓▓▓▓▓ ]", color=random.randint(0x000000, 0xffffff))
		await m.edit(embed=embed)
		await asyncio.sleep(2)
		embed = discord.Embed(title=f"{member} info ", description=f"*Email `{member}@gmail.com` Password `{random.choice(passwords)}`  IP `{random.choice(fakeips)}`*", color=random.randint(0x000000, 0xffffff))
		embed.set_footer(text="You've totally been hacked 😏")
		await m.edit(embed=embed)
		await asyncio.sleep(3)


	# @command(name = 'emojify')
	# async def emojify(self, ctx, *, text: str):
	# 	"""Turns your text into emojis!"""
	# 	try:
	# 		await ctx.message.delete()
	# 	except discord.Forbidden:
	# 		pass
	# 	to_send = ""
	# 	for char in text:
	# 		if char == " ":
	# 			to_send += " "
	# 		elif char.lower() in 'qwertyuiopasdfghjklzxcvbnm':
	# 			to_send += f":regional_indicator_{char.lower()}:  "
	# 		elif char in '1234567890':
	# 			numbers = {
	# 				"1": "one",
	# 				"2": "two",
	# 				"3": "three",
	# 				"4": "four",
	# 				"5": "five",
	# 				"6": "six",
	# 				"7": "seven",
	# 				"8": "eight",
	# 				"9": "nine",
	# 				"0": "zero"
	# 			}
	# 			to_send += f":{numbers[char]}: "
	# 		else:
	# 			return await ctx.send("Characters must be either a letter or number. Anything else is unsupported.")
	# 		if len(to_send) > 2000:
	# 			return await ctx.send("Emoji is too large to fit in a message!")
	# 		await ctx.send(to_send)

	async def clean_text(self,ctx, text):
		"""Removes any mentions from the text."""
		return await commands.clean_content().convert(ctx, text)


	@command(name = 'say', description = 'Sends the message you wrote', usage = '+say <message>')
	@custom_check()
	async def echo(self,ctx, *,message):
		try:
			await ctx.message.delete()
		except discord.Forbidden:
			pass
		x = message
		res  = await self.clean_text(ctx,x)
		await ctx.send(res)


	@commands.group(name = 'base64',invoke_without_command=True, description ='Encode and decode base64 Text time to annoy your friends with encoded text.' )
	@custom_check()
	async def base64(self, ctx):
		
		await ctx.send("Base64 Encode/Decode\nCommands: encode: Encode text\ndecode: Decode text")
		
	@base64.command(name = 'encode', description = 'Encode base64 text', usage = '+base64 encode <msg>')
	@custom_check()
	async def encode(self, ctx, *, msg: str):
		await ctx.message.delete()
		
		try:
			x = base64.b64encode(msg.encode("ascii")).decode("ascii")
			if len(x) > 1950: return await ctx.send("Results too long.")
			res = await self.clean_text(ctx, x)
			
			await ctx.send(f"```{res}```") 
		except Exception as e:
			await ctx.send("Something went wrong.")
			
	@base64.command(name = 'decode', description = 'decode base64 text', usage = '+base64 decode <msg>')
	@custom_check()
	async def decode(self, ctx, *, msg: str):
		
	
		try:
			
			x = base64.b64decode(msg)
			if len(x) > 1950: return await ctx.send("Results too long.")
			res = await self.clean_text(ctx, x.decode('ascii'))

			await ctx.send(f"```{res}```")
		except Exception as e:
			await ctx.send("Invalid Base64 Text")
			


	
	@command(name="fact", description  =  'tells a random fact about some animals', usage = '+fact <animal>')
	@custom_check()
	@cooldown(3, 10, BucketType.guild)
	async def animal_fact(self, ctx, animal: str):
		if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
			fact_url = f"https://some-random-api.ml/facts/{animal}"
			image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]

				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					embed = Embed(title=f"{animal.title()} fact",
								  description=data["fact"],
								  colour=ctx.author.colour)
					if image_link is not None:
						embed.set_image(url=image_link)
					await ctx.send(embed=embed)

				else:
					await ctx.send(f"API returned a {response.status} status.")

		else:
			await ctx.send("Here is the list of animals :- \n `dog, cat, panda, fox, bird, koala`")


	@command(name = 'coinflip', aliases = ['flip'], description = 'flips a coin', usage = '+flip')
	@custom_check()
	
	async def coinflip(self, ctx):

		
		coinsides = ['Heads', 'Tails']
		msg = await ctx.send('heads or tails ?')
		await msg.add_reaction("🇭")
		await msg.add_reaction("🇹")
		def checkreact(reaction, user):
			if user == ctx.author and str(reaction.emoji) in ['🇭', '🇹'] :
				return True
			return False
			  
		try:
			reaction,user = await self.bot.wait_for('reaction_add', timeout=20.0, check=checkreact)
			
			x = random.choice(coinsides)
			if x == 'Heads' and str(reaction.emoji) == "🇭" :
				await ctx.send(f"**{ctx.author.name}** guessed it right, it's a **{x}**!")
			elif x =="Tails" and str(reaction.emoji) == "🇹" :
				await ctx.send(f"**{ctx.author.name}** guessed it right, it's a **{x}**!")
			else :
				await ctx.send(f"**{ctx.author.name}** guessed it wrong, it's a **{x}**!")
		except asyncio.TimeoutError:
			await msg.delete()
			



	@command(name = 'ascii', description = 'ascii text banners', usage = '+ascii <text>')
	@custom_check()
	@cooldown(3, 30, BucketType.user)

	async def ascii(self, ctx, *, text :str):
		
		ascii_banner = pyfiglet.figlet_format(f'{text}')

		
		await ctx.send(f"```{ascii_banner}```")


	@command(name = 'reverse', description = 'reverses text', usage = '+reverse <text>')
	@custom_check()
	async def reverse(self, ctx, *, text: str):
		t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
		await ctx.send(f"🔁 {t_rev}")
  #   
	# @command(name="helpp")
	# async def help(self, ctx, member: discord.Member = None):
	# 	await ctx.message.delete()
	# 	prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)

	# 	member = ctx.author if not member else member
	# 	embed = discord.Embed(title=f'All Commands (Default prefix is {prefix})')
	# 	embed.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n♣️ __**General Commands**__ {Commands showing things such as serverinfo, userinfo, etc.}\n\n🤡 __**Fun Commands**__ {Variety of Different Fun Commands}\n\n🎮 __**Minecraft Commands**__ {Minecraft Related Fun Commands}\n\n📑 __**Application Commands**__ {Commands to apply for something}\n\n📫 __**Suggestion Commands**__ {Commands to leave a Suggestion}\n\n🔐 __**Moderation Commands**__ {Commands to Moderate the server (Mods and Admins Only)}\n\n🔗 __**Misc Commands**__ {Misc Commands Only Mods and Admins can Use}", inline=False)
	# 	embed.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
	# 	m = await ctx.send(embed=embed)
	# 	await m.edit(embed=embed)
	# 	await m.add_reaction('📖')
	# 	await m.add_reaction('♣️')
	# 	await m.add_reaction('🤡')
	# 	await m.add_reaction('🎮')
	# 	await m.add_reaction('📑')
	# 	await m.add_reaction('📫')
	# 	await m.add_reaction('🔐')
	# 	await m.add_reaction('🔗')
	# 	def checkreact(reaction, user):
	# 		return user == ctx.author and str(reaction.emoji) in ['📖', '♣️', '🤡', '🎮', '📑', '📫', '🔐', '🔗']
	# 	while True:
	# 		try:
	# 			reaction, user = await self.bot.wait_for('reaction_add', timeout=45.0, check=checkreact)
			
		
	# 			if str(reaction.emoji) == '♣️':
	# 				await m.remove_reaction('♣️', member)
	# 				embed1 = discord.Embed(title=f'General Commands (Default prefix is "{prefix}")', color=discord.Color.darker_grey())
	# 				embed1.add_field(name="__**Commands:**__", value="_*binfo*_ - {Shows info about the Bot}\n\n_*sinfo*_ - {Shows info about the server}\n\n_*uinfo*_ - {Shows info about a user}\n\n_*avatar*_ - {Shows the avatar of a user}\n\n_*ping*_ - {Runs a connection test to Discord}", inline=False)
	# 				await m.edit(embed=embed1)
	# 			elif str(reaction.emoji) == '🤡':
	# 				await m.remove_reaction('🤡', member)
	# 				embed2 = discord.Embed(title=f'Fun Commands (Default prefix is "{prefix}")', color=discord.Color.dark_blue())
	# 				embed2.add_field(name="__**Commands:**__", value="_*8ball*_ - {Ask a question and get an answer}\n\n_*letschat(chat)*_ - {Have a convo with the Bot}\n\n_*fact*_ - {Get a random fact}\n\n_*insta*_ - {Get info on an Insta Account}\n\n_*embed*_ - {Make your message a fancy embed}\n\n_*bottles*_(!bottles 7 water) - {x bottles of x on the wall}\n\n_*add*_(4+4) - {Add two numbers together}\n\n_*hug*_ - {Hug someone}\n\n_*punch*_ - {Punch somebody}\n\n_*slap*_ - {Slap someone}\n\n_*iq*_ - {Says your IQ}\n\n_*gay*_ - {Shows how gay you are}\n\n_*penis*_ - {Says your penis size}\n\n_*thot*_ - {Says how much of a thot you are}\n\n_*hack_* - {Hack somebody}\n\n_*coinflip*_ - {Flip a coin}\n\n_*slots*_ - {Will you win the slot machine?}", inline=False)
	# 				await m.edit(embed=embed2)
	# 			elif str(reaction.emoji) == '🎮':
	# 				await m.remove_reaction('🎮', member)
	# 				embed3 = discord.Embed(title=f'Minecraft Commands (Default prefix is "{prefix}")', color=0xa0722a)
	# 				embed3.add_field(name="__**Commands:**__ ", value="_*mcping(!mcping play.hypixel.net)*_ - {Shows stats of a Minecraft server}\n\n_*skin*_ - {Get the skin of another Player}\n\n_*uuid*_ - {Get the UUID of another Player}\n\n_*getplayer*_ - {Get a Player username with their UUID]\n\n_*mcsales*_ - {Shows the sales of Minecraft}\n\n_*buildidea*_ - {Get a random build idea}\n\n_*colorcodes*_ - {Get the colorcodes of Minecraft Text}", inline=False)
	# 				await m.edit(embed=embed3)
	# 			elif str(reaction.emoji) == '📑':
	# 				await m.remove_reaction('📑', member)
	# 				embed4 = discord.Embed(title=f'Application Commands (Default prefix is "{prefix}")', color=0x223ba3)
	# 				embed4.add_field(name="__**Commands:**__", value="_*applymod*_ - {Apply for Moderator}", inline=False)
	# 				await m.edit(embed=embed4)
					
	# 			elif str(reaction.emoji) == '📫':
	# 				await m.remove_reaction('📫', member)
	# 				embed5 = discord.Embed(title=f'Suggestion Commands (Default prefix is "{prefix}")', color=0x223ba3)
	# 				embed5.add_field(name="__**Commands:**__", value="_*suggest*_ - {Leave a suggestion}", inline=False)
	# 				await m.edit(embed=embed5)
	# 			elif str(reaction.emoji) == '🔐':
	# 				await m.remove_reaction('🔐', member)
	# 				embed6 = discord.Embed(title=f'Moderation Commands(Mods and Admins **Only**) (Default prefix is "{prefix}")', color=0x9a9a23)
	# 				embed6.add_field(name="__**Commands:**__", value="_*kick*_ - {Kicks a User}\n\n_*ban*_ - {Bans a User}\n\n_*unban*_(!unban User name#1234) - {Unbans a User}\n\n_*mute*_ - {Mutes a user from texting for a specified amount of time}\n\n_*unmute*_ - {Manually Unmutes a User}\n\n_*purge(prune, clean)*_ - {Deletes a specified amount of messages}", inline=False)
	# 				await m.edit(embed=embed6)
					
	# 			elif str(reaction.emoji) == '🔗':
	# 				await m.remove_reaction('🔗', member)
	# 				embed7 = discord.Embed(title=f'Misc Commands(Mods and Admins **Only**) (Default prefix is "{prefix}")', color=0x62239a)
	# 				embed7.add_field(name="__**Commands:**__", value="_*invite(!invite #channelname)*_ - {Creates an invite for a specific channel}\n\n_*announce*_ - {Bot will say whatever the User says}\n\n_*dm*_ - {DM a User a custom message}\n\n_*poll*_ - {Creates a Poll}\n\n_*quickpoll*_ - {Creates a poll quickly}\n\n_*restart(shutdown)*_ - {Restart/Shutdown the Bot (Owner **Only**)}", inline=False)
	# 				await m.edit(embed=embed7)
	# 			else:
	# 				if str(reaction.emoji) == '📖':
	# 					await m.remove_reaction('📖', member)
	# 					embed0 = discord.Embed(title=f'All Commands (Default prefix is "{prefix}")')
	# 					embed0.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n♣️ __**General Commands**__ {Commands showing things such as serverinfo, userinfo, etc.}\n\n🤡 __**Fun Commands**__ {Variety of Different Fun Commands}\n\n🎮 __**Minecraft Commands**__ {Minecraft Related Fun Commands}\n\n📑 __**Application Commands**__ {Commands to apply for something}\n\n📫 __**Suggestion Commands**__ {Commands to leave a Suggestion}\n\n🔐 __**Moderation Commands**__ {Commands to Moderate the server (Mods and Admins Only)}\n\n🔗 __**Misc Commands**__ {Misc Commands Only Mods and Admins can Use}", inline=False)
	# 					embed0.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
	# 					await m.edit(embed=embed0)

	# 		except asyncio.TimeoutError:
	# 			await m.delete()
	# 			break

	# @command(name = 'quote' , aliases=['q','quotes'], description  = 'Random quotes')
	# @custom_check()
	# @cooldown(1, 10, BucketType.user)
	# async def quote(self,ctx):
	# 	async with aiohttp.ClientSession() as cs:
	# 		async with cs.get('https://zenquotes.io/api/random') as res:
	# 			data = await res.json()

	# 			embed = discord.Embed(colour=ctx.author.color, description= " " + data[0]['q'] + " " , timestamp=ctx.message.created_at)
	# 			embed.set_author(name=data[0]['a'])
	# 			await ctx.send(embed=embed)


	# @command(name = 'quote' , aliases=['q','quotes'], description  = 'Random quotes')
	# @custom_check()
	# @cooldown(3, 30, BucketType.user)
	
	# async def quote(self,ctx):
		

		
	# 	async with aiohttp.ClientSession() as s:
	# 		async with s.get("https://api.quotable.io/random") as r:
	# 			data = await r.json()
 
	# 	embed = discord.Embed(colour=ctx.author.color, description= " " + data['content'] + " " , timestamp=ctx.message.created_at)
	# 	embed.set_author(name=data['author'])
	# 	await ctx.send(embed=embed)


	def get_quote(self):
		response = requests.get("https://zenquotes.io/api/random")
		json_data = json.loads(response.text)
		
		return(json_data)  


	@command(name = 'quote' , aliases=['q','quotes'], description  = 'Random quotes')
	@custom_check()
	@cooldown(1, 10, BucketType.user)
	async def quote(self,ctx):
		#  quote = json_data[0]['q'] + " -" + json_data[0]['a']
		quote = self.get_quote()


		embed = discord.Embed(colour=ctx.author.color, description= " " + quote[0]['q'] + " " , timestamp=ctx.message.created_at)
		embed.set_author(name=quote[0]['a'])
		await ctx.send(embed=embed)
		
		

		
		
				
 
				# embed = discord.Embed(colour=ctx.author.color, description= " " + data['content'] + " " , timestamp=ctx.message.created_at)
				# embed.set_author(name=data['author'])
				# await ctx.send(embed=embed)
				
	# @command(name = 'spotify', description  = 'shows detail of a song user is listening to', usage = '+spotify <user>')
	# @custom_check()
	# @cooldown(1, 10, BucketType.user)
	# async def spotify(self, ctx, user: discord.Member=None):
	# 	user = user or ctx.author
	# 	for activity in user.activities:
	# 		# try:
			

	# 		# except:
	# 		if activity.type == discord.ActivityType.listening and not user.bot and activity.name  == 'Spotify':

	# 			em = Embed(color=discord.Color.dark_green())
	# 			em.set_author(name  = 'Spotify', icon_url  = "https://cdn.discordapp.com/attachments/714910677029879898/745727179274321941/spotify2.png")
	# 			em.set_thumbnail(url=activity.album_cover_url)
	# 			em.add_field(name = f"**Song Name**:" , value =  f'{activity.title}', inline = True)
				
	# 			em.add_field(name = f"**Song Artist**:" , value =  f'{activity.artist}', inline = True)
	# 			em.add_field(name = "**Song Album**:" , value = f'{activity.album}', inline = False)
	# 			em.add_field(name = f"**Song Duration**:" , value =  f"{pendulum.duration(seconds=activity.duration.total_seconds()).in_words(locale='en')}", inline = True)
	# 			em.add_field(name  = f'**Song url :**', value  = f"https://open.spotify.com/track/%7B{activity.track_id}%7D", inline = False)
	# 			await ctx.send(embed=em)
	# 			break

	# 		# elif isinstance(activity, Spotify):
	# 		# 	em = Embed(color=discord.Color.dark_green())
	# 		# 	em.set_author(name  = 'Spotify', icon_url  = "https://cdn.discordapp.com/attachments/714910677029879898/745727179274321941/spotify2.png")
	# 		# 	em.set_thumbnail(url=activity.album_cover_url)
	# 		# 	em.add_field(name = f"**Song Name**:" , value =  f'{activity.title}', inline = True)
				
	# 		# 	em.add_field(name = f"**Song Artist**:" , value =  f'{activity.artist}', inline = True)
	# 		# 	em.add_field(name = "**Song Album**:" , value = f'{activity.album}', inline = False)
	# 		# 	em.add_field(name = f"**Song Duration**:" , value =  f"{pendulum.duration(seconds=activity.duration.total_seconds()).in_words(locale='en')}", inline = True)
	# 		# 	em.add_field(name  = f'**Song url :**', value  = f"https://open.spotify.com/track/%7B{activity.track_id}%7D", inline = False)
	# 		# 	return await ctx.send(embed=em)


	# 	else:
	# 		embed = discord.Embed(description=f"{user.name} isn't listening to Spotify right now", color=discord.Color.dark_red())
	# 		await ctx.send(embed=embed)



	@commands.command(name = 'choose',description = 'Choose from given options. separate choices with "or"')
	async def choose(self, ctx, *, choices):


		"""+choose <a> or <b> or ... or <thing_n>"""
		choices = choices.split(" or ")
		if len(choices) < 2:
			return await ctx.send(
				"Give me at least 2 options to choose from! (separate options with `or`)"
			)
		choice = random.choice(choices).strip()
		await ctx.send(f"I choose **{choice}**")





	@commands.group(name  = "horoscope", description  ="Get your daily horoscope.",  aliases=["hs"])
	@custom_check()
	@commands.cooldown(1,10,commands.BucketType.user)
	async def horoscope(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send_help(str(ctx.command))

	@horoscope.command(name="today", description  = "Get today's horoscope.", usage = "+hs today")
	async def horoscope_today(self, ctx):

		await self.send_hs(ctx, "today")

			

	@horoscope.command(name="tomorrow", description  = "Get tomorrow's horoscope.", usage = "+hs tomorrow")
	async def horoscope_tomorrow(self, ctx):

		await self.send_hs(ctx, "tomorrow")

	@horoscope.command(name="yesterday",description = "Get yesterday's horoscope.", usage = '+hs yesterday')
	async def horoscope_yesterday(self, ctx):
		
		await self.send_hs(ctx, "yesterday")

	async def send_hs(self, ctx, day):
		userdata = db.record('SELECT * FROM horoscope WHERE user_id = ?',ctx.author.id)
		if userdata is None or userdata[1] is None:
			return await ctx.send(
				"Please save your sunsign using `>horoscope set <sign>`\n"
				"use `>horoscope list` if you don't know which one you are."
			)
		sign = userdata[1]
		params = {"sign": sign, "day": day}
		async with aiohttp.ClientSession() as session:
			async with session.post(
				"https://aztro.sameerkumar.website/", params=params
			) as response:
				data = await response.json()

		content = discord.Embed(color=hs_colors[sign])
		content.title = f"{sign.capitalize()} - {data['current_date']}"
		content.description = data["description"]

		content.add_field(name="Mood", value=data["mood"], inline=True)
		content.add_field(name="Compatibility", value=data["compatibility"], inline=True)
		content.add_field(name="Color", value=data["color"], inline=True)
		content.add_field(name="Lucky number", value=data["lucky_number"], inline=True)
		content.add_field(name="Lucky time", value=data["lucky_time"], inline=True)
		content.add_field(name="Date range", value=data["date_range"], inline=True)

		await ctx.send(embed=content)

	@horoscope.command(name = 'set', description  = "Set your sunsign.", usage = "+hs set <sign>")
	async def set(self, ctx, sign):
		
		hs = [
			"aries",
			"taurus",
			"gemini",
			"cancer",
			"leo",
			"virgo",
			"libra",
			"scorpio",
			"sagittarius",
			"capricorn",
			"aquarius",
			"pisces",
		]
		sign = sign.lower()
		if sign not in hs:
			return await ctx.send(
				f"`{sign}` is not a valid sunsign! Use `>horoscope list` for a list of sunsigns."
			)

		try:
			db.execute('INSERT INTO horoscope (sunsign,user_id) VALUES (?,?)', sign, ctx.author.id)
			await ctx.send(f"Sunsign saved as `{sign}`")
			
		except:
			db.execute('UPDATE horoscope SET sunsign = ? WHERE user_id = ?', sign,ctx.author.id)
			await ctx.send(f"Sunsign saved as `{sign}`")
			
		

	@horoscope.command(name = 'list', description  ="Get list of all sunsigns.")
	async def __list(self, ctx):
	
		sign_list = [
			"`(Mar 21-Apr 19)` **Aries**",
			"`(Apr 20-May 20)` **Taurus**",
			"`(May 21-Jun 20)` **Gemini**",
			"`(Jun 21-Jul 22)` **Cancer**",
			"`(Jul 23-Aug 22)` **Leo**",
			"`(Aug 23-Sep 22)` **Virgo**",
			"`(Sep 23-Oct 22)` **Libra**",
			"`(Oct 23-Nov 21)` **Scorpio**",
			"`(Nov 22-Dec 21)` **Sagittarius**",
			"`(Dec 22-Jan 19)` **Capricorn**",
			"`(Jan 20-Feb 18)` **Aquarius**",
			"`(Feb 19-Mar 20)` **Pisces**",
		]
		content = discord.Embed(color=discord.Color.gold())
		content.title = "Sunsign list"
		content.description = "\n".join(sign_list)
		return await ctx.send(embed=content)


			

				
				
				
				
				
			
					
			
		
			
	@command(name = "mimic", description = 'Say something like someone else')
	@custom_check()
	@cooldown(3, 20, BucketType.user)

	async def mimic(self, ctx, user: discord.Member, *, message: str):
	
		try:
			await ctx.message.delete()
		except:
			pass
		img = user.avatar_url_as(format="png", size=1024)
		async with aiohttp.ClientSession() as cs:
			async with cs.get(str(img)) as res:
				byte = await res.read()
		
				try:
					webhook = await ctx.channel.create_webhook(name=user.display_name, avatar=byte)
				except:
					return await ctx.send("I don't have enough permissions! I need the **Manage Webhooks** permission.")
				# message = await Utils.clean_text(ctx, message)
				x = message
				res  = await self.clean_text(ctx,x)
			
				await webhook.send(res)
				await webhook.delete()



	# @command(name = 'testhelp')
	# async def testhelp(self, ctx, *, command: str = None):
	# 	"""HELP! Not this one, tho..."""
	# 	if command is None:
	# 		color = 0x00ff00
	# 		em = discord.Embed(color=color, title='recolty help')
	# 		lol = []
	# 		commands = []
	# 		pgnumber = 0
	# 		for x in self.bot.cogs:
	# 			lol.append(x)
	# 		for x in lol:
	# 			cmdlist = self.bot.get_cog_commands(x)
	# 			if x == lol[pgnumber]:
	# 				commands.append(cmdlist)
	# 		for x in commands:
	# 			em.description += f"**{x.name}**\n{x.short_doc}"
	# 	em.set_footer(text="Pulling your hair out? Use the '?' to GET HELP!")
	# 	msg = await ctx.send(embed=em)
	# 	try:
	# 		await msg.add_reaction("\U000021a9")  # Fast forward left
	# 		await msg.add_reaction("\U00002b05")  # Turn left
	# 		await msg.add_reaction("\U000027a1")  # Turn right
	# 		await msg.add_reaction("\U000021aa")  # Fast forward right
	# 		await msg.add_reaction("\U0001f6d1")  # Stop
	# 		await msg.add_reaction("\U00002049")  # Info
	# 	except discord.Forbidden:
	# 		return await ctx.send("Uh-oh! I don't have the 'Add Reactions' permission, so I can't paginate...")
	# 	while True:
	# 		reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction: x.channel == ctx.channel and x.author == ctx.author and user == ctx.author, timeout=120.0)
	# 		if reaction.emoji == '⬅':
	# 			try:
	# 				await msg.remove_reaction("\U00002b05", ctx.author)
	# 			except:
	# 				pass
	# 			pgnumber -= 1
	# 			em.description = ''
	# 			for x in commands:
	# 				em.description += f"**{x.name}**\n{x.short_doc}"
	# 			await msg.edit(embed=em)
	# 		elif reaction.emoji == '➡':
	# 			try:
	# 				await msg.remove_reaction("\U000027a1", ctx.author)
	# 			except:
	# 				pass
	# 			pgnumber += 1
	# 			em.description = ''
	# 			for x in commands:
	# 				em.description += f"**{x.name}**\n{x.short_doc}"
	# 			await msg.edit(embed=em)
	# 		elif reaction.emoji == 'ℹ':
	# 			try:
	# 				await msg.remove_reaction("\U00002139", ctx.author)
	# 			except:
	# 				pass
	# 			em.description = textwrap.dedent("""
    #             **What do these buttons do?**
                
    #             :arrow_left: Turns left one page.
    #             :arrow_right: Turns right one page.
    #             :information_source: Shows this message.
    #             """)
	# 			em.set_footer(text="This will revert back in 15 seconds.")
	# 			await msg.edit(embed=em)
	# 			await asyncio.sleep(15)
	# 			await msg.edit(embed=msg)
	# 		elif reaction.emoji == '⏹':
	# 			await msg.delete()
	# 			break



	@command(name = 'define', description = 'tells definition of a word', usage = '+define <word>')
	@custom_check()
	async def define(self,ctx, *, word):
		baseurl = "https://api.urbandictionary.com/v0/define"
		async with aiohttp.ClientSession() as session:
			async with session.get(baseurl, params={"term": word}) as response:
				data = await response.json()
				

		pages = []
		if data["list"]:
			for entry in data["list"]:
				definition = entry["definition"]
				example = entry["example"]
				timestamp = entry["written_on"]
				content = discord.Embed(colour=ctx.author.colour)
				content.description = f"{definition}"

				if not example == "":
					content.add_field(name="Example", value=f"`{example}`")

				content.set_footer(
					text=f"{entry.get('thumbs_up')} 👍 {entry.get('thumbs_down')} 👎"
				)
				content.timestamp = ctx.message.created_at
				content.set_author(
					name=f"Definition of '{entry['word']}'",
					icon_url= ctx.author.avatar_url,
					url=entry.get("permalink"),
				)
				pages.append(content)

			await util.page_switcher(ctx, pages)

		else:
			await ctx.send(f"No definitions found for `{word}`")




	# @command(name = 'insta')
	# async def insta(self, ctx, username):
	# 	try:
	
	# 		user = instagramy.InstagramUser(username) 
	# 		embed = discord.Embed(title  = f" User's Insta details", color = ctx.author.color)
	# 		embed.add_field(name  = 'User Name', value = user.username, inline = True)
	# 		embed.add_field(name = 'bio', value = user.biography, inline = False)
	# 		embed.add_field(name = 'followers', value = user.number_of_followers, inline = True)
	# 		embed.add_field(name = 'following', value = user.number_of_followings, inline = True)
	# 		embed.add_field(name = 'Total Posts', value = user.number_of_posts, inline = True)
	# 		if user.is_private is True:

	# 			embed.add_field(name  = 'account', value = 'Private', inline= True)

	# 		else: 
	# 			embed.add_field(name  = 'account', value = 'Public', inline= True)
	# 		embed.add_field(name= 'verified ?', value = user.is_verified, inline = True)
	# 		embed.set_thumbnail(url = user.profile_picture_url)
	# 		await ctx.send(embed = embed)
	# 	except instagramy.core.exceptions.UsernameNotFound:
	# 		await ctx.send('invalid username')

		
			




	



	


	@command(name = 'movie', description  = 'gives info about a movie', usage = '+movie <name>')
	@custom_check()
	async def movie(self, ctx , *,movie):
		try :
			
			search = tmdb.Search()
			response = search.movie(query = movie)

			details = [i for i in search.results]
			
			total = details[0]
			print(total)

			name = total['title']
			rating = total['vote_average']
			overview = total['overview']
			release = total['release_date']
			lang = total['original_language']
			adult = total['adult']
			votes = total['vote_count']
			popularity = total['popularity']
			
			poster = total['poster_path']
			thumb = f"http://image.tmdb.org/t/p/w500{poster}"
			
			image = total['backdrop_path']
			img = f"http://image.tmdb.org/t/p/w500{image}"
			
			embed = discord.Embed()
			embed.add_field(name = "Name:" , value = name)
			embed.add_field(name = "Overview:" , value = overview)
			embed.add_field(name = "Release Date:" , value = release)
			embed.add_field(name = "Language:" , value = lang)
			embed.add_field(name = "Adult:" , value = adult)
			embed.add_field(name = "Rating:" , value = rating)
			embed.add_field(name = "Total votes:" , value = votes)
			embed.add_field(name = "Popularity:" , value = popularity)
			
			embed.set_thumbnail(url=thumb)
			embed.set_image(url=img)
			
			await ctx.send(embed=embed)
		except :
			await ctx.send('enter a valid movie name')
		
				
				


	@command(name = 'colour', aliases = ['color'], description  = 'View the colour HEX details', usage = '+colour <hex>')
	@custom_check()
	@cooldown(3, 30, BucketType.user)
	async def colour(self, ctx, colour: str = None):
		
		async with ctx.channel.typing():
			# if not permissions.can_embed(ctx):
			# 	return await ctx.send("I can't embed in this channel ;-;")
				
			if colour == None:
				colour = "%06x" % random.randint(0, 0xFFFFFF)
				
			if colour[:1] == "#":
				colour = colour[1:]
				
			if not re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', colour):
				return await ctx.send("You're only allowed to enter HEX (0-9 & A-F)")
				
			try:
				# r = await http.get(f"https://api.alexflipnote.dev/colour/{colour}", res_method="json", no_cache=True)
				async with aiohttp.ClientSession() as cs:
					async with cs.get(f"https://api.alexflipnote.dev/colour/{colour}", headers={"Authorization": "R91VWGwSlMh7hsuvsSu2xoKy60VHuUXnm-cIA-D2"}) as res:
						r = await res.json() 
						embed = discord.Embed(colour=r["int"])#
						embed.set_thumbnail(url=r["image"])
						embed.set_image(url=r["image_gradient"])
						embed.add_field(name="HEX", value=r['hex'], inline=True)
						embed.add_field(name="RGB", value=r['rgb'], inline=True)
						embed.add_field(name="Int", value=r['int'], inline=True)
						embed.add_field(name="Brightness", value=r['brightness'], inline=True)
						await ctx.send(embed=embed, content=f"{ctx.invoked_with.title()} name: **{r['name']}**")
			except aiohttp.ClientConnectorError:
				return await ctx.send("The API seems to be down...")
			except aiohttp.ContentTypeError:
				return await ctx.send("The API returned an error or didn't return JSON...")
				
			


	@command(name = 'password', aliases = ['pass'], description = 'generates a random pass')
	@custom_check()
	async def password(self, ctx, nbytes:int =  8):
		if nbytes not in range(3, 1401):
			return await ctx.send("I only accept any numbers between 3-1400")
		if hasattr(ctx, 'guild') and ctx.guild is not None:
			await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
			
		nbytes = int(nbytes/1.3)
		await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

	@command(name = 'rate', description = 'Rates what you desire', usage = '+rate <user>')
	@custom_check()
	async def rate(self, ctx, *, thing: commands.clean_content):
		
		rate_amount = random.uniform(0.0, 10.0)
		await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount)} / 10**")

	@command(name = 'howhot', description  = 'tells how hot are you', usage = '+howhot <user>')
	@custom_check()
	async def hotcalc(self, ctx, *, user: discord.Member = None):
		
		user = user or ctx.author
		
		r = random.randint(1, 100)
		
		hot = r / 1.17
		emoji = "💔"
		if hot > 25:
			emoji = "❤"
		if hot > 50:
			emoji = "💖"
		if hot > 75:
			emoji = "💞"
			
		await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

	@command(name = 'slot', description  = 'Roll the slot machine')
	@custom_check()
	async def slot(self, ctx):
		
		emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
		a = random.choice(emojis)
		b = random.choice(emojis)
		c = random.choice(emojis)
		slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"
		if (a == b == c):
			await ctx.send(f"{slotmachine} All matching, you won! 🎉")
		elif (a == b) or (a == c) or (b == c):
			await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
		else:
			await ctx.send(f"{slotmachine} No match, you lost 😢")

	@command(name = 'beer', description  = 'Give someone a beer! 🍻 ')
	@custom_check()
	async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
		
		if not user or user.id == ctx.author.id:
			return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
		if user.id == self.bot.user.id:
			return await ctx.send("*drinks beer with you* 🍻")
		if user.bot:
			return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")
		beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
		beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
		msg = await ctx.send(beer_offer)
		
		def reaction_check(m):
			if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
				return True
			return False
			
		try:
			await msg.add_reaction("🍻")
			await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
			await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
		except asyncio.TimeoutError:
			await msg.delete()
			await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
		except discord.Forbidden:
			# Yeah so, bot doesn't have reaction permission, drop the "offer" word
			beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
			beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
			await msg.edit(content=beer_offer)


	@command(name = '8b', description  = 'Consult 8ball to receive an answer', usage = '+8b <question>')
	@custom_check()
	async def eightball(self, ctx, *, question: commands.clean_content):

		answer = random.choice(lists.ballresponse)
		await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")
	async def randomimageapi(self, ctx, url, endpoint):
		try:
			async with aiohttp.ClientSession() as cs:
				async with cs.get(url) as res:
					r = await res.json() 
			
		except aiohttp.ClientConnectorError:
			return await ctx.send("The API seems to be down...")
		except aiohttp.ContentTypeError:
			return await ctx.send("The API returned an error or didn't return JSON...")
			
		await ctx.send(r[endpoint])
		
	async def api_img_creator(self, ctx, url, filename, content=None):
		async with ctx.channel.typing():
			async with aiohttp.ClientSession() as cs:
				async with cs.get(url) as res:
					req = await res.read() 
		
			if req is None:
				return await ctx.send("I couldn't create the image ;-;")
				
			bio = BytesIO(req)
			bio.seek(0)
			await ctx.send(content=content, file=discord.File(bio, filename=filename))


	@command(name='pornhub', aliases=['ph'], description = 'text as pornhub logo')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def pornhub(self, ctx, p, h):
		async with aiohttp.ClientSession() as cs:
			async with cs.get(f"https://api.alexflipnote.dev/pornhub?text={p}&text2={h}", headers={"Authorization": "R91VWGwSlMh7hsuvsSu2xoKy60VHuUXnm-cIA-D2"}) as res:
				data = BytesIO(await res.read()) 
				file = discord.File(filename="ph.png", fp=data)
				await ctx.send(file=file)

	@commands.command(name="text2art", aliases=["textart"], description  = 'Generate random art from text.', usage = '+text2art <text>')
	@custom_check()
	async def t2a(self, ctx, *, text:str):
		
		art = text2art(text, "rand")
		if len(art) <0:
			await ctx.send("Cant art that!")
		else:
			try:
				await ctx.send("```" + art + "```")
			except Exception as e:
				await ctx.send(e)
	

	
	@commands.command(name = 'randomstyle',description = 'Some cool font style.',usage = '+rns <text>' ,aliases=["randstyle", "rns"])
	@custom_check()
	async def randomstyle(self, ctx, *, text:str):
		
		art = text2art(text, "random-na")
		if len(art) <0:
			await ctx.send("Cant art that!")
		else:
			try:
				await ctx.send(art)
			except Exception as e:
				await ctx.send(e)
	
	@commands.command(name = 'usd', description = 'upside down text',usage = '+usd <text>')
	@custom_check()
	async def upsidedown(self, ctx, *, text:str):
		
		art = text2art(text, "upsidedown")
		if len(art) <0:
			await ctx.send("Cant art that!")
		else:
			try:
				await ctx.send(art)
			except Exception as e:
				await ctx.send(e)
	

	@commands.command(name = 'emote', aliases = ['jumbo', 'emoji'], description = 'Get links of emoji from a message by putting its message id.', usage = '+emote <emoji>')
	@custom_check()
	async def emote(self, ctx,emoji):
		
		try:
			if emoji[1] == "a" :
					emote_id = emoji[-19:-1]
					link = "https://cdn.discordapp.com/emojis/"+emote_id+".gif"
					embed = discord.Embed()
					embed.set_image(url = link)
					await ctx.send(embed = embed)
			else :
					emote_id = emoji[-19:-1]
					link = "https://cdn.discordapp.com/emojis/"+emote_id+".png"
					embed = discord.Embed()
					embed.set_image(url = link)
					await ctx.send(embed = embed)
					
		except :
			pass





	# @commands.command(aliases=["ig"])
	# async def instagram(self, ctx, *, url):
	# 	profile = Profile(f'{url}')
	# 	headers
	# 	data  = profile.scrape(headers = headers)
	# 	print(data)
				
				
				

		
		
			

		# await util.page_switcher(ctx, pages)
				
				
			

		
	


   


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("fun")


def setup(bot):
	bot.add_cog(Fun(bot))
