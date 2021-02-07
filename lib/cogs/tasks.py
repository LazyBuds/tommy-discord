from discord.ext import tasks
from discord.ext.commands import Cog, command
from discord.ext import commands
from random import choice 
import discord
import PIL
from PIL import ImageDraw, ImageFilter, Image
from PIL import ImageFont
from io import BytesIO
import aiohttp
import random
import re
import string
import math
import asyncio
import random
import discord
from ..db import db




last_message = {}
class Tasks(Cog):
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


    async def captcha(self):
        capcha= ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8)) 
        capcha = str(capcha)
        return capcha
        

    
    # @command(name = 'verify',  description  = 'verify yourself', usage   = '+verify')
    # @custom_check()
    # @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    # async def verify(self, ctx):
    #     capcha= ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8)) 
    #     await ctx.author.send(f"Your CAPTCHA is :  **{str(capcha)}**")
    #     def check(m):
    #         return m.content == capcha  
    #     try:
    
    #         await self.bot.wait_for('message', check=check, timeout = 30)
    #         await ctx.author.send(f'{ctx.author.mention} Congratulations! you have been verified')

    #     except:
    #         await ctx.author.send('try again after 60 secs')

 


    
    
       
                                
   
      
        
        
          
    


    @command(name = 'yt', description  = 'send you top result of youtube search', usage = '+yt <query>')
    @custom_check()
    async def youtube(self, ctx, *, query:str):
        async with aiohttp.request("GET", f'https://www.youtube.com/results?search_query={query}') as resp:
            res2= await resp.text()
            search_results = re.findall('\"\/watch\?v=(.{11})',res2)
            result = "https://www.youtube.com/watch?v=" + search_results[0]
            await ctx.send(f"{ctx.author.mention} {result}")

    # @command(name = 'google',description  = 'send you top result of google search', usage = '+google <query>')
    # @custom_check()
    # async def google(self, ctx,*, argument):
    #     # author = ctx.message.author
    #     # embed = discord.Embed(title="Google Result", color=0xfffffd)
    #     # embed.add_field(name="Here is your result:", value=f"**Request**: {argument}\n**Result**: Click [here](https://www.google.com/search?q={argument})")
    #     # embed.set_footer(text=f"Requested by {author}")
    #     for j in search(argument, tld="com", num=10, stop=1, pause=2): 
    #         await ctx.send(j)


    @command(name = "vote" , description = 'Upvote me on top.gg')
    async def vote(self, ctx):
        embed = discord.Embed(title = f'Vote for me on top.gg', url= "https://top.gg/bot/697463492457922571/vote", colour = ctx.author.colour)
        await ctx.send(embed = embed)

    # @commands.command(name = 'snipe',description = 'shows last deleted message', usage = '+snipe')
    # @custom_check()
    # async def snipe (self , ctx ):
    #     try :
    #         global last_message
            
        
    #         last_message = last_message[str(ctx.channel.id)]
                    
    #         embed = discord.Embed(description = str(last_message["content"]) , color = discord.Color.blue())
    #         embed.set_footer(text = f"Author: {last_message['author']}")
    #         await ctx.send(embed=embed)
    #     except :
    #         pass 

    @commands.Cog.listener()
    async def on_message_delete(self , message):
        global last_message
        

    
        if message.attachments:
            # last_message = {str(message.channel.id) : {"content" : str(message.content) , "author" : str(message.author) , "attachments" : message.attachments[0].proxy_url()}}
            # print(last_message)
            pass

        else :


                        

 
            last_message = {str(message.channel.id) : {"content" : str(message.content) , "author" : str(message.author)}}








    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("tasks")
            
            


def setup(bot) :
    
    bot.add_cog(Tasks(bot))

  


