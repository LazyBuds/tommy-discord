from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure , cooldown
from discord.ext.commands import command, has_permissions, BucketType, bot_has_permissions
from discord.ext.commands import CheckFailure, guild_only, BadArgument
from discord.ext import commands
import discord
from PIL import Image
import operator
import time
from datetime import datetime ,timedelta
import PIL
import aiohttp
from datetime import datetime
from math import floor
import re

import io
from PIL import ImageDraw, ImageFilter, ImageChops, ImageOps, ImageSequence
from PIL import ImageFont
from io import BytesIO
import qrcode
from typing import Union
import requests
import textwrap
import os
import random



from ..db import db
from ..utils import default, zomato, datpaginator,paginator
from ..utils.paginator import HelpPaginator, CannotPaginate, Pages
from ..utils.textutils import auto_text_size,auto_size


numbers = ("🇦","🇧")

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

class Misc(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.dps = []
		
	
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


	@command(name = 'embed', description ='create your own custom embed', usage = '+embed')
	@custom_check()
	@has_permissions(manage_channels=True)
	@bot_has_permissions(manage_channels=True)
	@cooldown(2, 60, BucketType.user)

	async def embed(self, ctx , channel : discord.TextChannel):
		await ctx.send("What should be title ? Reply None if no title")
		

		def check(m):
			return m.author == ctx.message.author
		
		try:
			#TITLE 
			
			title_reply = await self.bot.wait_for('message', timeout=25.0, check=check)

			#DESCRIPTION

			await ctx.send("What should be description ? Reply None if no description")

			description_reply = await self.bot.wait_for('message', timeout=45.0, check=check)

			#Footer

			await ctx.send("What should be footer ? Reply None if no footer")

			footer_reply = await self.bot.wait_for('message', timeout=25.0, check=check)

			#Thumbnail

			await ctx.send("Please send link of thumbnail for embed. Reply None if no image")

			thumbnail_reply = await self.bot.wait_for('message', timeout=25.0, check=check)

			#IMAGE

			await ctx.send("Please send link of image for embed. Reply None if no image")

			image_reply = await self.bot.wait_for('message', timeout=25.0, check=check)

			#Color

			await ctx.send("Color code for embed (Hex); ex. `FFGG11`. Reply None if no color")

			color_reply = await self.bot.wait_for('message', timeout=45.0, check=check)

			image_url = image_reply.content
			thumbnail_url = thumbnail_reply.content
			#hex_code = color_reply.content
			#color_final = int(f"{hex_code}" , 16)

			embed_msg = discord.Embed(title = title_reply.content , description = description_reply.content)

			if color_reply.content.lower() != "none" :
				color_c = color_reply.content
				color_content = color_c.upper()
				hex_code = color_content
				color_final = int(f"{hex_code}" , 16)
				embed_msg.color = color_final
				
			if color_reply.content.lower() == "none" :
				embed_msg.color == None
				
			
			if image_url.lower() != "none" :
				embed_msg.set_image(url = image_url)
				
			if image_url.lower() == "none" :
				embed_msg.image == None
				
			if thumbnail_url.lower() != "none" :
				embed_msg.set_thumbnail(url=thumbnail_url)
				
			if thumbnail_url.lower() == "none" :
				embed_msg.thumbnail == None
				
			if footer_reply.content.lower() != "none" :
				embed_msg.set_footer(text = footer_reply.content)

			if footer_reply.content.lower() == "none" :
				embed_msg.footer == None
				

			if embed_msg.title.lower() == "none" :
				embed_msg.title = None
				
			if embed_msg.description.lower() == "none" : 
				embed_msg.description = None
			
			
			await channel.send(embed = embed_msg)
			


		except Exception as error:
			
			await ctx.send("`Reply with message in time i.e. 45 seconds`") 

	@embed.error
	async def embed_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("You need the Manage channel permission to do that.")


	@command(name="prefix", description  = 'change your guild prefix', usage = '+prefix <newprefix>')
	@custom_check()
	@has_permissions(manage_guild=True)
	async def change_prefix(self, ctx, new:str = None):

		if new is None:
			oldprefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)
			await ctx.send(f"Current prefix is `{oldprefix}`")

		if new != None:
			if len(new) > 5:
				await ctx.send("The prefix can not be more than 5 characters in length.")
			else: 
				db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
				await ctx.send(f"Prefix set to `{new}`")

		
		

	@change_prefix.error
	async def change_prefix_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("You need the Manage Server permission to do that.")

	# @command(name="sendpic")
	# async def pic(self, ctx, channel:discord.TextChannel=None, *, name):
	# 	channel = channel or  ctx.channel
	# 	await channel.send(file=discord.File(f"./data/images/{name}"+".png"))

	# @command(name="sendpic")
	# @cooldown(3, 60, BucketType.user)
	# async def picc(self, ctx, pfp, channel :discord.TextChannel, *, picname):
	# 	async with aiohttp.ClientSession() as session:
	# 		async with session.get(f"{pfp}") as resp:
	# 			if resp.status != 200:
	# 				return await ctx.send('Could not download file...')
	# 			data = io.BytesIO(await resp.read())
				
	# 			await channel.send(file=discord.File(data, f'{picname}.png'))

	# @command(name="sendgif")
	# @cooldown(3, 60, BucketType.user)
	# async def gif(self, ctx, pfp, channel :discord.TextChannel, *, gifname):
	# 	async with aiohttp.ClientSession() as session:
	# 		async with session.get(f"{pfp}") as resp:
	# 			if resp.status != 200:
	# 				return await ctx.send('Could not download file...')
	# 			data = io.BytesIO(await resp.read())
				
	# 			await channel.send(file=discord.File(data, f'{gifname}.gif'))
		
	# @command(name = "emote")
	# async def piccc(self, ctx):
	# 	basewidth = 800
	# 	img = Image.open('./data/images/self_roles.png')
	# 	wpercent = (basewidth/float(img.size[0]))
	# 	hsize = int((float(img.size[1])*float(wpercent)))
	# 	img = img.resize((basewidth,hsize), Image.ANTIALIAS)
	# 	img = img.convert("RGB")
	# 	img.save('sompic.jpg',quality = 95)
	# 	# dataa = io.BytesIO(await resp.read())
	# 	await ctx.guild.create_custom_emoji(name = 'rohan', image ='./data/images/sexy.png' )


	# @command(name='bgfill', aliases = ['bg'])
	# async def bg(self, ctx, user:discord.Member = None, fill):
	
	# 	member = member or ctx.author
	# 	img_url = member.avatar_url_as(format="png") # try all three

	# 	image = Image.open(BytesIO(response.content))
	# 	fill_color = fill
				
	# 	if image.mode in ('RGBA', 'LA'):
	# 		background = Image.new(image.mode[:-1], image.size, fill_color)
	# 		background.paste(image, image.split()[-1])
	# 		image = background
	# 		b = BytesIO()
	# 		image.save(b, format='png')
	# 		b.seek(0)
	# 		file = discord.File(filename="background.png", fp=b)
	# 		await ctx.send(file = file)


	# @command(name = 'createemoji', aliases = ['emote','emoji'])
	# async def jg (self, ctx, url, namee):
	# 	async with aiohttp.botSession() as session:
	# 		async with session.get(f"{url}") as resp:
	# 			if resp.status != 200:
	# 				return await ctx.send('Could not download file...')
	# 			data = io.BytesIO(await resp.read())
	# 			kk = Image.open(data)
	# 			size  = 100,100
	# 			kk.resize(size)
	# 			kk.save(f'./data/images/emote.png', quality=95)
	# 			with open(f'./data/images/emote.png', "rb") as image:
	# 				image_byte = image.read()
	# 				await ctx.guild.create_custom_emoji(name = namee, image = image_byte)
	# 				await ctx.send("emote added successfully")


	

	@command(name= 'jankaari', aliases =['jankari'], description  = 'gives jankaari about you on nice bg', usage = '+jankaari <user>' )
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def jankaari(self, ctx, user: discord.Member= None):
		user = user or ctx.author
		img = Image.open("./data/images/infoimgimg.png") #Replace infoimgimg.png with your background image.
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype("./data/ModernSans-Light.ttf", 120) #Make sure you insert a valid font from your folder.
		fontbig = ImageFont.truetype("./data/Fitamint_Script.ttf", 400) #Make sure you insert a valid font from your folder.
		draw.text((200, 0), "Information:", fill = 'black', font=fontbig) #draws Information
		draw.text((50, 500), "Username: {}".format(user.name), fill = 'black', font=font) #draws the Username of the user
		draw.text((50, 700), "ID:  {}".format(user.id), fill = 'black', font=font) #draws the user ID
		draw.text((50, 900), "User Status:{}".format(user.status), fill = 'black', font=font) #draws the user status
		draw.text((50, 1100), "Account created: {}".format(user.created_at),fill = 'black', font=font) #When the account was created 
		draw.text((50, 1300), "Nickname:{}".format(user.display_name), fill = 'black', font=font) # Nickname of the user
		draw.text((50, 1500), "Users' Top Role:{}".format(user.top_role), fill = 'black', font=font) #draws the top rome
		draw.text((50, 1700), "User Joined:{}".format(user.joined_at), fill = 'black', font=font) #draws info about when the user joined
		b = BytesIO()
		img.save(b, format='png')
		b.seek(0)
		file = discord.File(filename="jankaari.png", fp=b)
		await ctx.send(file = file)
		del b


	# @command(name = 'merge')
	# async def merge(self, ctx):
	# 	im1 = Image.open('./data/images/test.gif')
	# 	im2 = Image.open('./data/images/card1.png')
	# 	im2 = im2.resize((200, 200))
	# 	mask_im = Image.new("L", im2.size, 0)
	# 	draw = ImageDraw.Draw(mask_im)
	# 	draw.ellipse([(0, 0), im2.size], fill=255)
	# 	# mask_im.save('./data/images/mask_circle.png', quality=95)
	# 	frames = []
	# 	for frame in ImageSequence.Iterator(im1):
	# 		frame = frame.copy()
	# 		frame.paste(im2, (400, 35), mask_im)
	# 		frames.append(frame)
	# 		frames[0].save('output.gif', save_all=True, append_images=frames[1:])
		
		# back_im = im1.copy()
		# back_im.paste(im2,(755,50), mask_im)
		# back_im = back_im.convert("RGB")
		# back_im.save('./data/images/dangerchamaar.png', quality=95)
		# # img = Image.open('./data/images/dangerchamaar.png')
		# # draw = ImageDraw.Draw(img)
		# # fontbig = ImageFont.truetype("./data/ruso.ttf", 100)
		# # font = ImageFont.truetype("./data/ruso.ttf",70)
		# # Fontt= ImageFont.truetype("./data/ruso.ttf",65)
		# # draw.text((720, 485), f"WELCOME", (255, 255, 255), font=fontbig)
		# # draw.text((750, 620),f"{ctx.author}", (255, 255, 255), font=font)
		# # draw.text((750, 720),f"{len(ctx.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)
	
		# img.save('./data/images/dangerchamaarr.png')

		# await ctx.send(file = discord.File('output.gif'))
		
	@command(name = 'ping', description  = 'Pong!')
	@custom_check()
	async def ping(self, ctx):
		
		before = time.monotonic()
		before_ws = int(round(self.bot.latency * 1000, 1))
		message = await ctx.send("🏓 Pong")
		ping = (time.monotonic() - before) * 1000
		await message.edit(content=f"🏓 WS: `{before_ws}`ms  |  REST: `{int(ping)}`ms")

	@command(name = 'avatar',aliases= ['av'], description  = 'Get the avatar of you or someone else')
	@custom_check()

	async def avatar(self, ctx, *, member: discord.Member = None):
	
		member = member or ctx.author
		
		embed = discord.Embed(color = discord.Color.red())
		embed.set_image(url = member.avatar_url)
		await ctx.send(embed=embed)

	@command(name = 'zomato', description  = 'display top 5 restaurants in your city',usage = f'+zomato <city>' )
	@custom_check()
	@cooldown(2, 45, BucketType.user)
	async def food(self, ctx, params : str ):
		
		try:
			
			city = params
		
		
		
		
			count = '5'
			data = zomato.top_rest(city, count)
			names = ""
			for j in range(0, int(count)):
				name = (data[j]["Name"])
				cuisines = (data[j]["Cuisines"])
				timings = (data[j]["Timings"])
				url = (data[j]["url"])
				names = names + f"{j+1}:" + "\n" + \
					f"**Name** : {name}" + "\n" + \
					f"**Cuisines** : {cuisines}" + "\n" + \
					f"**Timings** : {timings}" + "\n" + \
					f"**url** : [Here]({url})" + "\n"
				j = j+1
			# p = Pages(ctx,names)
			# await p.paginate()
			embed = discord.Embed(title="Top restaurents near you:",
								description=f"{names}",
								color=ctx.author.colour)
			await ctx.send(embed=embed)
		except:
			await ctx.send('enter a valid city')
		

	# @food.error
	# async def food_error(self, ctx, exc):
	# 	if isinstance(exc, CheckFailure):
	# 		await ctx.send("enter valid city name")
	# 	if isinstance(exc, BadArgument):
	# 		await ctx.send("enter valid city name")



	# @command(name  = 'roles')
	# @guild_only()
	# @has_permissions(administrator = True)
	# async def roles(self, ctx):
	# 	""" Get all roles in current server """
	# 	allroles = ""
	# 	for num, role in enumerate(sorted(ctx.guild.roles, reverse=True), start=1):
	# 		allroles += f"[{str(num).zfill(2)}] {role.id}\t{role.name}\t[ Users: {len(role.members)} ]\r\n"
			
	# 	data = BytesIO(allroles.encode('utf-8'))
	# 	await ctx.send(content=f"Roles in **{ctx.guild.name}**", file=discord.File(data, filename=f"{default.timetext('Roles')}"))

	@command(name = 'joindate', description  = 'Check when a user joined the current server',usage = '+joindate <user>')
	@custom_check()
	@guild_only()
	async def joinedat(self, ctx, *, user: discord.Member = None):
		
		user = user or ctx.author
		embed = discord.Embed(colour = ctx.author.colour)
		embed.set_thumbnail(url=user.avatar_url)
		embed.description = f'**{user}** joined **{ctx.guild.name}**\n{default.date(user.joined_at)}'
		await ctx.send(embed=embed)


	@command(name = 'modsonline', description = 'Check which mods are online on current guild')
	@custom_check()
	@guild_only()
	async def mods(self, ctx):
		
		message = ""
		online, idle, dnd, offline = [], [], [], []
		for user in ctx.guild.members:
			if ctx.channel.permissions_for(user).kick_members or \
				ctx.channel.permissions_for(user).ban_members:
				if not user.bot and user.status is discord.Status.online:
					online.append(f"**{user}**")
				if not user.bot and user.status is discord.Status.idle:
					idle.append(f"**{user}**")
					
				if not user.bot and user.status is discord.Status.dnd:
					dnd.append(f"**{user}**")
				if not user.bot and user.status is discord.Status.offline:
					offline.append(f"**{user}**")
		if online:
			message += f"🟢 {', '.join(online)}\n"
		if idle:
			message += f"🟡 {', '.join(idle)}\n"
		if dnd:
			message += f"🔴 {', '.join(dnd)}\n"
		if offline:
			message += f"⚫ {', '.join(offline)}\n"
		await ctx.send(f"Mods in **{ctx.guild.name}**\n{message}")

	@command(name = 'invite', description  = ' Invite me to your server ')
	@custom_check()
	async def invite(self, ctx):
		await ctx.send(f"**{ctx.author.name}**, use this URL to invite me\n<https://discord.com/api/oauth2/authorize?client_id=697463492457922571&permissions=2147483639&redirect_uri=https%3A%2F%2Fwww.lazybuds.xyz%2Ftommy&response_type=code&scope=identify%20bot>")

	@command(name = 'free-nitro', description  = 'giving away 100 nitros')
	@custom_check()
	async def givenitro(self, ctx):
		embed = discord.Embed(title = 'Claim your free nitro ', description  = '[https://discord.gift/HMYpGmkY3qaqefR9](https://discord.gg/gCmPWtC)')
		await ctx.send(embed = embed)

	@command(name = 'supportserver', aliases = ['support'], description  = ' Get an invite to our support server! ')
	@custom_check()
	async def botserver(self, ctx):
		await ctx.send(f"**Here you go {ctx.author.name} 🍻\n ")
		await ctx.send('https://discord.gg/gCmPWtC')

	@command(name = 'qr', description  = 'convert text into qrcode', usage = '+qr <text>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def qr(self, ctx, *, text):
		await ctx.message.delete()
		qr = qrcode.make(f'{text}')
		b = BytesIO()
		qr.save(b, format='png')
		b.seek(0)
		file = discord.File(filename="qr.png", fp=b)
		await ctx.send(file = file)
		del b
		# with open('./data/images/qr.png','rb') as fp:
		
	# @command(name = 'resize')
	# async def resize(self, ctx, user: Union[discord.User, discord.Member] )-> bytes :
	# 	avatar_url = user.avatar_url_as(format="png")
	# 	async with self.session.get(f'{avatar_url}') as response:
	# 		avatar_bytes = await response.read()
				
				
	# 		kk  = Image.open(BytesIO(avatar_bytes))
	# 		size = 256,256
	# 		kk.resize(size)
	# 		kk.save('./data/images/avatar'+ ".png")

	# 		def crop_to_circle(im):
	# 			bigsize = (im.size[0] * 3, im.size[1] * 3)
	# 			mask = Image.new('L', bigsize, 0)
	# 			ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
	# 			mask = mask.resize(im.size, Image.ANTIALIAS)
	# 			mask = ImageChops.darker(mask, im.split()[-1])
	# 			im.putalpha(mask)
	# 		im = Image.open('./data/images/avatar.png').convert('RGBA')
	# 		crop_to_circle(im)
	# 		im.save('./data/images/croppedcircle.png')
	# 		await ctx.send(file = discord.File('./data/images/croppedcircle' +".png"))

	# @command(name = 'resizegif')
	# async def resizegif(self, ctx, user: Union[discord.User, discord.Member] )-> bytes :
	# 	avatar_url = user.avatar_url_as(format="png")
	# 	async with self.session.get(f'{avatar_url}') as response:
    #         # this gives us our response object, and now we can read the bytes from it.
	# 		avatar_bytes = await response.read()
	# 		kk  = Image.open(BytesIO(avatar_bytes))	
	# 		kk.resize(256,256)
			
	# 		kk.save("./data/images/resizegif.png")

	# 		def crop_to_circle(im):
	# 			bigsize = (im.size[0] * 3, im.size[1] * 3)
	# 			mask = Image.new('L', bigsize, 0)
	# 			ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
	# 			mask = mask.resize(im.size, Image.ANTIALIAS)
	# 			mask = ImageChops.darker(mask, im.split()[-1])
	# 			im.putalpha(mask)
	# 		im = Image.open('./data/images/resizegif.png').convert('RGBA')
	# 		crop_to_circle(im)
	# 		im.save('./data/images/croppedgif.png')
	# 		await ctx.send(file = discord.File('./data/images/croppedgif' +".png"))

	

	@command(name = 'beautiful',aliases = ['bful',"b'ful"] ,description  = 'tell everyone how beautiful they are', usage  = '+beatiful <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def card(self, ctx, user:discord.Member = None):
		if user == None and ctx.message.attachments:
			attachment_url = ctx.message.attachments[0].url
			img_url = attachment_url 
		elif user != None and not ctx.message.attachments:
			
			img_url = user.avatar_url_as(format="png")
		else :
			entity =  ctx.command
			p = await HelpPaginator.from_command(ctx, entity)
			return

		# user  =  user or ctx.author 
		# img_url = user.avatar_url_as(format="png", size=256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				img = Image.open(data)
				bcg = Image.open(f'./data/images/beautiful.jpg')
				img = img.resize((150,180))
				back_im = bcg.copy()
				back_im.paste(img, (435, 40), img.convert('RGBA'))
				back_im.paste(img,(440, 380), img.convert('RGBA'))
				b = BytesIO()
				back_im.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="beautiful.png", fp=b)
				await ctx.send(file = file)
				del b


	@command(name ='bday',aliases = ['happybday',"birthday"] ,description  = 'wish your friend  on their bday', usage  = '+bday <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def bday(self, ctx, user:discord.Member = None):
		# if user == None and ctx.message.attachments:
		# 	attachment_url = ctx.message.attachments[0].url
		# 	img_url = attachment_url 
		# elif user != None and not ctx.message.attachments:
			
		# 	img_url = user.avatar_url_as(format="png")
		# else :
		# 	entity =  ctx.command
		# 	p = await HelpPaginator.from_command(ctx, entity)
		# 	return

		user  =  user or ctx.author 
		img_url = user.avatar_url_as(format="png",size = 1024) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				img = Image.open(data)
				bcg = Image.open(f'./data/images/bday.png')
				img = img.resize((480,480))
				back_im = bcg.copy()
				back_im.paste(img, (1400, 25), img.convert('RGBA'))
				# back_im.paste(img,(440, 380), img.convert('RGBA'))
				draw = ImageDraw.Draw(back_im)
				shadowcolor  = 'red'
				fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 110)
		
				x = 600
				y = 480
				draw.text((x-4, y-4), f"{user.display_name}", font=fontbig, fill=shadowcolor)
				draw.text((x+4, y-4), f"{user.display_name}", font=fontbig, fill=shadowcolor)
				draw.text((x-4, y+4), f"{user.display_name}", font=fontbig, fill=shadowcolor)
				draw.text((x+4, y+4), f"{user.display_name}", font=fontbig, fill=shadowcolor)
				draw.text((x, y), f"{user.display_name}", fill = 'white', font=fontbig)
				b = BytesIO()
				back_im.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="bday.png", fp=b)
				await ctx.send(file = file)
				del b


	
	@command(name = 'neta', description = 'congratulations for joining bjp', usage = '+neta <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def neta(self, ctx, user:discord.Member =None):
		user = user or ctx.author
		
		img_url = user.avatar_url_as(format="png", size=256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				img = Image.open(data)
				bcg = Image.open(f'./data/images/modi3.png')
				img = img.resize((180,150))
				back_im = bcg.copy().resize((1200,800))
				back_im.paste(img, (820, 220), img.convert('RGBA'))
				draw = ImageDraw.Draw(back_im)
				shadowcolor  = 'orange'
				fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 66)
		
				x = 100
				y = 650
				draw.text((x-2, y-2), f"{user.display_name}", font=fontbig, fill=shadowcolor)
				draw.text((x+2, y-2), f"{user.display_name}", font=fontbig, fill=shadowcolor)
				draw.text((x-2, y+2), f"{user.display_name}", font=fontbig, fill=shadowcolor)
				draw.text((x+2, y+2), f"{user.display_name}", font=fontbig, fill=shadowcolor)
				draw.text((x, y), f"{user.display_name}", fill = 'black', font=fontbig)
				
				b = BytesIO()
				back_im.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="neta.png", fp=b)
				await ctx.send(file = file)
				del b


	@command(name = 'pooja', description = 'what is this behaviour?', usage = '+pooja <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def pooja(self, ctx, user:discord.Member =None):
		# if user == None and ctx.message.attachments:
		# 	attachment_url = ctx.message.attachments[0].url
		# 	img_url = attachment_url 
		# elif user != None and not ctx.message.attachments:
			
		# 	img_url = user.avatar_url_as(format="png")
		# else :
		# 	entity =  ctx.command
		# 	p = await HelpPaginator.from_command(ctx, entity)
		# 	return

		user = user or ctx.author
		img_url = user.avatar_url_as(format="png", size=256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				img = Image.open(data)
				bcg = Image.open(f'./data/images/pooja.png')
				img = img.resize((150,120))
				back_im = bcg.copy().resize((1200,800))
				back_im.paste(img, (650, 50), img.convert('RGBA'))
				draw = ImageDraw.Draw(back_im)
				shadowcolor  = 'black'
				fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 55)
		
				x = 80
				y = 700
				draw.text((x-2, y-2), f"{user.display_name} , what's this behaviour?", font=fontbig, fill=shadowcolor)
				draw.text((x+2, y-2), f"{user.display_name} , what's this behaviour?", font=fontbig, fill=shadowcolor)
				draw.text((x-2, y+2), f"{user.display_name} , what's this behaviour?", font=fontbig, fill=shadowcolor)
				draw.text((x+2, y+2), f"{user.display_name} , what's this behaviour?", font=fontbig, fill=shadowcolor)
				draw.text((x, y), f"{user.display_name} , what's this behaviour? ", fill = 'white', font=fontbig)
				
				b = BytesIO()
				back_im.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="pooja.png", fp=b)
				await ctx.send(file = file)
				del b


	@command(name = 'worthless', description  = 'tell everyone how worthless they are', usage = '+worthless <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def worthless(self, ctx, user:discord.Member = None):
		if user == None and ctx.message.attachments:
			attachment_url = ctx.message.attachments[0].url
			img_url = attachment_url 
		elif user != None and not ctx.message.attachments:
			
			img_url = user.avatar_url_as(format="png")
		else :
			entity =  ctx.command
			p = await HelpPaginator.from_command(ctx, entity)
			return

		# user = user or ctx.author
		# img_url = user.avatar_url_as(format="png", size=256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				img = Image.open(data)
				bcg = Image.open(f'./data/images/worthless.jpg')
				img = img.resize((390,200))
				back_im = bcg.copy()
				img2 = img.copy()
			
				img2=img2.resize((80,60))
				back_im.paste(img, (120, 100), img.convert('RGBA'))
				back_im.paste(img2,(395, 620), img2.convert('RGBA'))
				b = BytesIO()
				back_im.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="worthless.png", fp=b)
				await ctx.send(file = file)
				del b
		

	def text_wrap(self, text, font, max_width):
		lines = []
		if font.getsize(text)[0] <= max_width:
			lines.append(text) 
		else:
			words = text.split(' ')  
			i = 0
			while i < len(words):
				line = ''         
				while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
					line = line + words[i] + " "
					i += 1
				if not line:
					line = words[i]
					i += 1
				lines.append(line)
		return lines
 
 
