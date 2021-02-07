import discord
from discord.ext import commands 
import box
from discord.ext.commands import Cog, command, check
import aiohttp
import random
import json
from ..db import db

class Anime(Cog):
    """ category for anime commands """
    def __init__(self, bot):
        self.bot = bot
      

    async def req(self, url):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://nekos.life/api/v2/img/{url}") as res:
                res = await res.json()
                return box.Box(res)


        
        
    
      
        


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

   

    # @command(name = 'gif')
    # @custom_check()
    # async def gif(self,ctx,* , search:str = None):
    #     embed = discord.Embed(colour=discord.Colour.blue())
    #     session = aiohttp.ClientSession()
        
        
    #     search.replace(' ', '+')
    #     response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=jOHZjNUuLf8v9lMMAKP2cUw7GeD1GjTX&limit=10')
    #     data = json.loads(await response.text())
    #     gif_choice = random.randint(0, 9)
    #     embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
    #     await session.close()
    #     await ctx.send(embed=embed)


    @command(name = 'baka',
             description = 'Random anime picture of BAKA.',
             usage = '+baka')
    @custom_check()
    async def baka(self, ctx):
        
       
        res = await self.req("baka")
        em = discord.Embed(color=ctx.author.color)
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    
    @command(name = 'cuddle',
             description =  "Cuddle with someone..",
             usage  = '+cuddle `user`')
    @custom_check()
    async def cuddle(self, ctx, user: discord.Member = None):
        """+cuddle @Rohan#7140 \n +cuddle """
        res = await self.req("cuddle")
        em = discord.Embed(color=ctx.author.color)
        em.description = f"Looks like **{ctx.author.name}** is cuddling with {f'**{str(user.name)}**' if user else 'themselves'}!"
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)} ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @command(name = 'poke',
             description  = 'Poke someone..')
    @custom_check()
    async def poke(self, ctx, user: discord.Member = None):
      
         
        res = await self.req("poke")
        em = discord.Embed(color=ctx.author.color)
        em.description = f"**{ctx.author.name}** poked {f'**{str(user.name)}**' if user else 'themselves'}!"
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}   ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @command(name = 'kiss', description  = ' kiss someone')
    @custom_check()
    async def kiss(self, ctx, user: discord.Member = None):
         
        res = await self.req("kiss")
        em = discord.Embed(color=ctx.author.color)
        em.description = f"**{ctx.author.name}** just kissed {f'**{str(user.name)}**' if user else 'themselves'}!"
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}   ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @command(name = 'hug', description  = 'hug someone')
    @custom_check()
    async def hug(self, ctx, user: discord.Member = None):
    
         
        res = await self.req("hug")
        em = discord.Embed(color=ctx.author.color)
        em.description = f"**{ctx.author.name}** just hugged {f'**{str(user.name)}**' if user else 'themselves'}!"
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}   ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @command(name = 'pat',  description = 'pat someone')
    @custom_check()
    async def pat(self, ctx, user: discord.Member = None):
  
         
        res = await self.req("pat")
        em = discord.Embed(color=ctx.author.color)
        em.description = f"**{ctx.author.name}** just patted {f'**{str(user.name)}**' if user else 'themselves'}!"
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}   ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @command(name = 'tickle', description = 'tickle someone')
    @custom_check()
    async def tickle(self, ctx, user: discord.Member = None):
      
         
        res = await self.req("tickle")
        em = discord.Embed(color=ctx.author.color)
        em.description = f"**{ctx.author.name}** tickled {f'**{str(user.name)}**' if user else 'themselves'}!"
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}   ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @command(name = 'woof', description = 'woof woof')
    @custom_check()
    async def woof(self, ctx, user: discord.Member = None):
      
         
        res = await self.req("woof")
        em = discord.Embed(color=ctx.author.color)
      
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}   ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @command(name = 'weeb', description = 'Get random pics for weeb')
    @custom_check()
    async def weeb(self, ctx):
        
         
        res = await self.req("avatar")
        em = discord.Embed(color=ctx.author.color)
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}   ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @command(name = 'smug', description ='Get a random pic of smug anime' )
    @custom_check()
    async def smug(self, ctx):
       
         
        res = await self.req("smug")
        em = discord.Embed(color=ctx.author.color)
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}   ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @command(name = 'waifu', description = 'Why not get yourself a waifu?')
    @custom_check()
    async def waifu(self, ctx):
   
         
        res = await self.req("waifu")
        em = discord.Embed(color=ctx.author.color)
        em.description = "Found a waifu for you!"
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}   ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

  

    @command(name = 'slap',description  = 'slap someone')
    @custom_check()
    async def slap(self, ctx, user: discord.Member = None):
      
         
        res = await self.req("slap")
        em = discord.Embed(color=ctx.author.color)
        em.description = f"**{ctx.author.name}** slapped {f'**{str(user.name)}**' if user else 'themselves'}!"
        em.set_image(url=res.url)
        # em.set_footer(text=f"Requested by: {str(ctx.author)}   ", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command(name = 'blush', description = 'full blush', usage = '+blush ')
    @custom_check()
    async def blush(self , ctx):
        async with aiohttp.ClientSession() as s:
            async with s.get("https://api.tenor.com/v1/random?q=anime+blush&key=W987E2ZYYXQX") as r:
                link = await r.json()
 
        
                results = link["results"]
                data = [i for i in results]
                info = data[0]
                media = info["media"]
                types = [i for i in media]
                gif = types[0]
                tinygif = gif["gif"]
                url = tinygif["url"]
                embed=discord.Embed(color = ctx.author.color, description = f"**{ctx.author.name}** blushes!")
                embed.set_image(url=url)
                await ctx.send(embed=embed)


    @commands.command(name = 'cry', description  = "don't cry you are being loved and cared", usage = "+cry" )
    @custom_check()
    async def cry(self , ctx):
        async with aiohttp.ClientSession() as s:
            async with s.get("https://api.tenor.com/v1/random?q=anime+cry&key=W987E2ZYYXQX") as r:
                link = await r.json()
                results = link["results"]
                data = [i for i in results]
                info = data[0]
                media = info["media"]
                types = [i for i in media]
                gif = types[0]
                tinygif = gif["gif"]
                url = tinygif["url"]
                embed=discord.Embed(color = ctx.author.color ,description = f"**{ctx.author.name}** cries!")
                embed.set_image(url=url)
                await ctx.send(embed=embed)


    @commands.command(name = 'dance',description = 'lets dance', usage = '+dance <user>')
    @custom_check()
    async def dance(self , ctx):
        async with aiohttp.ClientSession() as s:
            async with s.get("https://api.tenor.com/v1/random?q=anime+dance&key=W987E2ZYYXQX") as r:
                link = await r.json()
                results = link["results"]
                data = [i for i in results]
                info = data[0]
                media = info["media"]
                types = [i for i in media]
                gif = types[0]
                tinygif = gif["gif"]
                url = tinygif["url"]
                embed=discord.Embed(color = ctx.author.color,description = f"**{ctx.author.name}** dances!")
                embed.set_image(url=url)
                await ctx.send(embed=embed)

    @commands.command(name = 'kill', description = 'kill someone', usage = '+kill <user>')
    @custom_check()
    async def kill(self , ctx,  user:discord.Member= None):
       

        async with aiohttp.ClientSession() as s:
            async with s.get("https://api.tenor.com/v1/random?q=anime+kill&key=W987E2ZYYXQX") as r:
                link = await r.json()
                results = link["results"]
                data = [i for i in results]
                info = data[0]
                media = info["media"]
                types = [i for i in media]
                gif = types[0]
                tinygif = gif["gif"]
                url = tinygif["url"]
                embed=discord.Embed(color = ctx.author.color, description  = f"**{ctx.author.name}** just killed  {f'**{str(user.name)}**' if user else 'themselves'}!")
                embed.set_image(url=url)
                await ctx.send(embed=embed)


    @commands.command(name = 'punch', description = 'punch someone', usage = "+punch <user>")
    @custom_check()
    async def punch(self , ctx,  user:discord.Member= None):
    

        async with aiohttp.ClientSession() as s:
            async with s.get("https://api.tenor.com/v1/random?q=anime+punch&key=W987E2ZYYXQX") as r:
                link = await r.json()
                results = link["results"]
                data = [i for i in results]
                info = data[0]
                media = info["media"]
                types = [i for i in media]
                gif = types[0]
                tinygif = gif["gif"]
                url = tinygif["url"]
                embed=discord.Embed(color = ctx.author.color, description  = f"**{ctx.author.name}** just punched  {f'**{str(user.name)}**' if user else 'themselves'}!")
                embed.set_image(url=url)
                await ctx.send(embed=embed)

    @commands.command(name = 'wink',description = 'wink at someone', usage = '+wink <user>')
    @custom_check()
    async def wink(self , ctx , user:discord.Member=None):
    
        async with aiohttp.ClientSession() as s:
            async with s.get("https://some-random-api.ml/animu/wink") as r:
                link = await r.json()
                url = link["link"]
                embed=discord.Embed(color = ctx.author.color, description  = f"**{ctx.author.name}** just winked at  {f'**{str(user.name)}**' if user else 'themselves'}!")
                embed.set_image(url=url)
                await ctx.send(embed=embed)

    @commands.command(name = 'lick',description = 'lick someone' , usage = '+lick <user>')
    @custom_check()
    async def lick(self , ctx,  user:discord.Member= None):
        

        async with aiohttp.ClientSession() as s:
            async with s.get("https://api.tenor.com/v1/random?q=anime+lick&key=W987E2ZYYXQX") as r:
                link = await r.json()
                results = link["results"]
                data = [i for i in results]
                info = data[0]
                media = info["media"]
                types = [i for i in media]
                gif = types[0]
                tinygif = gif["gif"]
                url = tinygif["url"]
                embed=discord.Embed(color = ctx.author.color, description  = f"**{ctx.author.name}** just licked {f'**{str(user.name)}**' if user else 'themselves'}!")
                embed.set_image(url=url)
                await ctx.send(embed=embed)


    @commands.command(name = 'angry', description = 'angry you ', usage = '+angry')
    @custom_check()
    async def angry(self , ctx):
        async with aiohttp.ClientSession() as s:
            async with s.get("https://api.tenor.com/v1/random?q=anime+angry&key=W987E2ZYYXQX") as r:
                link = await r.json()
        
                results = link["results"]
                data = [i for i in results]
                info = data[0]
                media = info["media"]
                types = [i for i in media]
                gif = types[0]
                tinygif = gif["gif"]
                url = tinygif["url"]
                embed=discord.Embed(title = f"{ctx.author.name} is angry")
                embed.set_image(url=url)
                await ctx.send(embed=embed)



   

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("anime")



def setup(bot): 
    bot.add_cog(Anime(bot)) 
