from discord.ext import tasks
from discord.ext.commands import Cog, command ,cooldown ,BucketType
from discord.ext import commands
from random import choice 
import discord
import requests
from discord import Spotify
import pendulum
# aiohttp should be installed if discord.py is
import aiohttp
from discord import Webhook, AsyncWebhookAdapter
import random
import PIL
from asyncio import sleep
from imdb import IMDb
# PIL can be installed through
# `pip install -U Pillow`
from PIL import Image, ImageDraw, ImageChops, ImageEnhance,ImageOps ,ImageFont

# partial lets us prepare a new function with args for run_in_executor
from functools import partial

# BytesIO allows us to convert bytes into a file-like byte stream.
from io import BytesIO
# from wand import image

# this just allows for nice function annotation, and stops my IDE from complaining.
from typing import Union
from random import randint
import discord
import datetime
from ..utils import noisegen
from ..utils.textutils import auto_text_size
from ..db import db
from ..utils.paginator import HelpPaginator


class ImageCog(Cog):
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
            self.bot.cogs_ready.ready_up("image")

    async def get_avatar(self, user: Union[discord.User, discord.Member]) -> bytes:

        # generally an avatar will be 1024x1024, but we shouldn't rely on this
        avatar_url = user.avatar_url_as(format="png")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'{avatar_url}') as res:

        
            # this gives us our response object, and now we can read the bytes from it.
                avatar_bytes = await res.read()

        return avatar_bytes

    @staticmethod
    def processing(avatar_bytes: bytes, colour: tuple) -> BytesIO:

        # we must use BytesIO to load the image here as PIL expects a stream instead of
        # just raw bytes.
        with Image.open(BytesIO(avatar_bytes)) as im:

            # this creates a new image the same size as the user's avatar, with the
            # background colour being the user's colour.
            with Image.new("RGB", im.size, colour) as background:

                # this ensures that the user's avatar lacks an alpha channel, as we're
                # going to be substituting our own here.
                rgb_avatar = im.convert("RGB")

                # this is the mask image we will be using to create the circle cutout
                # effect on the avatar.
                with Image.new("L", im.size, 0) as mask:

                    # ImageDraw lets us draw on the image, in this instance, we will be
                    # using it to draw a white circle on the mask image.
                    mask_draw = ImageDraw.Draw(mask)

                    # draw the white circle from 0, 0 to the bottom right corner of the image
                    mask_draw.ellipse([(0, 0), im.size], fill=255)

                    # paste the alpha-less avatar on the background using the new circle mask
                    # we just created.
                    background.paste(rgb_avatar, (0, 0), mask=mask)

                # prepare the stream to save this image into
                final_buffer = BytesIO()

                # save into the stream, using png format.
                background.save(final_buffer, "png")
                background.save("./data/images/circle.png")

        # seek back to the start of the stream
        final_buffer.seek(0)

        return final_buffer

    # @command(name = "circle")
    # @cooldown(2, 60, BucketType.user)
    # async def circle(self, ctx, *, member: discord.Member = None):
    #     """Display the user's avatar on their colour."""

    #     # this means that if the user does not supply a member, it will default to the
    #     # author of the message.
    #     member = member or ctx.author

    #     async with ctx.typing():
    #         # this means the bot will type while it is processing and uploading the image

    #         if isinstance(member, discord.Member):
    #             # get the user's colour, pretty self explanatory
    #             member_colour = member.colour.to_rgb()
    #         else:
    #             # if this is in a DM or something went seriously wrong
    #             member_colour = (0, 0, 0)

    #         # grab the user's avatar as bytes
    #         avatar_bytes = await self.get_avatar(member)

    #         # create partial function so we don't have to stack the args in run_in_executor
    #         fn = partial(self.processing, avatar_bytes, member_colour)

    #         # this runs our processing in an executor, stopping it from blocking the thread loop.
    #         # as we already seeked back the buffer in the other thread, we're good to go
    #         final_buffer = await self.bot.loop.run_in_executor(None, fn)

    #         # prepare the file
    #         file = discord.File(filename="./data/images/circle.png", fp=final_buffer)

    #         # send it
    #         await ctx.send(file=file)
    @command(name = 'brazzers', description = 'Add the Brazzers logo to profile pic', usage = '+brazzers <user>')
    @custom_check()
    @cooldown(3, 45, BucketType.user)

    async def brazzers(self,ctx,*,member :discord.Member = None):
        # member = member or ctx.author
        # img_url = member.avatar_url_as(format="png",size = 1024) # try all three
        # response = await requests.get(img_url)
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png")
        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = BytesIO(await resp.read())
                avatar = Image.open(data)
                base = Image.open('./data/images/brazzers.bmp')
                aspect = avatar.width / avatar.height
                new_height = int(base.height * aspect)
                new_width = int(base.width * aspect)
                scale = new_width / avatar.width
                size = (int(new_width / scale / 2), int(new_height / scale / 2))
                base = base.resize(size).convert('RGBA')
                # avatar is technically the base
                avatar.paste(base, (avatar.width - base.width,
                                    avatar.height - base.height), base)
                avatar = avatar.convert('RGBA')
                b = BytesIO()
                avatar.save(b, format='png')
                b.seek(0)
                file = discord.File(filename="brazzers.png", fp=b)
                await ctx.send(file = file)
                del b


    @command(name = 'leftist', description  = 'add marxist flag to your profile', usage = '+leftist <user>')
    @custom_check()
    @cooldown(3, 45, BucketType.user)
    

    async def leftist(self,ctx,member:discord.Member=None):
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png")
        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        # member = member or ctx.author
        # img_url = member.avatar_url_as(format="png") # try all three
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = BytesIO(await resp.read())
                img1 = Image.open(data)
                img1 = img1.resize((300,300)).convert('RGBA')
                img2 = Image.open('./data/images/communism.gif')
                img1.putalpha(96)
                out = []
                for i in range(0, img2.n_frames):
                    img2.seek(i)
                    f = img2.copy().convert('RGBA').resize((300, 300))
                    f.paste(img1, (0, 0), img1)
                    out.append(f.resize((256, 256)))
                b = BytesIO()
                out[0].save(b, format='gif', save_all=True, append_images=out[1:], loop=0, disposal=2, optimize=True, duration=40)
                img2.close()
                b.seek(0)
                file = discord.File(filename="leftist.gif", fp=b)
                await ctx.send(file = file)
                del b


    @command(name = 'deepfry', description  = 'deepfries your pfp', usage = '+deepfry <user>')
    @custom_check()
    @cooldown(3, 45, BucketType.user)

    async def deepfry(self,ctx,member:discord.Member=None):
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png")
        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        # member = member or ctx.author
        # img_url = member.avatar_url_as(format="png") # try all three
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = BytesIO(await resp.read())
                avatar = Image.open(data)
                
                avatar = avatar.resize((400, 400)).convert('RGBA')

                # noinspection PyPep8
                joy, hand, hundred, fire = [
                    Image.open(f'./data/images/deepfry/{asset}.bmp')
                    .resize((100, 100))
                    .rotate(randint(-30, 30))
                    .convert('RGBA')
                    for asset in ['joy', 'ok-hand', '100', 'fire']
                ]

                avatar.paste(joy, (randint(20, 75), randint(20, 45)), joy)
                avatar.paste(hand, (randint(20, 75), randint(150, 300)), hand)
                avatar.paste(hundred, (randint(150, 300), randint(20, 45)), hundred)
                avatar.paste(fire, (randint(150, 300), randint(150, 300)), fire)

                noise = avatar.convert('RGB')
                noise = noisegen.add_noise(noise, 25)
                noise = ImageEnhance.Contrast(noise).enhance(randint(5, 20))
                noise = ImageEnhance.Sharpness(noise).enhance(17.5)
                noise = ImageEnhance.Color(noise).enhance(randint(-15, 15))

                b = BytesIO()
                noise.save(b, format='png')
                b.seek(0)
                file = discord.File(filename="deepfry.png", fp=b)
                await ctx.send(file = file)
                del b


    @command(name = 'imdelete', description = 'delete this meme', usage = '+delete <user>')
    @custom_check()
    @cooldown(3, 45, BucketType.user)

    async def imdelete(self,ctx,member:discord.Member=None):
        # member = member or ctx.author
        # img_url = member.avatar_url_as(format="png") # try all three
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png")
        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = BytesIO(await resp.read())
                avatar = Image.open(data)
                
                avatar = avatar.resize((195, 195)).convert('RGBA')
                base = Image.open('./data/images/delete.bmp').convert('RGBA')
            

                base.paste(avatar, (120, 135), avatar)
                base = base.convert('RGBA')

                b = BytesIO()
                base.save(b, format='png')
                b.seek(0)
                file = discord.File(filename="delete.png", fp=b)
                await ctx.send(file = file)
                del b


    @command(name = 'disability', description = 'not all disabilities look like you', usage = '+disability <user>')
    @custom_check()
    @cooldown(3, 45, BucketType.user)

    async def disability(self,ctx,member:discord.Member=None):
        # member = member or ctx.author
        # img_url = member.avatar_url_as(format="png") # try all three
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png")
        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = BytesIO(await resp.read())
                avatar = Image.open(data)
                
                avatar = avatar.resize((175, 175)).convert('RGBA')
                base = Image.open('./data/images/disability.bmp').convert('RGBA')
                base.paste(avatar, (450, 325), avatar)
                base = base.convert('RGBA')

                b = BytesIO()
                base.save(b, format='png')
                b.seek(0)
                file = discord.File(filename="disability.png", fp=b)
                await ctx.send(file = file)
                del b


    @command(name = 'door', description  = 'door meme manipulation',usage = '+door <user>' )
    @custom_check()
    @cooldown(3, 45, BucketType.user)

    async def door(self,ctx,member:discord.Member=None):
        # member = member or ctx.author
        # img_url = member.avatar_url_as(format="png") # try all three
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png")
        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = BytesIO(await resp.read())
                avatar = Image.open(data)
                base = Image.open('./data/images/door.bmp').convert('RGBA')
                avatar = avatar.resize((479, 479)).convert('RGBA')
                final_image = Image.new('RGBA', base.size)

                # Put the base over the avatar
                final_image.paste(avatar, (250, 0), avatar)
                final_image.paste(base, (0, 0), base)
                final_image = final_image.convert('RGBA')

                b = BytesIO()
                final_image.save(b, format='png')
                b.seek(0)
                
            
                file = discord.File(filename="door.png", fp=b)
                await ctx.send(file = file)
                del b


    @command(name = 'failure', description = 'are you a failure?', usage =  '+failure <user>')
    @custom_check()
    @cooldown(3, 45, BucketType.user)

    async def failure(self,ctx,member:discord.Member=None):
        # member = member or ctx.author
        # img_url = member.avatar_url_as(format="png") # try all three
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png")
        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = BytesIO(await resp.read())
                avatar = Image.open(data)
                
                avatar = avatar.resize((215, 215)).convert('RGBA')
                base = Image.open('./data/images/failure.bmp').convert('RGBA')
                base.paste(avatar, (143, 525), avatar)
                
                base = base.convert('RGBA')

                b = BytesIO()
                base.save(b, format='png')
                b.seek(0)

            
                file = discord.File(filename="failure.png", fp=b)
                await ctx.send(file = file)
                del b


    @command(name = 'gay', description  = 'Show your gay pride!', usage = '+gay <user>')
    @custom_check()
    @cooldown(3, 45, BucketType.user)

    async def gay(self,ctx,member:discord.Member=None):
        # member = member or ctx.author
        # img_url = member.avatar_url_as(format="png") # try all three
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png")
        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = BytesIO(await resp.read())
                avatar = Image.open(data)
                
                base = Image.open('./data/images/gay.bmp').convert('RGBA').resize(avatar.size)
                base.putalpha(128)
                avatar.paste(base,(0,0),base)
            
                avatar = avatar.convert('RGB')

                b = BytesIO()
                avatar.save(b, format='png')
                b.seek(0)

            
                file = discord.File(filename="gay.png", fp=b)
                await ctx.send(file = file)
                del b


    @command(name = 'bjp', description = 'command for bjp fan',usage = '+bjp <user>' )
    @custom_check()
    @cooldown(3, 45, BucketType.user)

    async def bjp(self,ctx,member:discord.Member=None):
        # member = member or ctx.author
        # img_url = member.avatar_url_as(format="png") # try all three
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png")
        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = BytesIO(await resp.read())
                img1 = Image.open(data)
                img1 = img1.resize((300,300)).convert('RGBA')
                img2 = Image.open('./data/images/bjp.gif')
                img1.putalpha(98)
                out = []
                for i in range(0, img2.n_frames):
                    img2.seek(i)
                    f = img2.copy().convert('RGBA').resize((300, 300))
                    f.paste(img1, (0, 0), img1)
                    out.append(f.resize((256, 256)))
                b = BytesIO()
                out[0].save(b, format='gif', save_all=True, append_images=out[1:], loop=0, disposal=2, optimize=True, duration=40)
                img2.close()
                b.seek(0)
                file = discord.File(filename="bjp.gif", fp=b)
                await ctx.send(file = file)
                del b


    @command(name = 'bonk', description = 'bonk a user',usage = '+bonk <user>' )
    @custom_check()
    @cooldown(1, 10, BucketType.user)

    async def bonk(self,ctx, member : discord.Member = None ):
        '''+bonk @rohan'''
        
       
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png")

        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = BytesIO(await resp.read())
                img1 = Image.open(data)
                img1 = img1.resize((140,100)).convert('RGBA')
                img1 = img1.rotate(40,PIL.Image.NEAREST, expand = 1) 
                img2 = Image.open('./data/images/bonk.gif')
                out = []
                for i in range(0, img2.n_frames):
                    img2.seek(i)
                    
                    f = img2.copy().convert('RGBA')
                    f.paste(img1, (285, 205), img1)
                    out.append(f)
                b = BytesIO()
                out[0].save(b, format='gif', save_all=True, append_images=out[1:], loop=0, disposal=2, optimize=True, duration=40)
                img2.close()
                b.seek(0)
                file = discord.File(filename="bonk.gif", fp=b)
                await ctx.send(file = file)
                del b


    @command(name = 'faket6', aliases = ['ft6'], description  = 'create your own t6',usage = '+faket6 <title> <user>' )
    @custom_check()
    @cooldown(3, 45, BucketType.user)

    async def faket6(self,ctx, title , member:discord.Member=None):
        '''faket6 rohan-bhangi @rohan \nfaket6 tommy-cutie @tommy'''
        
            
      
       
        
        if member == None and ctx.message.attachments:
            attachment_url = ctx.message.attachments[0].url
            img_url = attachment_url 
        elif member != None and not ctx.message.attachments:
            
            img_url = member.avatar_url_as(format="png",size = 1024)
        else :
            entity =  ctx.command
            p = await HelpPaginator.from_command(ctx, entity)
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{img_url}") as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
        
                data = BytesIO(await resp.read())
                avatar = Image.open(data)
                base = Image.open('./data/images/t6.png').convert('RGBA')
                avatar = avatar.resize((258, 358)).convert('RGBA')
                base.paste(avatar,(21,0), avatar)
                b = BytesIO()
                base.save(b, format='png')
                b.seek(0)
                file = discord.File(filename="ft6.png", fp=b)
                try:
                    title = title.split("-")
                    
                    title =  (" ").join(f"{entry}" for entry in title)
                except:
                    title = title
                   
                shoob  = self.bot.get_user(673362753489993749)
                img = shoob.avatar_url_as(format = 'png', size = 1024)
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(str(img)) as res:
                        byte = await res.read()
                        hook = await ctx.channel.webhooks()
                    
                        if len(hook)< 10 :
                            # print(len(ctx.channel.webhooks()))
                            web = await ctx.channel.create_webhook(name=shoob.display_name,avatar = byte)
                            
                
                
                
                        

                            embed =  discord.Embed(title = f'{title} Tier: 6', colour = discord.Color(value=0xff0000),url = 'https://www.lazybuds.xyz/' ,description = 'To claim, use: `claim [captcha code]`\n[See your card inventory on our site.\nSupport us and get global rewards!](https://www.lazybuds.xyz/)')
                            embed.set_image(url = "attachment://ft6.png")
                            await web.send(embed = embed, file = file)
                            await web.delete()
                            try:
                                await ctx.message.delete()
                            except:
                                pass
                            res = 'claim bwbih'
                            def check(m):
                                return (m.content).lower() == res.lower()
                            try: 
                    
                                reply = await self.bot.wait_for('message', check=check, timeout = 120)
                                web2 = await ctx.channel.create_webhook(name=shoob.display_name,avatar = byte)
                                table = f'✅ {reply.author.mention} got the card! `{title}` Issue #: `1`. '
                                embed= discord.Embed(description = table, colour  = discord.Color(value = 0x80ca57))
                                await web2.send(embed = embed)
                                await web2.delete()

                            except :
                                await ctx.send(f'Looks like no one got the card {title} T6 at this time..')

                    
                   
                        else :
                            await ctx.send('webhook limit is full for the channel')




    @command(name = 'spotify', description  = 'shows detail of a song user is listening to', usage = '+spotify <user>')
    @custom_check()
    @commands.cooldown(1,30, commands.BucketType.user)
    async def music(self,ctx, user:discord.Member = None):
        user = user or ctx.author

        for activity in user.activities:
            if isinstance(activity,Spotify):
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{activity.album_cover_url}") as resp:
                        if resp.status != 200:
                            return await ctx.send('Could not download file...')
                
                        data = BytesIO(await resp.read())
                        album_pic = Image.open(data)
                        base = Image.open('./data/images/spotify.png')
                        width, height =base.size
                        album_pic = album_pic.resize((120, 120)).convert('RGBA')
                        base.paste(album_pic,(50,(height//2)-60), album_pic)
                        draw = ImageDraw.Draw(base)
                        shadowcolor  = 'black'
                        
                        if (len(activity.title) <= 37):
                            fontbig = ImageFont.truetype("arial.ttf", 28)
                            x,y = (190,(height//2)-61)

                      
                            draw.text((190, (height//2)-60), f"{activity.title}", font=fontbig, fill=shadowcolor)
                            fontbig = ImageFont.truetype("./data/tommy_thin.otf", 24)
                            draw.text((190, (height//2)-21), f"{activity.artist}", font=fontbig, fill=shadowcolor)
                        elif 45> len(activity.title)> 37:
                            fontbig = ImageFont.truetype("arial.ttf", 23)
                            x,y = (190,(height//2)-61)

                      
                            draw.text((190, (height//2)-60), f"{activity.title}", font=fontbig, fill=shadowcolor)
                            fontbig = ImageFont.truetype("./data/tommy_thin.otf", 20)
                            draw.text((190, (height//2)-21), f"{activity.artist}", font=fontbig, fill=shadowcolor)

                        else:
                            em = discord.Embed(color=discord.Color.dark_green())
                            em.set_author(name  = 'Spotify', icon_url  = "https://cdn.discordapp.com/attachments/714910677029879898/745727179274321941/spotify2.png")
                            em.set_thumbnail(url=activity.album_cover_url)
                            em.add_field(name = f"**Song Name**:" , value =  f'{activity.title}', inline = True)
                            
                            em.add_field(name = f"**Song Artist**:" , value =  f'{activity.artist}', inline = True)
                            em.add_field(name = "**Song Album**:" , value = f'{activity.album}', inline = False)
                            em.add_field(name = f"**Song Duration**:" , value =  f"{pendulum.duration(seconds=activity.duration.total_seconds()).in_words(locale='en')}", inline = True)
                            em.add_field(name  = f'**Song url :**', value  = f"https://open.spotify.com/track/%7B{activity.track_id}%7D", inline = False)
                            return await ctx.send(embed=em)




                        print(activity.start)
                        print(datetime.datetime.utcnow())
                    
                        now = datetime.datetime.utcnow()- activity.start
                    
                        print(now)
                        count = now.total_seconds()
                        date_time_obj = datetime.datetime.strptime(str(now), '%H:%M:%S.%f')

                        current = f'{date_time_obj.minute}m {date_time_obj.second}s'
                        print(current)
                     
                        total = activity.duration
                   
                     
                        dur = total.total_seconds()
                        total = datetime.datetime.strptime(str(total), '%H:%M:%S.%f')

                        final = f'{total.minute}m {total.second}s'
                     
                        bar_len = 14 # bar length
                        filled_len = int(bar_len * count // float(dur))
                        bar =   u"─"  * filled_len + '●' + '─' * (bar_len - filled_len)
                        song =  f'{bar}'
                        listening = f'<:spotify:805776553626828800> Listening to **{activity.title}** by **{activity.artist}** | {user.name}'
                        fontbig = ImageFont.truetype("./data/arialuni.ttf", 32, encoding = "utf-8")
                        draw.text((190, (height//2)+18),song, font=fontbig, fill=shadowcolor)
                        fontbi = ImageFont.truetype("arial.ttf", 16)

                        draw.text((364, (height//2)+50),f'{current} / {final}', font=fontbi, fill=shadowcolor)
                        b = BytesIO()
                        base.save(b, format='png')
                        b.seek(0)
                        file = discord.File(filename="spotify.png", fp=b)
                        await ctx.send(listening, file= file)
                        break

        else:
            embed = discord.Embed(description=f"<:spotify:805776553626828800> {user.name} isn't listening to Spotify right now", color=discord.Color.dark_red())
            await ctx.send(embed=embed)




    # @command(name  = 'imdb')
    # async def imdb(self,ctx, * , movie):
    #     ia = IMDb()
    #     search = ia.search_movie(f"{movie}")
    #     for i in range(len(search)): 
    #         id_ = search[0].movieID 

    #     movie = ia.get_movie(id_)
    #     print(movie)
    
       


        


        
      
                    
              
            
              
            




  
    



    


# setup function so this can be loaded as an extension
def setup(bot):
    bot.add_cog(ImageCog(bot))