# def draw_text(self, text):    
# 	img = Image.open('./data/images/notshow.png')
# 	img = img.resize((1024,1024))
# 	image_size = img.size 
 

#     font_file_path = './data/ruso.ttf'
#     font = ImageFont.truetype(font_file_path, size=65, encoding="unic")
 
#     # get shorter lines
#     lines = self.text_wrap(text, font, image_size[0])
#     print lines # ['This could be a single line text ', 'but its too long to fit in one. ']
# 	draw_text("This could be a single line text but its too long to fit in one.")

# 	# def draw_multiple_line_text(self, image, text, font, text_color, text_start_height):
# 	# 	draw = ImageDraw.Draw(image)
# 	# 	image_width, image_height = image.size
# 	# 	y_text = text_start_height
# 	# 	lines = textwrap.wrap(text, width=65)
# 	# 	for line in lines:
# 	# 		line_width, line_height = font.getsize(line)
# 	# 		draw.text(((image_width - line_width) / 2, y_text), 
# 	# 		line, font=font, fill=text_color)
# 	# 		y_text += line_height
	@command(name = 'notshow', description = 'i may not show it but ...', usage = '+notshow <text>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def notshow(self, ctx, *, text):
		''' +notshow but aap toh bade cutie ho '''
		if len(text) > 200 :
			await ctx.send('text should be less than 200 chars')
		else:
			img = Image.open('./data/images/notshow.png')
			img = img.resize((1024,1024))
			image_size = img.size 
			font_file_path = './data/OpenSans-Regular.ttf'
			
			fontbig = ImageFont.truetype("./data/ruso.ttf", 100)
	
			
			x = 40
			y = 20
			z =800
			color= "black"
			shadowcolor = 'black'
			draw = ImageDraw.Draw(img)
			draw.text((x-2, y-2), f"I may not show it", font=fontbig, fill=shadowcolor)
			draw.text((x+2, y-2), f"I may not show it", font=fontbig, fill=shadowcolor)
			draw.text((x-2, y+2), f"I may not show it", font=fontbig, fill=shadowcolor)
			draw.text((x+2, y+2), f"I may not show it", font=fontbig, fill=shadowcolor)
			draw.text((x, y), f"I may not show it", (255, 255, 255), font=fontbig)

			# fontsize = int(9318.6/len(text)**1.0956)

			# fontsize  = 70

			
			

			
			font = ImageFont.truetype(font_file_path)
			label_font, label_text = auto_text_size(text, font, 950, font_scalar=1.1)

			

	
			draw.text((x,z), label_text, fill=color, font=label_font, align = 'center')
			



			# fontsize = 70  # starting font size
			# # portion of image width you want text width to be
			# img_fraction = 0.45
			# font = ImageFont.truetype("./data/OpenSans-Regular.ttf", fontsize)
			# while font.getsize(text)[0] < img_fraction*img.size[0]:
			# 	# iterate until the text size is just larger than the criteria
			# 	fontsize += 1
			# 	font = ImageFont.truetype("./data/OpenSans-Regular.ttf", fontsize)
			# 	# optionally de-increment to be sure it is less than criteria
			# fontsize -= 1
			# font = ImageFont.truetype("./data/OpenSans-Regular.ttf", fontsize)
			# print ('final font size',fontsize)
			# lines = self.text_wrap(text, font, image_size[0]- 10)
			# line_height = font.getsize('hg')[1]
			# # draw.text((10, 25), text, font=font) # put the text on the image
			# for line in lines:
			# 	draw.text((x,z), line, fill=color, font=font)
			# 	z = z + line_height
			b = BytesIO()
			img.save(b, format='png')
			b.seek(0)
			file = discord.File(filename="notshow.png", fp=b)
			await ctx.send(file = file)
			del b
			


	

	# @command(name = 'notshow')
	# async def notshow(self, ctx, *, texts ):
	# 	bcg = Image.open(f'./data/images/notshow.png')
	# 	bcg = bcg.resize((1024,1024))
	# 	back_im = bcg.copy()
	
	# 	draw = ImageDraw.Draw(back_im)
	# 	x,y = 40,0
	# 	w, h = back_im.size
	# 	shadowcolor = 'black'
	# 	color = 'white'
	# 	# WIDTH = 375
	# 	# HEIGHT = 100
	# 	fontbig = ImageFont.truetype("./data/ruso.ttf", 100)
	# 	font = ImageFont.truetype("./data/ruso.ttf",65)
	# 	# Fontt= ImageFont.truetype("./data/ruso.ttf",65)
	# 	draw.text((x-2, y-2), f"I may not show it", font=fontbig, fill=shadowcolor)
	# 	draw.text((x+2, y-2), f"I may not show it", font=fontbig, fill=shadowcolor)
	# 	draw.text((x-2, y+2), f"I may not show it", font=fontbig, fill=shadowcolor)
	# 	draw.text((x+2, y+2), f"I may not show it", font=fontbig, fill=shadowcolor)
	# 	draw.text((x, y), f"I may not show it", (255, 255, 255), font=fontbig)
	# 	text = "This could be a single line text but its too long to fit in one."
	# 	lines = text_wrap(text, font, image_size[0])
	# 	line_height = font.getsize('hg')[1]
	# 	x = 10
	# 	y = 20
	# 	for line in lines:
	# 		draw.text((x, y), line, fill=color, font=font)
	# 		y = y + line_height
		

	# 	# lines = textwrap.wrap(texts, width=6
	# 	# y_text = h
	# 	# for line in lines:
	# 	# 	width, height = font.getsize(line)
	# 	# 	draw.text(((w - width) / 2, y_text), line, font=font, fill=color)
	# 	# 	y_text += height

	# 	# self.draw_multiple_line_text(back_im, text, font,color, 300 )
		
	# 	back_im.save('./data/images/notshow1.png',quality = 95)
	# 	await ctx.send(file = discord.File('./data/images/notshow1.png'))

	@command(name = 'nadarre', usage = f"+nadarre text1 | text2", description = 'You can add text on nadarre meme template')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def split(self,ctx, *, text:str):
		'''+nadarre Rohan hu | lafda krduga '''
		try : 

			
			text = text.split("|",2)
			if len(text) != 2 :
				return await ctx.send(f'use {ctx.prefix}help nadarre')



			img = Image.open('./data/images/nadare.png')
			img = img.resize((1024,1024))
			image_size = ((700,700))
			font_file_path = './data/OpenSans-Regular.ttf'
			font = ImageFont.truetype(font_file_path, size=70, encoding="unic")
			fontbig = ImageFont.truetype("./data/ruso.ttf", 85)
			draw = ImageDraw.Draw(img)
			if 17> len(text[0])>13:
				fontbig = ImageFont.truetype("./data/ruso.ttf", 80)
				draw.text((80, 300), f"{text[0]}", fill = 'black', font=fontbig)
			elif len(text[0]) <13:
				fontbig = ImageFont.truetype("./data/ruso.ttf", 90)
				draw.text((80, 300), f"{text[0]}", fill = 'black', font=fontbig)
			elif len(text[0]) >17:
				fontbig = ImageFont.truetype("./data/ruso.ttf", 70)
				draw.text((80, 300), f"{text[0]}", fill = 'black', font=fontbig)

		except :
			await ctx.send(f'use {ctx.prefix}help nadarre')



	
		# draw.text((80, 600), f"{text[1]}", fill = 'black', font=fontbig)
		z = 680
		
		
		fontt = ImageFont.truetype(font_file_path)
		label_font, label_text = auto_text_size(text[1], fontt, 550, font_scalar=1.2)
		color = 'black'

			

	
		draw.text((20,z), label_text, fill=color, font=label_font, align = 'center')
		# lines = self.text_wrap(text[1], font, image_size[0])
		# line_height = font.getsize('hg')[1]
		# for line in lines:
		# 	draw.text((20,z), line, fill='black', font=font)
		# 	z = z + line_height
		b = BytesIO()
		img.save(b, format='png')
		b.seek(0)
		file = discord.File(filename="nadarre.png", fp=b)
		await ctx.send(file = file)
		del b


	@command(name = 'scroll', description  = 'the scroll of truth', usage = '+scroll <text>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def scroll(self,ctx, *, text:str):
		'''+scroll discord ko tinder mat bna'''
		
		img = Image.open('./data/images/scroll.jpg')
		img = img.resize((1024,1024))
		image_size = ((250,250))
		font_file_path = './data/ruso.ttf'
		font = ImageFont.truetype(font_file_path, size=35, encoding="unic")
		fontbig = ImageFont.truetype("./data/ruso.ttf", 100)
		draw = ImageDraw.Draw(img)
		# draw.text((80, 300), f"{text[0]}", fill = 'black', font=fontbig)
		# draw.text((80, 600), f"{text[1]}", fill = 'black', font=fontbig)
		z = 650
		lines = self.text_wrap(text, font, image_size[0])
		line_height = font.getsize('hg')[1]
		for line in lines:
			draw.text((190,z), line, fill='black', font=font)
			z = z + line_height

		b = BytesIO()
		img.save(b, format='png')
		b.seek(0)
		file = discord.File(filename="scroll.png", fp=b)
		await ctx.send(file = file)
		del b

		
	@command(name = 'didyoumean', description  = ' use krke dekhle ', usage = '+didyoumean <text1 | text2>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def didyoumean(self,ctx, *, text:str):
		''' +didyoumean sabse bada cutie | Sanket '''
		try:

			text = text.split("|",1)
			if len(text) != 2 :
				return await ctx.send(f'use {ctx.prefix}help didyoumean')
			img = Image.open('./data/images/didyou.jpeg')
			img = img.resize((1800,800))
			
			font_file_path = './data/OpenSans-Regular.ttf'
			font = ImageFont.truetype(font_file_path, size=70, encoding="unic")
			fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 70)
			draw = ImageDraw.Draw(img)
			draw.text((370, 215), f"{text[0]}", fill = 'black', font=fontbig)
			# draw.text((80, 600), f"{text[1]}", fill = 'black', font=fontbig)
			z = 590
			
			draw.text((600,z),f'{text[1]}' ,fill='blue', font=font)
			b = BytesIO()
			img.save(b, format='png')
			b.seek(0)
			file = discord.File(filename="didyoumean.png", fp=b)
			await ctx.send(file = file)
			del b
		except :
			await ctx.send(f'type {ctx.prefix}help didyoumean')


	@command(name = 'airpods',aliases= ['airpod'], description = 'saste airpods kay sath aapki tasveer', usage = '+airpods <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def airpod(self,ctx, user:discord.Member = None):
		if user == None and ctx.message.attachments:
			attachment_url = ctx.message.attachments[0].url
			img_url = attachment_url 
		elif user != None and not ctx.message.attachments:
			
			img_url = user.avatar_url_as(format="png")
		else :
			entity =  ctx.command
			p = await HelpPaginator.from_command(ctx, entity)
			return

		# user = user or ctx.author
		# img_url = user.avatar_url_as(format="png", size=128) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				avatar = Image.open(data)
				avatar = avatar.convert('RGBA').resize((128,128))


				blank = Image.new('RGBA', (400, 128), (255, 255, 255, 0))
				left = Image.open('data/images/leftairpod.gif')
				right = Image.open('data/images/rightairpod.gif')
				out = []
				for i in range(0, left.n_frames):
					left.seek(i)
					right.seek(i)
					f = blank.copy().convert('RGBA')
					l = left.copy().convert('RGBA')
					r = right.copy().convert('RGBA')
					f.paste(l, (0, 0), l)
					f.paste(avatar, (136, 0), avatar)
					f.paste(r, (272, 0), r)
					out.append(f.resize((400, 128), Image.LANCZOS).convert('RGBA'))
					
				b = BytesIO()
				out[0].save(b, format='gif', save_all=True, append_images=out[1:], loop=0, optimize=True,
							duration=30, transparency=0)
				b.seek(0)
				file = discord.File(filename="airpods.gif", fp=b)
				await ctx.send(file = file)
				del b


	# @command(name = 'welcomegif')
	# @cooldown(2, 60, BucketType.user)
	# async def welcomegif(self,ctx, user:discord.Member):
		
	
	# 	img_url = user.avatar_url_as(format="png", size=256) # try all three
	
	# 	avatar = Image.open(BytesIO(response.content))
	# 	avatar = avatar.convert('RGBA').resize((190,190))
	# 	mask = Image.new('L', avatar.size, 0)
	# 	draw = ImageDraw.Draw(mask)
	# 	draw.ellipse((0, 0) + avatar.size, fill=255)
	# 	output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
	# 	output.putalpha(mask)
	# 	# size = 900, 450
	# 	left = Image.open('data/images/welcome.gif')
	# 	out = []
	# 	for i in range(0, left.n_frames):
	# 		left.seek(i)
			
	# 		# f = blank.copy().convert('RGBA')
	# 		l = left.copy().convert('RGBA')
	# 		r = output.copy().convert('RGBA')
			
	# 		# f.paste(l, (0, 0), l)
	# 		l.paste(r, (405, 38), r)
	# 		draw = ImageDraw.Draw(l)
	# 		fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 70)
	# 		draw.text((370, 305), f" testing ", fill = 'white', font=fontbig)
	# 		# f.paste(r, (405, 38), r)
	# 		out.append(l.convert('RGBA'))	
	# 	b = BytesIO()
	# 	out[0].save(b, format='gif', save_all=True,append_images=out[1:], loop=0,disposal=2, optimize=True,
    #                 duration=100, transparency=100)
	# 	b.seek(0)
		

	# 	# Save output
	# 	# om = next(frames) # Handle first frame separately
	# 	# om.info = im.info # Copy sequence info
	# 	# om.save("out.gif", save_all=True, append_images=list(frames))		
	# 	file = discord.File(filename = 'welcome.gif', fp=b)
	# 	await ctx.send(file = file)
	

	@command(name = 'drift', description = 'use krke dekhle bhai please', usage = '+drift <user> <text1 | text2>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def drift(self,ctx, user:discord.Member = None, *, text:str):

		'''+drift @Rohan#7140 tinder | discord'''
		try :
			user =  user or ctx.author
			img_url = user.avatar_url_as(format="png", size=256) # try all three
			async with aiohttp.ClientSession() as session:
				async with session.get(f"{img_url}") as resp:
					if resp.status != 200:
						return await ctx.send('Could not download file...')
					data = BytesIO(await resp.read())
					img1 = Image.open(data)
					
					text = text.split("|")
					if len(text) != 2 :
						return await ctx.send(f'use {ctx.prefix}help drift')
					
					img = Image.open('./data/images/drift.jpg')
					img = img.resize((1024,1024))
					back_im = img.copy()
					back_im.paste(img1, (500, 700), img1.convert('RGBA'))

				
					font_file_path = './data/OpenSans-Regular.ttf'
					font = ImageFont.truetype(font_file_path, size=40, encoding="unic")
					fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 100)
					draw = ImageDraw.Draw(back_im)
					# draw.text((80, 300), f"{text[0]}", fill = 'black', font=fontbig)
					# draw.text((80, 600), f"{text[1]}", fill = 'black', font=fontbig)
					z = 110
					y= 110
					# draw.text((290,z), text[0], fill='white', font=font)
					# draw.text((590,z), text[1], fill='white', font=font)
					image_size = ((230,230))
					lines = self.text_wrap(text[0], font, image_size[0])
					liness = self.text_wrap(text[1], font, image_size[0])
					line_height = font.getsize('hg')[1]
					for line in lines:
						draw.text((250,z), line, fill='white', font=font)
						z = z + line_height
						

					for line in liness:
						draw.text((530,y), line, fill='white', font=font)
						y = y + line_height
					# b = BytesIO()
					# img.save(b, format='png')
					# b.seek(0)
					# file = discord.File(filename="drift.png", fp=b)
					# await ctx.send(file = file)


					# text = text.split("|",1)
					
					
					# font_file_path = './data/OpenSans-Regular.ttf'
					# # font = ImageFont.truetype(font_file_path, size=70, encoding="unic")
					# fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 40)
					# draw = ImageDraw.Draw(back_im)
					# # draw.text((370, 215), f"{text[0]}", fill = 'black', font=fontbig)
					# # draw.text((80, 600), f"{text[1]}", fill = 'black', font=fontbig)
					# z = 50
					# y = 730
					# image_size = ((1024,1024))
					# lines = self.text_wrap(text[0], fontbig, image_size[0])
					# liness = self.text_wrap(text[1], fontbig, image_size[0])
					# line_height = fontbig.getsize('hg')[1]
					# for line in lines:
					# 	draw.text((50,z), line, fill='white', font=fontbig)
					# 	z = z + line_height
						

					# for line in liness:
					#  	draw.text((20,y), line, fill='white', font=fontbig)
					#  	y = y + line_height
					
					# # draw.text((600,z),f'{text[1]}' ,fill='blue', font=font)
					b = BytesIO()
					back_im.save(b, format='png')
					b.seek(0)
					file = discord.File(filename="drift.png", fp=b)
					await ctx.send(file = file)
					del b
		except :
			await ctx.send(f'type {ctx.prefix}help drift')

	@command(name = 'sehwag', description = 'add text to sehwag meme', usage = '+sehwag <text1 | text2>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def sehwag(self,ctx, *, text:str):
		'''+sehwag dankmemer? | nhi bhai mai toh tommy bot use krta hu '''
		text = text.split("|",1)
		if len(text) != 2:
			return await ctx.send(f'type {ctx.prefix}help sehwag')

		img = Image.open('./data/images/sehwag.png')
		img = img.resize((1024,1024))
		
		font_file_path = './data/OpenSans-Regular.ttf'
		font = ImageFont.truetype(font_file_path,100)
		draw = ImageDraw.Draw(img)

		
		fontt = ImageFont.truetype(font_file_path)
		# label_font, label_text = auto_text_size(text[0], fontt, 980,fallback_size=80, font_scalar=0.98)
		label_font2, label_text2 = auto_text_size(text[1], fontt, 980, font_scalar=0.98)
		color = 'white'

			

	
		draw.text((270,50), f'{text[0]}', fill=color, font=font, align = 'center')
		draw.text((20,800), label_text2, fill=color, font=label_font2, align = 'center')
		# draw = ImageDraw.Draw(img)
		# # draw.text((500, 215), f"{text[0]}", fill = 'black', font=fontbig)
		# # draw.text((80, 600), f"{text[1]}", fill = 'black', font=fontbig)
		# z = 50
		# y = 730
		# image_size = ((1024,1024))
		# lines = self.text_wrap(text[0], fontbig, image_size[0])
		# liness = self.text_wrap(text[1], fontbig, image_size[0])
		# line_height = fontbig.getsize('hg')[1]
		# for line in lines:
		# 	draw.text((50,z), line, fill='white', font=fontbig)
		# 	z = z + line_height
			

		# for line in liness:
		#  	draw.text((20,y), line, fill='white', font=fontbig)
		#  	y = y + line_height
		
		# draw.text((600,z),f'{text[1]}' ,fill='blue', font=font)
		b = BytesIO()
		img.save(b, format='png')
		b.seek(0)
		file = discord.File(filename="sehwag.png", fp=b)
		await ctx.send(file = file)
		del b


	@command(name = 'idharaa', description = 'add text to idhar aa tujhe du meme', usage = '+idharaa <text1 | text2>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def idharaa(self,ctx, *, text:str):
		'''+idharaa idhar aa dankmemer | tujhe tommy bot dikhata hu  '''
		text = text.split("|",1)
		if len(text) != 2:
			return await ctx.send(f'type {ctx.prefix}help sehwag')

		img = Image.open('./data/images/petergriffin1.jpg')
		img = img.resize((1024,1024))
		
		font_file_path = './data/impact.ttf'
		font = ImageFont.truetype(font_file_path,100)
		draw = ImageDraw.Draw(img)

		
		fontt = ImageFont.truetype(font_file_path)
	
		color = 'white'

		x= 100
		y = 30
		shadowcolor = 'black'
		if len(text[0]) > 12 :

			label_font2, label_text2 = auto_size(text[0], font, 800, font_scalar=0.95)
			draw.text((x-4, y-4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x+4, y-4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x-4, y+4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x+4, y+4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			
			

				

		
			draw.text((100,30), label_text2, fill=color, font=label_font2, align = 'center')
		else :
			x= 270
			y = 30
			label_font2, label_text2 = auto_size(text[0], font, 800, font_scalar=0.95)
			draw.text((x-4, y-4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x+4, y-4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x-4, y+4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x+4, y+4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			
			

				

		
			draw.text((270,30), label_text2, fill=color, font=label_font2, align = 'center')
			
		if len(text[1]) >19: 
			x= 40
			y = 760
			label_font2, label_text2 = auto_size(text[1], font, 940, font_scalar=0.97)
			draw.text((x-4, y-4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x+4, y-4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x-4, y+4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x+4, y+4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x,y), label_text2, fill=color, font=label_font2, align = 'center')

		else :
			x= 180
			y = 760
			label_font2, label_text2 = auto_size(text[1], font, 800, font_scalar=0.97)
			draw.text((x-4, y-4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x+4, y-4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x-4, y+4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x+4, y+4), f"{label_text2}", font=label_font2, fill=shadowcolor, align = 'center')
			draw.text((x,y), label_text2, fill=color, font=label_font2, align = 'center')

		
		

			

	
		

		# image_size =((980,900))
		# fontt = ImageFont.truetype(font_file_path,85)
		
		# lines = self.text_wrap(text[1], fontt,image_size[0] )
		# z= 710
		# y =710
		# x = 30
		

		# line_height = fontt.getsize('hg')[1]
		# for line in lines:
		# 	draw.text((x-4, z-4), line, font=fontt, fill=shadowcolor, align = 'center')
		# 	draw.text((x+4, z-4), line, font=fontt, fill=shadowcolor,align = 'center')
		# 	draw.text((x-4, z+4),line, font=fontt, fill=shadowcolor,align = 'center')
		# 	draw.text((x+4, z+4), line, font=fontt, fill=shadowcolor,align = 'center')
		# 	draw.text((30,z), line, fill=color, font=fontt, align = 'center')
			
		# 	z = z + line_height
		
		
		
		b = BytesIO()
		img.save(b, format='png')
		b.seek(0)
		file = discord.File(filename="idharaa.png", fp=b)
		await ctx.send(file = file)
		del b


	# @command(name = 'whodidthis')
	# @cooldown(2, 60, BucketType.user)
	# async def whodidthis(self,ctx, user:discord.Member):
	# 	img_url = user.avatar_url_as(format="png") # try all three
	# 	response = requests.get(img_url)
	# 	avatar = Image.open(BytesIO(response.content))
	# 	base = Image.open('data/images/whodidthis.bmp')
	# 	avatar = avatar.resize((720, 405)).convert('RGBA')
	# 	base.paste(avatar, (0, 159), avatar)
	# 	base = base.convert('RGBA')
	# 	b = BytesIO()
	# 	base.save(b, format='png')
	# 	b.seek(0)
	# 	file = discord.File(filename="whodidthis.png", fp=b)
	# 	await ctx.send(file = file)

	@command(name = 'banner', description  = 'check how your custom banner looks', usage  = '+banner <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def banner(self,ctx, user: discord.Member = None):
		check = db.field("SELECT Custombanner FROM permission WHERE guildId = ?", ctx.guild.id)
		if check is not None :
			try:
				async with aiohttp.ClientSession() as session:
					async with session.get(f"{check}") as resp:
						if resp.status != 200:
							return await ctx.send('Could not download file...')
						data = io.BytesIO(await resp.read())
						img1 = Image.open(data)
				
						img1 = img1.resize((1920,843)).convert('RGBA')
						img2 =Image.open('./data/images/custom_temp.png')
						img2 = img2.convert('RGBA')
						user = user or ctx.author
						img_url = user.avatar_url_as(format="png", size=256) # try all three
						async with aiohttp.ClientSession() as session:
							async with session.get(f"{img_url}") as resp:
								if resp.status != 200:
									return await ctx.send('Could not download file...')
								data = BytesIO(await resp.read())
								img = Image.open(data)
								
								img = img.resize((374, 374))
								mask = Image.new('L', img.size, 0)
								draw = ImageDraw.Draw(mask)
								draw.ellipse((0, 0) + img.size, fill=255)
								output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
								output.putalpha(mask)
								img2.paste(output, (771, 65), output.convert('RGBA'))
								
								draw = ImageDraw.Draw(img2)
								fontbig = ImageFont.truetype("./data/ruso.ttf", 100)
								font = ImageFont.truetype("./data/ruso.ttf",80)
								Fontt= ImageFont.truetype("./data/ruso.ttf",70)
								shadowcolor = 'black'
								x,y = 720,485
								draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
								draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
								draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
								draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)

								draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
								draw.text((750, 620),f"{user}", (255, 255, 255), font=font)
								draw.text((750, 740),f"{len(ctx.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)
								# img1 = img1.resize((1750,900)).convert('RGBA')
								# img2 = img2.resize((1350,700)).convert('RGBA')
								img1.paste(img2,(0,0), img2)
								img1.convert('RGBA')
								b = BytesIO()
								img1.save(b, format='png')
								b.seek(0)
								file = discord.File(filename="banner.png", fp=b)
								await ctx.send(file = file)

			except aiohttp.InvalidURL:
				await ctx.send('custom banner saved by you is not valid please change it')

	@command(name = 'wholesome', description = 'try different wholesome filters', usage = '+wholesome <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def wholesome(self,ctx, user:discord.Member = None):
		
		if user == None and ctx.message.attachments:
			attachment_url = ctx.message.attachments[0].url
			img_url = attachment_url 
		elif user != None and not ctx.message.attachments:
			
			img_url = user.avatar_url_as(format="png")
		else :
			entity =  ctx.command
			p = await HelpPaginator.from_command(ctx, entity)
			return



		
		  # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				avatar = Image.open(data)
				files = os.listdir("./data/wholesome")
				index = random.randrange(0, len(files))
				base = Image.open(f'./data/wholesome/{files[index]}')
				# base = Image.open('data/images/wholesome3.png')
				# avatar = avatar.resize(base.size).convert('RGBA')
				base = base.resize(avatar.size).convert('RGBA')
				avatar.paste(base,(0,0), base)
				avatar = avatar.convert('RGBA')
				b = BytesIO()
				avatar.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="wholesome.png", fp=b)
				await ctx.send(file = file)
				del b

	@command(name = 'discord', description = 'full chutkulebaazi command hai yeh', usage = '+discord <user> <text>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def _discord(self,ctx, user:discord.Member , *, text:str):
		''' +discord @Rohan#7140 mai toh pagal hu '''
		try:
			await ctx.message.delete()
		except discord.Forbidden:
			pass
		img_url = user.avatar_url_as(format="png", size=256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				avatar = Image.open(data)
				avatar = avatar.convert('RGBA').resize((50,50))
				mask = Image.new('L', avatar.size, 0)
				draw = ImageDraw.Draw(mask)
				draw.ellipse((0, 0) + avatar.size, fill=255)
				output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
				output.putalpha(mask)
				base = Image.open('data/images/discord.png')
				base.paste(output,(20,10), output)
				fontbig = ImageFont.truetype("./data/discord.ttf", 23)
				draw = ImageDraw.Draw(base)
				draw.text((80, 7), f"{user.display_name}", fill = f'{user.colour}', font=fontbig)
				line_height = fontbig.getsize(f'{user.display_name}')[0]
				font = ImageFont.truetype("./data/discord.ttf", 15)
				draw = ImageDraw.Draw(base)
				now = datetime.now()
				current_time = now.strftime("%H:%M")
				font2 = ImageFont.truetype("./data/discord.ttf", 20)

				draw.text((90 + line_height, 12), f"Today at {current_time} PM", fill = "#72767d", font=font)
				image_size = ((300,200))
				lines = self.text_wrap(text, font, image_size[0])
				z= 35

				line_height = font.getsize('hg')[1]
				for line in lines:
					draw.text((80,z), line, fill='white', font=font2)
					z = z + line_height
					
				base = base.convert('RGBA')
				b = BytesIO()
				base.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="discord.png", fp=b)
				await ctx.send(file = file)
				del b


	@command(name = 'rip', description = 'yaha koi maar gya aur tu description padh rha', usage = '+rip <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def rip(self,ctx, user:discord.Member = None):
		user = user or ctx.author 
		img_url = user.avatar_url_as(format="png",size =256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				avatar = Image.open(data)
				base = Image.open('data/images/rip.png')
				avatar = avatar.resize((70,70)).convert('RGBA')
				base.paste(avatar, (85,180), avatar)
				base = base.convert('RGBA')
				if len(user.name)< 9 :
					fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 35)
					draw = ImageDraw.Draw(base)
					draw.text((55, 130), f"{user.name}", fill = 'black', font=fontbig)
				elif len(user.name)> 9:
					fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 20)
					draw = ImageDraw.Draw(base)
					draw.text((30, 140), f"{user.name}", fill = 'black', font=fontbig)


				
				b = BytesIO()
				base.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="rip.png", fp=b)
				await ctx.send(file = file)
				del b


	@command(name = 'affect', description = 'it wont affect my baby', usage = '+affect <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def affect(self,ctx, user:discord.Member =None):
		if user == None and ctx.message.attachments:
			attachment_url = ctx.message.attachments[0].url
			img_url = attachment_url 
		elif user != None and not ctx.message.attachments:
			
			img_url = user.avatar_url_as(format="png")
		else :
			entity =  ctx.command
			p = await HelpPaginator.from_command(ctx, entity)
			return

		# img_url = user.avatar_url_as(format="png") # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				avatar = Image.open(data)
				avatar = avatar.resize((200, 157)).convert('RGBA')
				base = Image.open('data/images/affect.bmp')
				base.paste(avatar, (180, 383, 380, 540), avatar)
				base = base.convert('RGB')
				b = BytesIO()
				base.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="affect.png", fp=b)
				await ctx.send(file = file)
				del b

	# @command(name = 'hot')
	# async def hot(self,ctx, user:discord.Member):
	# 	img_url = user.avatar_url_as(format="png") # try all three
	# 	response = requests.get(img_url)
	# 	avatar = Image.open(BytesIO(response.content))
	# 	avatar = avatar.convert('RGBA')
	# 	base = Image.open('data/images/hot.png')
	# 	smith = Image.open('data/images/smith.png')
	# 	smith =smith.resize((400,200))
	# 	base = base.convert('RGBA')
	# 	avatar.paste(base, (0,0), base)
	# 	avatar = avatar.convert('RGBA')
	# 	avatar = avatar.resize((400,200))
	
	# 	def get_concat_v(smith,avatar):
	# 		dst = Image.new('RGB', (smith.width, smith.height + avatar.height))
	# 		dst.paste(smith, (0, 0))
	# 		dst.paste(avatar, (0, smith.height))
	# 		return dst
	# 	b = BytesIO()
	# 	get_concat_v(smith, avatar).save(b, format='png',quality = 95)
	# 	b.seek(0)
	# 	file = discord.File(filename="hot.png", fp=b)
	# 	await ctx.send(file = file)



	@command(name = 'always', description ='always has been', usage = '+always <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def always(self,ctx, user:discord.Member , *, text:str=None):
		img_url = user.avatar_url_as(format="png", size=256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				avatar = Image.open(data)
				avatar = avatar.convert('RGBA').resize((512,512))
				mask = Image.new('L', avatar.size, 0)
				draw = ImageDraw.Draw(mask)
				draw.ellipse((0, 0) + avatar.size, fill=255)
				output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
				output.putalpha(mask)
				base = Image.open('data/images/always.png')
				fontbig = ImageFont.truetype("./data/discord.ttf", 50)
				draw = ImageDraw.Draw(base)
				draw.text((700, 400), f"Wait, It's all {user.name}", fill = 'white', font=fontbig)
				fontbi = ImageFont.truetype("./data/discord.ttf", 80)
				draw.text((1300, 10), f"Always has been", fill = 'white', font=fontbi)
				draw = ImageDraw.Draw(base)
				base.paste(output, (175,195), output)
				base = base.convert('RGBA')
				b = BytesIO()
				base.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="always.png", fp=b)
				await ctx.send(file = file)
				del b
	
	@command(name = 'fc', description = 'friendship cancel ', usage = '+fc <user1> <user2>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def fc(self,ctx, user:discord.Member, user2:discord.Member, user3:discord.Member = None):
		user3  = user3 or ctx.author
		img_url = user.avatar_url_as(format="png", size=256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				avatar = Image.open(data)
				avatar = avatar.resize((320,430)).convert('RGBA')
				avatarr= avatar.copy()
				avatarr = avatarr.resize((250,470)).convert('RGBA')

		img_url2 = user2.avatar_url_as(format="png", size=256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url2}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data2 = BytesIO(await resp.read())
				avatar2 = Image.open(data2)
				avatar2 = avatar2.resize((270,270)).convert('RGBA')
		img_url3 = user3.avatar_url_as(format="png", size=256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url3}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data3 = BytesIO(await resp.read())
				avatar3 = Image.open(data3)
				avatar3 = avatar3.resize((270,270)).convert('RGBA')
				base = Image.open('data/images/friendship.png')
				base = base.resize((1024,1024)).convert('RGBA')
				base.paste(avatarr, (0,560), avatarr)
				base.paste(avatar, (720,600), avatar)
				base.paste(avatar3, (50,200), avatar3)
				base.paste(avatar2, (680,230), avatar2)
				base = base.convert('RGBA')
				draw = ImageDraw.Draw(base)
				w, h = 200, 1000
				shape = [(40, 800), (w - 10, h - 10)] 
				draw.line(shape, fill ="green", width = 30) 
				x, y = 40, 1000
				shapew = [(200,800), (x - 10, y - 10)] 
				draw.line(shapew, fill ="green", width = 30)
				a, b = 780, 1000
				shapeww = [(920,800), (a - 10, b - 10)] 
				draw.line(shapeww, fill ="green", width = 30)
				c, d = 920, 1000
				shapeww = [(780,800), (c - 10, d - 10)] 
				draw.line(shapeww, fill ="green", width = 30)


				fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 100)
				font = ImageFont.truetype("./data/OpenSans-Regular.ttf", 65)

				if len(user.name)> 6 :
					fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 70)
					draw.text((700, 20), f"{user.name}", fill = 'green', font=fontbig)
					
				else :
					fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 100)
					draw.text((700, 20), f"{user.name}", fill = 'green', font=fontbig)

				draw.text((700, 20), f"{user.name}", fill = 'green', font=fontbig)
				if len(user2.name)> 9 :
					font = ImageFont.truetype("./data/OpenSans-Regular.ttf", 52)
					draw.text((345, 290), f"{user2.name}", fill = 'green', font=font)
				else :
					font = ImageFont.truetype("./data/OpenSans-Regular.ttf", 65)
					draw.text((345, 290), f"{user2.name}", fill = 'green', font=font)
				b = BytesIO()
				base.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="friendship.png", fp=b)
				await ctx.send(file = file)
				del b







	@command(name = 'batslap', description  = 'batslap someone', usage = '+batslap <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def batslap(self , ctx, user1:discord.Member  , user2:discord.Member = None):
		user2 = user2 or ctx.author
		img_url = user1.avatar_url_as(format="png") # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
		img_url2 = user2.avatar_url_as(format="png") # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url2}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data2 = BytesIO(await resp.read())
		
				avatar = Image.open(data)
				avatar2 = Image.open(data2)
				base = Image.open('data/images/batslap.bmp').resize((1000, 500)).convert('RGBA')
				avatar = avatar.resize((220, 220)).convert('RGBA')
				avatar2 = avatar2.resize((200, 200)).convert('RGBA')
				base.paste(avatar, (580, 260), avatar)
				base.paste(avatar2, (350, 70), avatar2)
				base = base.convert('RGB')
				b = BytesIO()
				base.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="slap.png", fp=b)
				await ctx.send(file = file)
				del b
		
	# @command(name = 'insta', description  = "Check out your/someone else's Insta", usage = '+insta <username>')
	# @custom_check()
	# @cooldown(3, 60, BucketType.user)
	# async def insta(self, ctx, username):
		
	# 	# try:
	# 		url = f'https://apis.duncte123.me/insta/{username}'
	# 		async with aiohttp.ClientSession() as session:
	# 			async with session.get(url) as response:
	# 				r = await response.json()
	# 				data = r['user']
	# 				username = data["username"]
	# 				followers = data["followers"]["count"]
	# 				following = data["following"]["count"]
	# 				uploads = data["uploads"]["count"]
	# 				biography = data["biography"]
	# 				private = data["is_private"]
	# 				verified = data["is_verified"]
	# 				embed = discord.Embed(title=f'Insta Details: {username}')
	# 				embed.add_field(name='Bio', value=biography + '\u200b', inline=False)
	# 				embed.add_field(name='Private Status', value=private, inline=False)
	# 				embed.add_field(name='Verified Status', value=verified, inline=False)
	# 				embed.add_field(name='Followers', value=followers, inline=False)
	# 				embed.add_field(name='Following', value=following, inline=False)
	# 				embed.add_field(name='Posts', value=uploads, inline=False)
	# 				await ctx.send(embed=embed)
	# 	# except:
	# 	# 	await ctx.send('enter valid username')



	


	@command(name = 'dpbattle', description  = 'discord dp battle', usage = '+dpbattle <time> <user1> <user2>')#new
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def dp(self , ctx,time : TimeConverter, user1:discord.Member  , user2:discord.Member = None):
		'''+dpbattle 1h @Rohan#7140'''
		try:
			user2 = user2 or ctx.author
			img_url = user1.avatar_url_as(format="png") # try all three
			async with aiohttp.ClientSession() as session:
				async with session.get(f"{img_url}") as resp:
					if resp.status != 200:
						return await ctx.send('Could not download file...')
					data = BytesIO(await resp.read())
			img_url2 = user2.avatar_url_as(format="png") # try all three
			async with aiohttp.ClientSession() as session:
				async with session.get(f"{img_url2}") as resp:
					if resp.status != 200:
						return await ctx.send('Could not download file...')
					data2 = BytesIO(await resp.read())
			
					avatar = Image.open(data)
					avatar2 = Image.open(data2)
					base = Image.open('data/images/dp.png').convert('RGBA')
					avatar = avatar.resize((256,256)).convert('RGBA')
					avatar2 = avatar2.resize((256,256)).convert('RGBA')
					base.paste(avatar, (14, 133), avatar)
					base.paste(avatar2, (373, 133), avatar2)
					draw = ImageDraw.Draw(base)
					font = ImageFont.truetype("./data/discord.ttf", 30)
					draw.text((20, 400), f"{user1.name}", fill = 'black', font=font)
					draw.text((385, 400), f"{user2.name}", fill = 'black', font=font)

					base = base.convert('RGB')
					b = BytesIO()
					base.save(b, format='png')
					b.seek(0)
					file = discord.File(filename="dpbattle.png", fp=b)
					await ctx.send(file = file)
					del b

					embed = discord.Embed(description  =   '\uFEFF' , colour = ctx.author.colour, timestamp = datetime.utcnow())
					embed.set_author(name = f'{ctx.guild.name} dp battle', icon_url  = ctx.guild.icon_url)
					embed.add_field(name  = '**Contestants : **', value  = f'🇦 `{user1.name}` \n\n 🇧 `{user2.name}`', inline =False)
					embed.add_field(name  = '**Time Duration : **', value  = f'{int(time)} seconds', inline =False)
					
					message = await ctx.send(embed=embed)
					for emoji in numbers:
						await message.add_reaction(emoji)
						
					self.dps.append((message.channel.id, message.id))
					self.bot.scheduler.add_job(self.complete_dp, "date", run_date=datetime.now()+timedelta(seconds =time),args=[message.channel.id, message.id])



					
		except :
			await ctx.send(f'Some error occured type {ctx.prefix}help to know more about the command')


	async def complete_dp(self, channel_id, message_id):
		try :
			message = await self.bot.get_channel(channel_id).fetch_message(message_id)
		
			most_voted = max(message.reactions, key=lambda r: r.count)
			for reaction in message.reactions :
				if str(reaction.emoji) =='🇦':
					x = reaction.count
				if str(reaction.emoji) =='🇧':
					y = reaction.count
			if x == y :
				await message.channel.send(" The results are in and oops it's a tie ")
			else:
				await message.channel.send(f"The results are in and option {most_voted.emoji} won with total of {most_voted.count-1:,} votes!")

			self.dps.remove((message.channel.id, message.id))
			await message.delete()
		except discord.NotFound :
			pass
		



	
	



	# @command(name = 'smith')
	# @cooldown(2, 60, BucketType.user)
	# async def smith(self,ctx, *, text:str):
	# 	text = text.split("|",1)
	# 	img = Image.open('./data/images/willsmith.jpg')
	# 	img = img.resize((1024,1024))
		
	# 	font_file_path = './data/OpenSans-Regular.ttf'

	# 	fontt = ImageFont.truetype(font_file_path)
	# 	label_font, label_text = auto_text_size(text[0], fontt, 980, font_scalar=0.99)
	# 	label_font2, label_text2 = auto_text_size(text[1], fontt, 980, font_scalar=0.99)
	# 	color = 'white'
	# 	draw = ImageDraw.Draw(img)

			

	
	# 	draw.text((50,30), label_text, fill=color, font=label_font, align = 'center')
	# 	draw.text((20,800), label_text2, fill=color, font=label_font2, align = 'center')
	# 	# font = ImageFont.truetype(font_file_path, size=70, encoding="unic")
	# 	# fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 90)
	# 	# draw = ImageDraw.Draw(img)
	# 	# # draw.text((370, 215), f"{text[0]}", fill = 'black', font=fontbig)
	# 	# # draw.text((80, 600), f"{text[1]}", fill = 'black', font=fontbig)
	# 	# z = 20
	# 	# y = 750
	# 	# image_size = ((1024,1024))
	# 	# lines = self.text_wrap(text[0], fontbig, image_size[0])
	# 	# liness = self.text_wrap(text[1], fontbig, image_size[0])
	# 	# line_height = fontbig.getsize('hg')[1]
	# 	# for line in lines:
	# 	# 	draw.text((50,z), line, fill='white', font=fontbig)
	# 	# 	z = z + line_height
			

	# 	# for line in liness:
	# 	#  	draw.text((20,y), line, fill='white', font=fontbig)
	# 	#  	y = y + line_height
		
	# 	# draw.text((600,z),f'{text[1]}' ,fill='blue', font=font)
	
		
	# 	b = BytesIO()
	# 	img.save(b, format='png')
	# 	b.seek(0)
	# 	file = discord.File(filename="smith.png", fp=b)
	# 	await ctx.send(file = file)
	

	

	@command(name = 'changemymind', description  = 'try to change my mind', usage = '+changemymind <text>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def changemymind(self,ctx, *, text):
		base = Image.open('data/images/changemymind.bmp').convert('RGBA')
		# text_layer = Image.new('RGBA', base.size)
		image_size = ((380,380))
		
		text_layer = Image.new('RGBA', base.size)
		draw = ImageDraw.Draw(text_layer)
		z= 280
		
		fontbig = ImageFont.truetype("./data/OpenSans-Regular.ttf", 25)
		lines = self.text_wrap(text, fontbig, image_size[0])

		line_height = fontbig.getsize('hg')[1]
		for line in lines:
			draw.text((280,z), line, fill='black', font=fontbig)
			z = z + line_height
		text_layer = text_layer.rotate(23, resample=Image.BICUBIC)
		base.paste(text_layer, (0, 0), text_layer)
		base = base.convert('RGB')
		b = BytesIO()
		base.save(b, format='jpeg')
		b.seek(0)
		file = discord.File(filename="changemymind.jpeg", fp=b)
		await ctx.send(file = file)
		del b


	

	



	

				


		

	# @command(name = 'o')
	# async def o(self,ctx):
	# 	img = Image.open(f'./data/images/bhangi.png')
	# 	bcg = Image.open(f'./data/images/test2.gif')
		
	# 	frames = []
	# 	for frame in ImageSequence.Iterator(bcg):
	# 		frame = frame.copy()
	# 		img = img.resize((200, 200))
	# 		mask = Image.new('L', img.size, 100)
	# 		draw = ImageDraw.Draw(mask)
	# 		draw.ellipse((0, 0) + img.size, fill=255)
	# 		output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
		
	# 		output.putalpha(mask)
			
	# 		frame.paste(output, (400, 35), output.convert('RGBA'))
	# 		frames.append(frame)
	# 		frames[0].save('output.gif', save_all=True, append_images=frames[1:])
		




	# @command(name = 'mergegif')
	# async def mergegif(self, ctx):
	# 	im1 = Image.open('./data/images/card7.png')
	# 	# im2 = Image.open('./data/images/croppedgif.png')
	# 	# # kar = (im2.size[0] * 2)
	# 	# # im2.resize((kar), Image.ANTIALIAS)
	# 	# im2.save("./data/images/croppedgif.png" 
	# 	im2 = Image.open("./data/images/croppedgif.png")
	# 	size = 2048,2048
	# 	im2.thumbnail(size)
	# 	im2.save("./data/images/croppedgif.png")
	# 	im3 = Image.open("./data/images/croppedgif.png")
	# 	mask_im = Image.new("L",im3.size, 0)
	# 	draw = ImageDraw.Draw(mask_im)
	# 	draw.ellipse([(0, 0), im3.size], fill=255)
	# 	mask_im.save('./data/images/mask_circlegif.png', quality=95)
	# 	back_im = im1.copy()
	# 	back_im.paste(im3,(755,50), mask_im)
	# 	back_im = back_im.convert("RGB")
	# 	back_im.save('./data/images/dangerchamaargif.png', quality=95)
	# 	img = Image.open('./data/images/dangerchamaargif.png')
	# 	draw = ImageDraw.Draw(img)
	# 	fontbig = ImageFont.truetype("./data/ruso.ttf", 100)
	# 	font = ImageFont.truetype("./data/ruso.ttf",70)
	# 	Fontt= ImageFont.truetype("./data/ruso.ttf",65)
	# 	draw.text((720, 485), f"WELCOME", (255, 255, 255), font=fontbig)
	# 	draw.text((750, 620),f"{ctx.author}", (255, 255, 255), font=font)
	# 	draw.text((750, 720),f"{len(ctx.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)
	
	# 	img.save('./data/images/dangerchamaarrgif.png')

	# 	await ctx.send(file = discord.File('./data/images/dangerchamaarrgif.png'))



	@command(name = 'welcomecard', description  = 'check how your welcome card looks like', usage = '+welcomecard <card> <user>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def welcomecard(self, ctx, name , user :discord.Member)-> bytes:
		'''+welcomecard card19 @Rohan#7140'''
		# avatar_url = user.avatar_url_as(format="png", size=512)
		# async with self.session.get(f'{avatar_url}') as response:
		# 	avatar_bytes = await response.read()
		# 	img = Image.open(BytesIO(avatar_bytes))
		# 	# size = 411,411
		# 	# img.thumbnail(size)

		# try :

		
		img_url = user.avatar_url_as(format="png", size=256) # try all three
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{img_url}") as resp:
				if resp.status != 200:
					return await ctx.send('Could not download file...')
				data = BytesIO(await resp.read())
				img = Image.open(data)
				bcg = Image.open(f'./data/templates/{name}.png')
				img = img.resize((374, 374))
				mask = Image.new('L', img.size, 0)
				draw = ImageDraw.Draw(mask)
				draw.ellipse((0, 0) + img.size, fill=255)
				output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
				output.putalpha(mask)
				bcg.paste(output, (774, 70), output.convert('RGBA'))
				
				draw = ImageDraw.Draw(bcg)
				fontbig = ImageFont.truetype("./data/ruso.ttf", 110)
				font = ImageFont.truetype("./data/ruso.ttf",80)
				Fontt= ImageFont.truetype("./data/ruso.ttf",70)
				shadowcolor = 'black'
				x,y = 720,485
				# draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
				# draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
				# draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
				# draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
				W, H = (1920,843)
				w, h = draw.textsize('WELCOME')
				draw.text(((W-w)/2.7,(H-h)/1.7), f'WELCOME', fill="white", font  = fontbig, align="center")
				w, h = draw.textsize(f'{user}')


				# draw.text(((W-w)/2.5,(H-h)/1.4), f'{user}', fill="white", font  = font, align="center")
				

				# draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
				if 10 > len(user.name)>= 7 :
					draw.text((690, 620),f"{user}", (255, 255, 255), font=font, align =  "center")
				elif 12 > len(user.name)>= 10 :
					draw.text((630, 620),f"{user}", (255, 255, 255), font=font, align =  "center")

				elif 16 > len(user.name)>= 12 :
					draw.text((570, 620),f"{user}", (255, 255, 255), font=font, align =  "center")
				
				elif 19 > len(user.name)>= 16 :
					draw.text((510, 620),f"{user}", (255, 255, 255), font=font, align =  "center")

				elif  len(user.name) < 7 :
					draw.text((740, 620),f"{user}", (255, 255, 255), font=font, align =  "center")
				else  :
				    draw.text((450, 620),f"{user}", (255, 255, 255), font=font, align =  "center")

				if 1000>len(ctx.guild.members) > 99 :
					draw.text((720, 740),f"{len(ctx.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

				elif 10000 >len(ctx.guild.members) > 999 :
					draw.text((700, 740),f"{len(ctx.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

				elif 100000 >len(ctx.guild.members) > 9999 :
					draw.text((670, 740),f"{len(ctx.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

				elif len(ctx.guild.members) > 99999 :
					draw.text((630, 740),f"{len(ctx.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

				else :
					
					draw.text((740, 740),f"{len(ctx.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)


				

					

				
				
				b = BytesIO()
				bcg.save(b, format='png')
				b.seek(0)
				file = discord.File(filename="welcome.png", fp=b)
				await ctx.send(file = file)
				del b
		# except :
		# 	await ctx.send('enter a valid card number \n there are total 35cards')


	@command(name = 'modi', description = 'sends random modi memes', usage  = '+modi')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	
	async def modi(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://namo-memes.herokuapp.com/memes/1") as res:

	
				link = await res.json()


				url = [i for i in link]
				data = url[0]
				image = data["url"]
				
				embed = discord.Embed()
				embed.set_image(url=image)
				
				await ctx.send(embed=embed)


	# @command(name = 'weather', description = 'check weather', usage  = '+weather <location>')
	# @custom_check()
	# @cooldown(2, 60, BucketType.user)
	# async def weather (self,ctx, *, location):
	# 	location = location.replace(" " , "+")
	# 	url = f"https://www.metaweather.com/api/location/search/?query={location}"
		
	# 	link = await self.session.get(url)
	# 	link = await link.json()
		
	# 	convert = [i for i in link]
	# 	data = convert[0]
	# 	title = data["title"]
	# 	loc_type = data['location_type']
	# 	lat = data['latt_long']
	# 	woeid = data['woeid']

	# 	wea_link = f"https://www.metaweather.com/api/location/{woeid}"
	# 	wea_link = await self.session.get(wea_link)
	# 	wea_link = await wea_link.json()
		
	# 	weather = wea_link["consolidated_weather"]
	# 	stats = [i for i in weather]
		
	# 	info = stats[0]
		
	# 	weather_state_name = info["weather_state_name"]
	# 	wind_direction_compass = info["wind_direction_compass"]
	# 	applicable_date = info["applicable_date"]
	# 	min_temp = info["min_temp"]
	# 	max_temp = info["max_temp"]
	# 	the_temp = info["the_temp"]
	# 	wind_speed = info["wind_speed"]
	# 	air_pressure = info["air_pressure"]
	# 	humidity = info["humidity"]
	# 	visibility = info["visibility"]

	# 	embed = discord.Embed()
	# 	embed.add_field(name = "Location:" , value = title)
	# 	embed.add_field(name = "Location Type:" , value = loc_type)
	# 	embed.add_field(name = "Lattitude and Longitude" , value = lat)
	# 	embed.add_field(name = "Weather:" , value = weather_state_name)
	# 	embed.add_field(name = "Wind direction:" , value = wind_direction_compass)
	# 	embed.add_field(name = "Current Temperature:" , value = f"{the_temp}°C")
	# 	embed.add_field(name = "Minimum Temperature:" , value = f"{min_temp}°C")
	# 	embed.add_field(name = "Maximum Temperature:" , value = f"{max_temp}°C")
	# 	embed.add_field(name = "Air Pressure:" , value = air_pressure)
	# 	embed.add_field(name = "Humidity:" , value = humidity)
	# 	embed.add_field(name = "Visibility:" , value = visibility)
	# 	embed.set_footer(text=applicable_date)

	# 	await ctx.send(embed=embed)


	

	@command(name  = 'show', description  = 'get detail info about a show', usage  = "+show <show>")
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def show(self, ctx, *,show):
		try :

			show = show.replace(" ","+")
			async with aiohttp.ClientSession() as cs:
				async with cs.get(f"http://api.tvmaze.com/search/shows?q={show}") as res:
			
		
			
					url= await res.json()
					

					data = [i for i in url]
					data = data[0]
					show = data["show"]
					name = show["name"]
					typee = show["type"]
					lang = show["language"]
					genre = show["genres"]
					status = show["status"]
					premiere = show["premiered"]
					
					site = show['officialSite']
					
					rating = show['rating']
					avg = rating['average']
					image = show['image']
					thumb = image['medium']
					img = image['original']
					summary = show['summary']

					embed = discord.Embed()
					embed.add_field(name = "Name:" , value  = name)
					embed.add_field(name = "Rating:" , value  = avg)
					embed.add_field(name = "Type of show:" , value  = typee)
					embed.add_field(name = "Orignal Language:" , value  = lang)
					embed.add_field(name = "Genre:" , value  = genre)
					embed.add_field(name = "Status" , value  = status)
					embed.add_field(name = "Premiered on:" , value  = premiere)
					embed.add_field(name = "Official site:" , value  = site)
					embed.add_field(name = "Summary" , value  = summary, inline = False)

					
					embed.set_thumbnail(url=thumb)

					await ctx.send(embed=embed)

		except :
			await ctx.send('enter a valid show')


# if customwc is not None:
#             if wcmessage != None and channell !=None :

        
#                 a = len(member.guild.members)
#                 b = member.mention

#                 info = {'user': b , "membercount" : a}


#                 await self.bot.get_channel(channell).send(wcmessage.format(**info))


		
	
	@Cog.listener()
	async def on_member_join(self, member):


		customwc = db.field("SELECT Customwelcome FROM permission WHERE guildId = ?", member.guild.id)
		wcmessage = db.field("SELECT Wcmessage FROM guilds WHERE GuildID = ?", member.guild.id)
		wcchannel = db.field("SELECT Wcchannel FROM guilds WHERE GuildID = ?", member.guild.id)
		bannersetting = db.field("SELECT Bannersetting FROM permission WHERE guildId = ?", member.guild.id)
        

		custombanner = db.field("SELECT Custombanner FROM permission WHERE guildId = ?", member.guild.id)
		wccard = db.field("SELECT Welcomecard FROM permission WHERE guildId = ?", member.guild.id)
		try:
			if customwc !=None and wccard !=None :
				if custombanner !=None and bannersetting != None :
					if wcmessage !=None and wcchannel != None :
						try:
							async with aiohttp.ClientSession() as session:
								async with session.get(f"{custombanner}") as resp:
									if resp.status != 200:
										pass						
									data = io.BytesIO(await resp.read())
									img1 = Image.open(data)
									img1 = img1.resize((1920,843)).convert('RGBA')
									img2 =Image.open('./data/images/custom_temp.png')
									img2 = img2.convert('RGBA')
									img_url =  member.avatar_url_as(format="png", size=256) # try all three
									async with aiohttp.ClientSession() as session:
										async with session.get(f"{img_url}") as resp:
											if resp.status != 200:
												return 
											dataa = BytesIO(await resp.read())
											img = Image.open(dataa)
											
											img = img.resize((374, 374))
											mask = Image.new('L', img.size, 0)
											draw = ImageDraw.Draw(mask)
											draw.ellipse((0, 0) + img.size, fill=255)
											output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
											output.putalpha(mask)
											img2.paste(output, (771, 63), output.convert('RGBA'))
											
											draw = ImageDraw.Draw(img2)

											fontbig = ImageFont.truetype("./data/ruso.ttf", 110)
											font = ImageFont.truetype("./data/ruso.ttf",80)
											Fontt= ImageFont.truetype("./data/ruso.ttf",70)
											shadowcolor = 'black'
											x,y = 720,485
											# draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
											W, H = (1920,843)
											w, h = draw.textsize('WELCOME')
											draw.text(((W-w)/2.7,(H-h)/1.7), f'WELCOME', fill="white", font  = fontbig, align="center")
											


											# draw.text(((W-w)/2.5,(H-h)/1.4), f'{user}', fill="white", font  = font, align="center")
											

											# draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
											if 10 > len(member.name)>= 7 :
												draw.text((690, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
											elif 12 > len(member.name)>= 10 :
												draw.text((630, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

											elif 16 > len(member.name)>= 12 :
												draw.text((570, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
											
											elif 19 > len(member.name)>= 16 :
												draw.text((510, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

											elif  len(member.name) < 7 :
												draw.text((740, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
											else  :
												draw.text((450, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

											if 1000>len(member.guild.members) > 99 :
												draw.text((720, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

											elif 10000 >len(member.guild.members) > 999 :
												draw.text((700, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

											elif 100000 >len(member.guild.members) > 9999 :
												draw.text((670, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

											elif len(member.guild.members) > 99999 :
												draw.text((630, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

											else :
												
												draw.text((740, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)
											# fontbig = ImageFont.truetype("./data/ruso.ttf", 100)
											# font = ImageFont.truetype("./data/ruso.ttf",80)
											# Fontt= ImageFont.truetype("./data/ruso.ttf",70)
											# shadowcolor = 'black'
											# x,y = 720,485
											# draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)

											# draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
											# draw.text((680, 620),f"{member}", (255, 255, 255), font=font)
											# draw.text((730, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)
											# img1 = img1.resize((1750,900)).convert('RGBA')
											# img2 = img2.resize((1350,700)).convert('RGBA')
											img1.paste(img2,(0,0), img2)
											img1.convert('RGBA')
											b = BytesIO()
											img1.save(b, format='png')
											b.seek(0)
											file = discord.File(filename="banner.png", fp=b)
											a = len(member.guild.members)
											c = member.mention
											info = {'user': c , "membercount" : a}
											
											await self.bot.get_channel(wcchannel).send(wcmessage.format(**info), file = file)
											
						except aiohttp.InvalidURL:
							pass

					elif wcmessage == None and wcchannel != None :

						try:
							async with aiohttp.ClientSession() as session:
								async with session.get(f"{custombanner}") as resp:
									if resp.status != 200:
										pass						
									data = io.BytesIO(await resp.read())
									img1 = Image.open(data)
									img1 = img1.resize((1920,843)).convert('RGBA')
									img2 =Image.open('./data/images/custom_temp.png')
									img2 = img2.convert('RGBA')
									img_url =  member.avatar_url_as(format="png", size=256) # try all three
									async with aiohttp.ClientSession() as session:
										async with session.get(f"{img_url}") as resp:
											if resp.status != 200:
												return 
											dataa = BytesIO(await resp.read())
											img = Image.open(dataa)
											
											img = img.resize((374, 374))
											mask = Image.new('L', img.size, 0)
											draw = ImageDraw.Draw(mask)
											draw.ellipse((0, 0) + img.size, fill=255)
											output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
											output.putalpha(mask)
											img2.paste(output, (771, 63), output.convert('RGBA'))
											
											draw = ImageDraw.Draw(img2)

											fontbig = ImageFont.truetype("./data/ruso.ttf", 110)
											font = ImageFont.truetype("./data/ruso.ttf",80)
											Fontt= ImageFont.truetype("./data/ruso.ttf",70)
											shadowcolor = 'black'
											x,y = 720,485
											# draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
											W, H = (1920,843)
											w, h = draw.textsize('WELCOME')
											draw.text(((W-w)/2.7,(H-h)/1.7), f'WELCOME', fill="white", font  = fontbig, align="center")


											# draw.text(((W-w)/2.5,(H-h)/1.4), f'{user}', fill="white", font  = font, align="center")
											

											# draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
											if 10 > len(member.name)>= 7 :
												draw.text((690, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
											elif 12 > len(member.name)>= 10 :
												draw.text((630, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

											elif 16 > len(member.name)>= 12 :
												draw.text((570, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
											
											elif 19 > len(member.name)>= 16 :
												draw.text((510, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

											elif  len(member.name) < 7 :
												draw.text((740, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
											else  :
												draw.text((450, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

											if 1000>len(member.guild.members) > 99 :
												draw.text((720, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

											elif 10000 >len(member.guild.members) > 999 :
												draw.text((700, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

											elif 100000 >len(member.guild.members) > 9999 :
												draw.text((670, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

											elif len(member.guild.members) > 99999 :
												draw.text((630, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

											else :
												
												draw.text((740, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)



											# fontbig = ImageFont.truetype("./data/ruso.ttf", 100)
											# font = ImageFont.truetype("./data/ruso.ttf",80)
											# Fontt= ImageFont.truetype("./data/ruso.ttf",70)
											# shadowcolor = 'black'
											# x,y = 720,485
											# draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
											# draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)

											# draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
											# draw.text((680, 620),f"{member}", (255, 255, 255), font=font)
											# draw.text((730, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)
											# # img1 = img1.resize((1750,900)).convert('RGBA')
											# # img2 = img2.resize((1350,700)).convert('RGBA')
											img1.paste(img2,(0,0), img2)
											img1.convert('RGBA')
											b = BytesIO()
											img1.save(b, format='png')
											b.seek(0)
											file = discord.File(filename="banner.png", fp=b)
											
											await self.bot.get_channel(wcchannel).send(file = file)
											
						except aiohttp.InvalidURL:
							pass


				else :
					if wcmessage !=None and wcchannel != None :
						img_url = member.avatar_url_as(format="png", size=256) # try all three
						async with aiohttp.ClientSession() as session:
							async with session.get(f"{img_url}") as resp:
								if resp.status != 200:
									return 
								data = BytesIO(await resp.read())
								img = Image.open(data)
								files = os.listdir("./data/templates")
								index = random.randrange(0, len(files))
								bcg = Image.open(f'./data/templates/{files[index]}')
								img = img.resize((374, 374))
								mask = Image.new('L', img.size, 0)
								draw = ImageDraw.Draw(mask)
								draw.ellipse((0, 0) + img.size, fill=255)
								output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
								output.putalpha(mask)
								bcg.paste(output, (774, 70), output.convert('RGBA'))

								draw = ImageDraw.Draw(bcg)
								fontbig = ImageFont.truetype("./data/ruso.ttf", 110)
								font = ImageFont.truetype("./data/ruso.ttf",80)
								Fontt= ImageFont.truetype("./data/ruso.ttf",70)
								shadowcolor = 'black'
								x,y = 720,485
								# draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
								# draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
								# draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
								# draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
								W, H = (1920,843)
								w, h = draw.textsize('WELCOME')
								draw.text(((W-w)/2.7,(H-h)/1.7), f'WELCOME', fill="white", font  = fontbig, align="center")
								


								# draw.text(((W-w)/2.5,(H-h)/1.4), f'{user}', fill="white", font  = font, align="center")
								

								# draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
								if 10 > len(member.name)>= 7 :
									draw.text((690, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
								elif 12 > len(member.name)>= 10 :
									draw.text((630, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

								elif 16 > len(member.name)>= 12 :
									draw.text((570, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
								
								elif 19 > len(member.name)>= 16 :
									draw.text((510, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

								elif  len(member.name) < 7 :
									draw.text((740, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
								else  :
									draw.text((450, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

								if 1000>len(member.guild.members) > 99 :
									draw.text((720, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

								elif 10000 >len(member.guild.members) > 999 :
									draw.text((700, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

								elif 100000 >len(member.guild.members) > 9999 :
									draw.text((670, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

								elif len(member.guild.members) > 99999 :
									draw.text((630, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

								else :
									
									draw.text((740, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)
								
								
								b = BytesIO()
								bcg.save(b, format='png')
								b.seek(0)
								file = discord.File(filename="banner.png", fp=b)
								a = len(member.guild.members)
								c = member.mention
								info = {'user': c , "membercount" : a}
								try:
									await self.bot.get_channel(wcchannel).send(wcmessage.format(**info), file = file)
								except :
									pass
							
								

					elif wcmessage == None and wcchannel != None :
						img_url = member.avatar_url_as(format="png", size=256) # try all three
						async with aiohttp.ClientSession() as session:
							async with session.get(f"{img_url}") as resp:
								if resp.status != 200:
									return 
								data = BytesIO(await resp.read())
								img = Image.open(data)
								files = os.listdir("./data/templates")
								index = random.randrange(0, len(files))
								bcg = Image.open(f'./data/templates/{files[index]}')
								img = img.resize((374, 374))
								mask = Image.new('L', img.size, 0)
								draw = ImageDraw.Draw(mask)
								draw.ellipse((0, 0) + img.size, fill=255)
								output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
								output.putalpha(mask)
								bcg.paste(output, (774, 70), output.convert('RGBA'))

								draw = ImageDraw.Draw(bcg)
								fontbig = ImageFont.truetype("./data/ruso.ttf", 110)
								font = ImageFont.truetype("./data/ruso.ttf",80)
								Fontt= ImageFont.truetype("./data/ruso.ttf",70)
								shadowcolor = 'black'
								x,y = 720,485
								# draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
								# draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
								# draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
								# draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
								W, H = (1920,843)
								w, h = draw.textsize('WELCOME')
								draw.text(((W-w)/2.7,(H-h)/1.7), f'WELCOME', fill="white", font  = fontbig, align="center")
								


								# draw.text(((W-w)/2.5,(H-h)/1.4), f'{user}', fill="white", font  = font, align="center")
								

								# draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
								if 10 > len(member.name)>= 7 :
									draw.text((690, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
								elif 12 > len(member.name)>= 10 :
									draw.text((630, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

								elif 16 > len(member.name)>= 12 :
									draw.text((570, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
								
								elif 19 > len(member.name)>= 16 :
									draw.text((510, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

								elif  len(member.name) < 7 :
									draw.text((740, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
								else  :
									draw.text((450, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

								if 1000>len(member.guild.members) > 99 :
									draw.text((720, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

								elif 10000 >len(member.guild.members) > 999 :
									draw.text((700, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

								elif 100000 >len(member.guild.members) > 9999 :
									draw.text((670, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

								elif len(member.guild.members) > 99999 :
									draw.text((630, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

								else :
									
									draw.text((740, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)
											
								
								b = BytesIO()
								bcg.save(b, format='png')
								b.seek(0)
								file = discord.File(filename="banner.png", fp=b)
							
								await self.bot.get_channel(wcchannel).send(file = file)


					

			
			elif customwc !=None and wccard ==None :
				if wcmessage!= None and wcchannel!=None :
					a = len(member.guild.members)
					c = member.mention
					info = {'user': c , "membercount" : a}
					try:

						channel  = self.bot.get_channel(wcchannel)
						
						await channel.send(wcmessage.format(**info))
						
					except:
						pass

			elif customwc == None and wccard !=None :
				if custombanner !=None and bannersetting != None and wcchannel!=None :
					try:
						async with aiohttp.ClientSession() as session:
							async with session.get(f"{custombanner}") as resp:
								if resp.status != 200:
									pass						
								data = io.BytesIO(await resp.read())
								img1 = Image.open(data)
								img1 = img1.resize((1920,843)).convert('RGBA')
								img2 =Image.open('./data/images/custom_temp.png')
								img2 = img2.convert('RGBA')
								img_url =  member.avatar_url_as(format="png", size=256) # try all three
								async with aiohttp.ClientSession() as session:
									async with session.get(f"{img_url}") as resp:
										if resp.status != 200:
											return 
										dataa = BytesIO(await resp.read())
										img = Image.open(dataa)
										
										img = img.resize((374, 374))
										mask = Image.new('L', img.size, 0)
										draw = ImageDraw.Draw(mask)
										draw.ellipse((0, 0) + img.size, fill=255)
										output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
										output.putalpha(mask)
										img2.paste(output, (771, 63), output.convert('RGBA'))
										
										draw = ImageDraw.Draw(img2)

										fontbig = ImageFont.truetype("./data/ruso.ttf", 110)
										font = ImageFont.truetype("./data/ruso.ttf",80)
										Fontt= ImageFont.truetype("./data/ruso.ttf",70)
										shadowcolor = 'black'
										x,y = 720,485
										# draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
										# draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
										# draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
										# draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
										W, H = (1920,843)
										w, h = draw.textsize('WELCOME')
										draw.text(((W-w)/2.7,(H-h)/1.7), f'WELCOME', fill="white", font  = fontbig, align="center")
										


										# draw.text(((W-w)/2.5,(H-h)/1.4), f'{user}', fill="white", font  = font, align="center")
										

										# draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
										if 10 > len(member.name)>= 7 :
											draw.text((690, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
										elif 12 > len(member.name)>= 10 :
											draw.text((630, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

										elif 16 > len(member.name)>= 12 :
											draw.text((570, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
										
										elif 19 > len(member.name)>= 16 :
											draw.text((510, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

										elif  len(member.name) < 7 :
											draw.text((740, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
										else  :
											draw.text((450, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

										if 1000>len(member.guild.members) > 99 :
											draw.text((720, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

										elif 10000 >len(member.guild.members) > 999 :
											draw.text((700, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

										elif 100000 >len(member.guild.members) > 9999 :
											draw.text((670, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

										elif len(member.guild.members) > 99999 :
											draw.text((630, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

										else :
											
											draw.text((740, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)



										# fontbig = ImageFont.truetype("./data/ruso.ttf", 100)
										# font = ImageFont.truetype("./data/ruso.ttf",80)
										# Fontt= ImageFont.truetype("./data/ruso.ttf",70)
										# shadowcolor = 'black'
										# x,y = 720,485
										# draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
										# draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
										# draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
										# draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)

										# draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
										# draw.text((680, 620),f"{member}", (255, 255, 255), font=font)
										# draw.text((730, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)
										# # img1 = img1.resize((1750,900)).convert('RGBA')
										# # img2 = img2.resize((1350,700)).convert('RGBA')
										img1.paste(img2,(0,0), img2)
										img1.convert('RGBA')
										b = BytesIO()
										img1.save(b, format='png')
										b.seek(0)
										file = discord.File(filename="banner.png", fp=b)
										
										await self.bot.get_channel(wcchannel).send(file = file)
										
					except aiohttp.InvalidURL:
						pass

				elif (custombanner == None or bannersetting ==None) and wcchannel !=None  :
					img_url = member.avatar_url_as(format="png", size=256) # try all three
					async with aiohttp.ClientSession() as session:
						async with session.get(f"{img_url}") as resp:
							if resp.status != 200:
								return 
							data = BytesIO(await resp.read())
							img = Image.open(data)
							files = os.listdir("./data/templates")
							index = random.randrange(0, len(files))
							bcg = Image.open(f'./data/templates/{files[index]}')
							img = img.resize((374, 374))
							mask = Image.new('L', img.size, 0)
							draw = ImageDraw.Draw(mask)
							draw.ellipse((0, 0) + img.size, fill=255)
							output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
							output.putalpha(mask)
							bcg.paste(output, (774, 70), output.convert('RGBA'))

							draw = ImageDraw.Draw(bcg)
							fontbig = ImageFont.truetype("./data/ruso.ttf", 110)
							font = ImageFont.truetype("./data/ruso.ttf",80)
							Fontt= ImageFont.truetype("./data/ruso.ttf",70)
							shadowcolor = 'black'
							x,y = 720,485
							# draw.text((x-2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
							# draw.text((x+2, y-2), f"WELCOME", font=fontbig, fill=shadowcolor)
							# draw.text((x-2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
							# draw.text((x+2, y+2), f"WELCOME", font=fontbig, fill=shadowcolor)
							W, H = (1920,843)
							w, h = draw.textsize('WELCOME')
							draw.text(((W-w)/2.7,(H-h)/1.7), f'WELCOME', fill="white", font  = fontbig, align="center")
							


							# draw.text(((W-w)/2.5,(H-h)/1.4), f'{user}', fill="white", font  = font, align="center")
							

							# draw.text((x, y), f"WELCOME", (255, 255, 255), font=fontbig)
							if 10 > len(member.name)>= 7 :
								draw.text((690, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
							elif 12 > len(member.name)>= 10 :
								draw.text((630, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

							elif 16 > len(member.name)>= 12 :
								draw.text((570, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
							
							elif 19 > len(member.name)>= 16 :
								draw.text((510, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

							elif  len(member.name) < 7 :
								draw.text((740, 620),f"{member}", (255, 255, 255), font=font, align =  "center")
							else  :
								draw.text((450, 620),f"{member}", (255, 255, 255), font=font, align =  "center")

							if 1000>len(member.guild.members) > 99 :
								draw.text((720, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

							elif 10000 >len(member.guild.members) > 999 :
								draw.text((700, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

							elif 100000 >len(member.guild.members) > 9999 :
								draw.text((670, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

							elif len(member.guild.members) > 99999 :
								draw.text((630, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)

							else :
								
								draw.text((740, 740),f"{len(member.guild.members)}TH MEMBER", (255, 255, 255), font=Fontt)
							
						
							b = BytesIO()
							bcg.save(b, format='png')
							b.seek(0)
							file = discord.File(filename="banner.png", fp=b)
						
							await self.bot.get_channel(wcchannel).send(file = file)
		except discord.Forbidden:
			pass





	

	
	# @command(name = 'illegal', description  = 'Make something illegal by Trump.', usage = '+illegal <text>')
	# @cooldown(2, 60, BucketType.user)
	# async def illegal(self, ctx, word):

	# 	if len(word) > 10:
	# 		return await ctx.send("Nope! Gotta be less than 10 characters.")
	# 	word = word.replace('x','a')
	# 	await self.session.post("https://is-now-illegal.firebaseio.com/queue/tasks.json", json={"task": "gif", "word": word.upper()})
	# 	resp = await self.session.get(f"https://is-now-illegal.firebaseio.com/gifs/{word.upper()}.json")
	# 	resp = await resp.json()
	# 	em = discord.Embed(color=ctx.author.color, title=f"Trump made {word} illegal.")
	# 	em.set_image(url=resp['url'])
	# 	em.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
	# 	await ctx.send(embed=em)
		
	
	@commands.command(name = 'tt', description  = 'tweet as Trump.', usage = '+tt <text>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def trumptweet(self, ctx, *, text):
		
		await ctx.trigger_typing()
		params = {
			"type": "trumptweet",
			"text": text
		}
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekobot.xyz/api/imagegen", params=params) as res:
	
				resp = await res.json()
				if not resp['success']:
					return await ctx.send("An error occurred with the API.")
				em = discord.Embed(color=ctx.author.color, title="Trump Tweet")
				em.set_image(url=resp['message'])
				await ctx.send(embed=em)
		
	@commands.command(name = 'kanna', description = 'Show a message as Kanna.', usage = '+kanna <text>')
	@cooldown(3, 30, BucketType.user)
	async def kanna(self, ctx, *, text):
		
		await ctx.trigger_typing()
		params = {
			"type": "kannagen",
			"text": text
		}
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekobot.xyz/api/imagegen", params=params) as res:
		
				resp = await res.json()
				if not resp['success']:
					return await ctx.send("An error occurred with the API.")
				em = discord.Embed(color=ctx.author.color, title="Kanna")
				em.set_image(url=resp['message'])
				await ctx.send(embed=em)
		
	@commands.command(name = 'clyde', description = 'See a message in Clyde-style.', usage = '+clyde <text>')
	@custom_check()
	@cooldown(3, 45, BucketType.user)
	async def clyde(self, ctx, *, text):
		
		await ctx.trigger_typing()
		params = {
			"type": "clyde",
			"text": text
		}
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://nekobot.xyz/api/imagegen", params=params) as res:
		
				resp = await res.json()
				if not resp['success']:
					return await ctx.send("An error occurred with the API.")
				em = discord.Embed(color=ctx.author.color, title="Clyde Message")
				em.set_image(url=resp['message'])
				await ctx.send(embed=em)


	@commands.command(name = 'ship', description  = 'Create a ship between two (or more) members.', usage = '+ship <user> ')
	@custom_check()
	@commands.cooldown(3, 30, BucketType.user)
	async def ship(self, ctx, *members: discord.Member):
	
		members = members or [(await ctx.history(before=ctx.message).next()).author]
		members = [*members, ctx.author] if len(members) == 1 else members  # Include the author if only one member
		if len(members) >= 10:
			await ctx.send("That ship is too big!")
		ship_name = "".join(name[i * (len(name) // len(members)): (i+1) * -(-len(name) // len(members))]
		                    for i, name in enumerate(member.display_name for member in members))    # Combine names
		avatar_size = 128
		image = Image.new("RGBA", ((len(members) * 2 - 1) * avatar_size, avatar_size))
		assets = (member.avatar_url_as(static_format="png", size=avatar_size) for member in members)
		avatars = map(Image.open, map(BytesIO, [await asset.read() for asset in assets]))
		heart = Image.open("./data/images/heart.png")
		for i, avatar in enumerate(avatars):
			image.alpha_composite(avatar.convert(mode="RGBA"), dest=(avatar_size * i * 2, 0))   # Attach avatar
			if i != 0:
				image.alpha_composite(heart, dest=(avatar_size * (i * 2 - 1), 0))                 # Attach heart
		ship_image = BytesIO()
		image.save(ship_image, format="PNG")
		ship_image.seek(0)
		await ctx.send(f"Your ship's name is **{ship_name}!**",file=discord.File(ship_image, f"{ctx.message.id}.png"))
	

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("misc")


def setup(bot) :
    
	bot.add_cog(Misc(bot))

