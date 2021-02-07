import discord
from discord.ext.commands import Cog, command
from captcha.image import ImageCaptcha
from io import BytesIO
import string
import secrets
from discord.ext import commands
import os
import random
from PIL import Image
from PIL import ImageFilter
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
from ..db import db





class Captcha(Cog):
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
            self.bot.cogs_ready.ready_up("captcha")
    

    @custom_check()
    @commands.cooldown(1,50,commands.BucketType.user)

    @command(name = 'verify')
    async def verify(self, ctx):
        chan = db.field('SELECT chid FROM captcha WHERE guid = ?', ctx.guild.id)
        if chan is None:
            img2 = Image.open('./data/images/captcha2.png')
            draw = Draw(img2)
            res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
                                                for i in range(7)) 

            fontbig = truetype("./data/Nervous.ttf", 100)
        
            shadowcolor = 'white'
            x,y = 290,140
            draw.text((x, y), f"{res}", font=fontbig, fill=shadowcolor)
            b = BytesIO()
            img2.save(b,format= "png")
            b.seek(0)
            file = discord.File(filename="captcha.png", fp=b)
            embed = discord.Embed(color = 0x5a6ea7, description = f'**Captcha Verification** \n Hey {ctx.author.name}, Please complete the Captcha below to get access to rest of server.\n\n**Why?**\n This is to prevent malicous attacks and raids using automated userbots in servers.\n\n **Need help?** \n [Join our support server](https://discord.gg/gCmPWtC)\n\n **Want to invite the bot?**\n [here is the invite link](https://discord.com/api/oauth2/authorize?client_id=697463492457922571&permissions=2147483639&redirect_uri=https%3A%2F%2Fwww.lazybuds.xyz%2Ftommy&response_type=code&scope=identify%20bot)\n\n **Note**: \nYou only have `20secs` to enter the captcha')
            embed.set_author(name=f'Welcome to {ctx.guild.name}', icon_url=ctx.guild.icon_url)
            embed.set_image(url = "attachment://captcha.png")
            try:
               
                await ctx.author.send(embed=embed,file=file)
                await ctx.send(f'check your dm for captcha {ctx.author.mention}')
            except:
                await ctx.send("Please open your dm so that bot can dm you the captcha")
            def check(m):
                return (m.content).lower() == res.lower()
            try:
            
                reply = await self.bot.wait_for('message', check=check, timeout = 20)
                try:
                    role = db.field('SELECT roleid FROM captcha WHERE guid = ?',ctx.guild.id)
                    await ctx.author.add_roles(role)
                    roles = ctx.guild.get_role(role)
                    await ctx.author.send(f' Congratulations! you have been verified')
                except :
                    await ctx.author.send(f' Congratulations! you have been verified')
            except:
                await ctx.author.send('captcha failed! try again after 30 secs')       

        else:
            if ctx.channel.id == chan:
                
                img2 = Image.open('./data/images/captcha2.png')
                draw = Draw(img2)
                res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
                                                    for i in range(7)) 

                fontbig = truetype("./data/Nervous.ttf", 100)
            
                shadowcolor = 'white'
                x,y = 290,140
                draw.text((x, y), f"{res}", font=fontbig, fill=shadowcolor)
                b = BytesIO()
                img2.save(b,format= "png")
                b.seek(0)
                file = discord.File(filename="captcha.png", fp=b)
                embed = discord.Embed(color = 0x5a6ea7, description = f'**Captcha Verification** \n Hey {ctx.author.name}, Please complete the Captcha below to get access to rest of server.\n\n**Why?**\n This is to prevent malicous attacks and raids using automated userbots in servers.\n\n **Need help?** \n [Join our support server](https://discord.gg/gCmPWtC)\n\n **Want to invite the bot?**\n [here is the invite link](https://discord.com/api/oauth2/authorize?client_id=697463492457922571&permissions=2147483639&redirect_uri=https%3A%2F%2Fwww.lazybuds.xyz%2Ftommy&response_type=code&scope=identify%20bot)\n\n **Note**: \nYou only have `20secs` to enter the captcha')
                embed.set_author(name=f'Welcome to {ctx.guild.name}', icon_url=ctx.guild.icon_url)
                embed.set_image(url = "attachment://captcha.png")
                try:
                    
                    await ctx.author.send(embed=embed,file=file)
                    await ctx.send(f'check your dm for captcha {ctx.author.mention}')
                except:
                    await ctx.send("Please open your dm so that bot can dm you the captcha")
                def check(m):
                    return (m.content).lower() == res.lower()
                try:
            
                    reply = await self.bot.wait_for('message', check=check, timeout = 15)
                    try:
                        role = db.field('SELECT roleid FROM captcha WHERE guid = ?',ctx.guild.id)
                        roles = ctx.guild.get_role(role)

                        await ctx.author.add_roles(roles)
                        await ctx.author.send(f' Congratulations! you have been verified')
                    except :
                        await ctx.author.send(f' Congratulations! you have been verified')
                except:
                    await ctx.author.send('captcha failed! try again after 30 secs')
                


                
            else:
                await ctx.send(f'type {ctx.prefix}verify in <#{chan}>')

        # image = ImageCaptcha(width = 280, height = 90)
    
        # b = BytesIO()
        # res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
        #                                         for i in range(7)) 
        # image.create_captcha_image(res,
        # (255, 255, 255),(255, 0, 0))
        # data = image.generate(res)
        # image.write(res, b, format = 'png')
        # b.seek(0)
        # file = discord.File(filename="captcha.png", fp=b)
        # await ctx.send(file = file)
        # def check(m):
        #     return m.content == res
        # try:
    
        #     reply = await self.bot.wait_for('message', check=check, timeout = 30)
        #     await ctx.send(f'{reply.author.mention} Congratulations! you have been verified')

        # except:
            # #     await ctx.author.send('try again after 60 secs')
            #     img2 = Image.open('./data/images/captcha2.png')
            #     draw = Draw(img2)
            #     res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
            #                                         for i in range(7)) 

            #     fontbig = truetype("./data/Nervous.ttf", 100)
            
            #     shadowcolor = 'white'
            #     x,y = 290,140
            #     draw.text((x, y), f"{res}", font=fontbig, fill=shadowcolor)
            #     b = BytesIO()
            #     img2.save(b,format= "png")
            #     b.seek(0)
            #     file = discord.File(filename="captcha.png", fp=b)
            #     embed = discord.Embed(color = ctx.author.colour, description = f'**Captcha Verification** \n Hey {ctx.author.name}, Please complete the Captcha below to get access to rest of server.\n\n**Why?**\n This is to prevent malicous attacks and raids using automated userbots in servers.\n\n **Need help?** \n [Join our support server](https://discord.gg/gCmPWtC)\n\n **Want to invite the bot?**\n [here is the invite link](https://discord.com/api/oauth2/authorize?client_id=697463492457922571&permissions=2147483639&redirect_uri=https%3A%2F%2Fwww.lazybuds.xyz%2Ftommy&response_type=code&scope=identify%20bot)\n\n **Note**: \nYou only have `15secs` to enter the captcha')
            #     embed.set_author(name=f'Welcome to {ctx.guild.name}', icon_url=ctx.guild.icon_url)
            #     embed.set_image(url = "attachment://captcha.png")
            #     await ctx.send(embed=embed,file=file)
            #     def check(m):
            #         return (m.content).lower() == res.lower()
            #     try:
            
            #         reply = await self.bot.wait_for('message', check=check, timeout = 15)
            #         role = db.execute('SELECT roleid FROM captcha WHERE guid = ?',ctx.guild.id)
            #         await reply.author.add_roles(role)
            #         await ctx.send(f'{reply.author.mention} Congratulations! you have been verified')

            #     except:
            #         await ctx.author.send('try again after 30 secs')
            # else:
            #     await ctx.send(f'type {ctx.prefix}verify in {chan}')

 
    @commands.group(name = 'verification')
    @commands.guild_only()
    @custom_check()
    @commands.has_guild_permissions(manage_roles = True,manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True, manage_roles = True)
    async def verification(self, ctx):
        
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    
        

    @verification.command(
        name="channel",
        description="set verification channel",
        usage="+verfication channel #channel",
    )
    async def verichan(self, ctx, channel:discord.TextChannel):
        db.execute("UPDATE captcha SET chid = ? WHERE guid =?", channel.id, ctx.guild.id) 
     
        await ctx.send(f"verification role has been set to `{channel}` ")


    @verichan.error
    async def verichan_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage channel perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage channel perms to run this command.")

    @verification.command(
        name="role",
        description="set verification role",
        usage="+verfication role @role",
    )
    async def verirole(self, ctx, role:discord.Role):
        db.execute("UPDATE captcha SET roleid = ? WHERE guid =?", role.id, ctx.guild.id) 
     
        await ctx.send(f"verification role has been set to `{role.mention}` ")

    @verirole.error
    async def verirole_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage channel perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage channel perms to run this command.")


    @verification.command(name  = 'settings', description = 'setup verification for your server', usage = '+verification settings')
    async def ver_settings(self,ctx):
        ver_channel = db.field("SELECT chid FROM captcha WHERE guid= ?", ctx.guild.id)
        ver_role = db.field("SELECT roleid FROM captcha WHERE guid = ?", ctx.guild.id)
        embed  = discord.Embed(title = '**Tommy verification settings**',description  = f'\n\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\n', colour = ctx.author.colour)
        embed.set_thumbnail(url = ctx.guild.icon_url)


        if ver_channel != None:
            embed.add_field(name = 'Verification channel', value = f'<#{ver_channel}> \n type {ctx.prefix}verfication <channel> to set it or change it', inline =True)
        else :
            embed.add_field(name = 'Verification channel', value = f'`None` \n type {ctx.prefix}verification <channel> to set it or change it', inline =True)
        if ver_role != None :
            embed.add_field(name = 'Verificaion Role', value = f'<@&{ver_role}> \n type {ctx.prefix}verification <role> to set it or change it', inline =True)

        else :
            embed.add_field(name = 'Verification Role', value = f'`None` \n type {ctx.prefix}verification <role> to set it or change it', inline = True)

        
        await ctx.send(embed=embed)











def setup(bot): 
    bot.add_cog(Captcha(bot)) 

        