from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext import commands
import discord
from ..db import db
import discord
from ..utils.paginator import HelpPaginator


class Settings(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("settings")



    @commands.command(name='wcmessage', description  = 'set welcome message for your server\n you can use variables also : \n `{membercount}` this tells total no.of members\n `{user}` this mentions the user', usage = '+wcmessage <text>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True) 
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def wc_message(self, ctx, *, message):
        '''+wcmessage welcome {user} to server . Now we are {membercount} members'''
        message = message 
        db.execute("UPDATE guilds SET wcmessage = ? WHERE GuildID = ?", message, ctx.guild.id) 
        ok = db.field("SELECT wcmessage FROM guilds WHERE GuildID = ?", ctx.guild.id)
        await ctx.send(f"wc message has been set to `{ok}` ")

    @wc_message.error
    async def wcmessage_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")


    

    @command(name='wcchannel' , description = 'set your welcome channel',usage = '+wcchannel <channelid>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def wc_channel(self, ctx, *, channel:discord.TextChannel):
      
            
        db.execute("UPDATE guilds SET wcchannel = ? WHERE GuildID =?", channel.id, ctx.guild.id) 
  
        await ctx.send(f"welcome channel has been set to `{channel}` ")
      

    @wc_channel.error
    async def wcchannel_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")


    @command(name='leavechannel' , description = 'set your leave channel',usage = '+leavechannel <channelid>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def leave_channel(self, ctx, *, channel:discord.TextChannel): 
        
        db.execute("UPDATE guilds SET leavechannel = ? WHERE GuildID =?", channel.id, ctx.guild.id) 
    
        await ctx.send(f"leave channel has been set to `{channel}` ")
       

    @leave_channel.error
    async def leavechannel_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")


    @command(name='leavemessage' , description = 'set your leave message',usage = '+leavemessage <text>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def leave_message(self, ctx, *, message):
        message = message or (f"User has left the guild  {ctx.guild.name}")
        db.execute("UPDATE guilds SET leavemessage = ? WHERE GuildID = ?", message, ctx.guild.id) 
        okkkk = db.field("SELECT leavemessage FROM guilds WHERE GuildID = ?", ctx.guild.id)
        await ctx.send(f"leave message has been set to `{okkkk}` ")

    @leave_message.error
    async def leavemessage_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")
        


    @command(name='logchannel' , description = 'set your log channel',usage = '+logchannel <channelid>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def log_channel(self, ctx, *, channel:discord.TextChannel):
      
        db.execute("UPDATE guilds SET Logchannel = ? WHERE GuildID =?", channel.id, ctx.guild.id) 
        
        await ctx.send(f"Log channel has been set to `{channel}` ")
        
    @log_channel.error
    async def logchannel_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")

    @command(name='muterole', description = 'set your mute role',usage = '+muterole <roleid>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def muterole(self, ctx, *, role:discord.Role ):
        
        db.execute("UPDATE permission SET Muterole = ? WHERE guildId =?", role.id, ctx.guild.id) 
    
        await ctx.send(f"mute role has been set to `{role}` ")
        
    @muterole.error
    async def muterole_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage roles perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage roles perms to run this command.")

    @command(name = 'custombanner', description = 'set your custom welcome banner',usage = '+custombanner <link>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def custombanner(self,ctx, link):
        if  link[-4:] in [".jpg",".png", "jpeg"] :
            db.execute('UPDATE permission SET Custombanner = ? WHERE guildId = ?',link, ctx.guild.id)
            check = db.field("SELECT Custombanner FROM permission WHERE guildId = ?", ctx.guild.id)
            if check is not None :
                await ctx.send(f'custom banner updated. New banner is :- {check}')
        else :
            await ctx.send('url must be of .png or .jpg')

    @custombanner.error
    async def banner_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")


    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def enable(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @enable.command(name  = 'custombanner' , description ='enable custom welcome banner for your server ', usage = '+enable custombanner')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def custom_banner_(self,ctx):
        new = 'true'

        db.execute('UPDATE permission SET Bannersetting = ? WHERE guildId = ?',new, ctx.guild.id)
        check = db.field("SELECT Bannersetting FROM permission WHERE guildId = ?", ctx.guild.id)
        
        if check is not None :
            await ctx.send('custom banner has been enabled')

    



    

    @enable.command(name  = 'command' , description ='enable a command  ', usage = '+enable command <commandname>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def ecommand(self,ctx, *, command: str):
        # new = 'True'

        entity = self.bot.get_command(command.lower())

        if entity is None:
            clean = command.replace('@', '@\u200b')
            return await ctx.send(f'Command "{clean}" not found.')
        elif isinstance(entity, commands.Command):
           
            ids = db.column("SELECT channelid FROM command")
            if ctx.channel.id in ids:
     
                check2 = db.field('SELECT commandname FROM command WHERE channelid = ?', ctx.channel.id)
               
                if check2 is None  :
                    await ctx.send('all the commands are enabled in this channel')
                elif check2 is not None :
                    newcheck = check2.split(",")
                    if len(newcheck) > 1 :
                        if command in newcheck :
                            newcheck.remove(command)
                            newcheck2 = ','.join(newcheck)
                            db.execute('UPDATE command SET commandname = ? WHERE channelid = ?',newcheck2, ctx.channel.id)
                            await ctx.send('command has been enabled')
                        else :
                            await ctx.send('command is already enabled')
                    else : 
                        if command in newcheck:
                            newcheck.remove(command)
                            db.execute('UPDATE command SET commandname = NULL WHERE channelid = ?', ctx.channel.id)
                            await ctx.send('that command has been enabled')
                        else :
                            await ctx.send('that command is already enabled')

            elif ctx.channel.id not in ids :
                await ctx.send('all commands are enabled')
      

           

    @ecommand.error
    async def ecommand_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")

    
    @custom_banner_.error
    async def customee_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")

    @enable.command(name = 'wccard', description ='enable custom welcome card for your server ', usage = '+enable wccard')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def wccard(self,ctx):
        new = 'true'
        db.execute("UPDATE permission SET Welcomecard = ? WHERE guildId = ?", new, ctx.guild.id)
        check = db.field("SELECT Welcomecard FROM permission WHERE guildId = ?", ctx.guild.id)
        if check is not None :
            await ctx.send('welcome card has been enabled')
    @wccard.error
    async def wccard_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")
            
    @enable.command(name  = 'customwelcome', description ='enable custom welcome and leave message for your server ', usage = '+enable customwelcome')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def wcmessage(self,ctx):
        wc = 'true'
        db.execute("UPDATE permission SET Customwelcome = ? WHERE guildId = ?", wc, ctx.guild.id)
        check = db.field("SELECT Customwelcome FROM permission WHERE guildId = ?", ctx.guild.id)
        if check is not None :
            await ctx.send('custom welcome message has been enabled')
    @wcmessage.error
    async def wc_message_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")


    @enable.command(name = 'boost-updates', description ='enable it to recieve boost updates', usage = '+enable boost-updates')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def boost_updates(self,ctx):
        new = 'on'
        
        check = db.field("SELECT setting FROM boost WHERE gu_id = ?", ctx.guild.id)
        if check == "off":
            db.execute("UPDATE boost SET setting = ? WHERE gu_id = ?", new, ctx.guild.id)
            await ctx.send(f'boost updates has been enabled. Please make sure to set up log channel for boost updates by typing `{ctx.prefix}boostchannel`')
        else:
            await ctx.send('setting is already enabled')
    @boost_updates.error
    async def boost_updates_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")


    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def disable(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @disable.command(name = 'wccard', description ='disable custom welcome card for your server ', usage = '+disable wccard')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def wccard_(self,ctx):
        db.execute('UPDATE permission SET Welcomecard = NULL WHERE guildId = ?', ctx.guild.id)
        check = db.field("SELECT Welcomecard FROM permission WHERE guildId = ?", ctx.guild.id)
        if check is None :
            await ctx.send('welcome card has been disabled')
    
   
    @wccard_.error
    async def wc_card_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")
            
    @disable.command(name  = 'customwelcome' , description ='disable custom welcome and leave message for your server ', usage = '+disable customwelcome')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def wcmessage_(self,ctx):
        db.execute("UPDATE permission SET Customwelcome = NULL WHERE guildId = ?", ctx.guild.id)
        check = db.field("SELECT Customwelcome FROM permission WHERE guildId = ?", ctx.guild.id)
        if check is None :
            await ctx.send('custom welcome message has been disabled')

    
    @wcmessage_.error
    async def wc_messsage_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")


    @disable.command(name  = 'custombanner', description ='disable custom welcome banner for your server ', usage = '+disable custombanner')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def custom_banner(self,ctx):
        db.execute("UPDATE permission SET Bannersetting = NULL WHERE guildId = ?", ctx.guild.id)
        check = db.field("SELECT Bannersetting FROM permission WHERE guildId = ?", ctx.guild.id)
        if check is None :
            await ctx.send('custom banner has been disabled')

    
    @custom_banner.error
    async def custome_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")

    @disable.command(name  = 'command', description ='disable a command  ', usage = '+disable command <commandname>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def dcommand(self,ctx, *, command: str):
        # new = 'False'

        entity = self.bot.get_command(command.lower())

        if entity is None:
            clean = command.replace('@', '@\u200b')
            return await ctx.send(f'Command "{clean}" not found.')
        elif isinstance(entity, commands.Command):

            # try:
            ids = db.column("SELECT channelid FROM command")
            if ctx.channel.id in ids:
                check2 = db.field('SELECT commandname FROM command WHERE channelid = ?', ctx.channel.id)
                if check2 is  None :
                    db.execute('UPDATE command SET commandname = ? WHERE channelid = ?',command, ctx.channel.id)
                    await ctx.send('command has been disabled')
                elif check2 is not None :
                    newcheck = check2.split(",")
                    if len(newcheck) > 1 :
                        if command in newcheck :
                         
                            await ctx.send('command is already disabled')
                        else :
                            newcheck.append(command)
                            newcheck2 = ','.join(newcheck)
                            db.execute('UPDATE command SET commandname = ? WHERE channelid = ?',newcheck2, ctx.channel.id)
                            await ctx.send('command has been disabled')
                    else : 
                        if command in newcheck:
                            await ctx.send('that command is already disabled')
                            
                        else :
                            
                            newcheck.append(command)
                            newcheck2 = ','.join(newcheck)
                            db.execute('UPDATE command SET commandname = ? WHERE channelid = ?',newcheck2, ctx.channel.id)
                            await ctx.send('that command has been disabled')
            elif ctx.channel.id not in ids :
                db.execute('INSERT INTO command (channelid,commandname) VALUES (?,?)',ctx.channel.id, command)
                await ctx.send('command has been disabled')


             
    @dcommand.error
    async def dcommand_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")


    @disable.command(name = 'boost-updates', description ='disable it to not recieve any boost updates', usage = '+enable boost-updates')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def boost_updatess(self,ctx):
        new = 'off'
        
        check = db.field("SELECT setting FROM boost WHERE gu_id = ?", ctx.guild.id)
        if check == "on":
            db.execute("UPDATE boost SET setting = ? WHERE gu_id = ?", new, ctx.guild.id)
            await ctx.send('boost updates has been disabled')

        else:
            await ctx.send('setting is already disabled')
    @boost_updatess.error
    async def boost_updatess_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")




    @command(name  = 'settings',aliases = ['setting'], description  = 'check your guild settings', usage = '+settings')
    async def settings(self, ctx):
        prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)
        
        logchannel = db.field("SELECT Logchannel FROM guilds WHERE GuildID = ?", ctx.guild.id)
        muterole  =  db.field("SELECT Muterole FROM permission WHERE guildId = ?", ctx.guild.id)
       


        embed  = discord.Embed(description  = f'**Welcome to {ctx.guild.name} settings**\n If any setting is None please set it up to use all the features of bot ', colour = ctx.author.colour)
        embed.set_author(name= 'Tommy guild settings',icon_url= ctx.guild.icon_url)
        embed.add_field(name = 'Prefix :', value = f'`{prefix}` or {ctx.bot.user.mention} \n type {prefix}prefix to  change it',inline = False)
        if logchannel != None:
            embed.add_field(name = 'Log channel', value = f'<#{logchannel}> \n type {prefix}logchannel to set it or change it', inline =True)
        else :
            embed.add_field(name = 'Log channel', value = f'`None` \n type {prefix}logchannel to set it or change it', inline =True)
        if muterole != None :
            embed.add_field(name = 'Mute Role', value = f'<@&{muterole}> \n type {prefix}muterole to set it or change it', inline =False)

        else :
            embed.add_field(name = 'Mute Role', value = f'`None` \n type {prefix}muterole to set it or change it', inline = False)

        embed.add_field(name = 'Welcomer settings :', value = f'To check welcomer settings type `{prefix}welcomer`', inline = False)

      


    
        await ctx.send(embed=embed)


    @command(name = 'welcomer', description = 'check your welcomer settings', usage = '+welcomer')
    async def welcomer(self,ctx):
        wcchannel = db.field("SELECT wcchannel FROM guilds WHERE GuildID = ?", ctx.guild.id)
        wcmessage = db.field("SELECT wcmessage FROM guilds WHERE GuildID = ?", ctx.guild.id)
        prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)
        leavechannel = db.field("SELECT leavechannel FROM guilds WHERE GuildID = ?", ctx.guild.id)
        leavemessage = db.field("SELECT leavemessage FROM guilds WHERE GuildID = ?", ctx.guild.id)
        custombanner = db.field("SELECT Custombanner FROM permission WHERE guildId = ?", ctx.guild.id)
        welcomecard = db.field("SELECT Welcomecard FROM permission WHERE guildId = ?", ctx.guild.id)
        bannersetting = db.field("SELECT Bannersetting FROM permission WHERE guildId = ?", ctx.guild.id)
        customwelcome = db.field("SELECT Customwelcome FROM permission WHERE guildId = ?", ctx.guild.id)
        embed  = discord.Embed(description  = f'**Welcome to {ctx.guild.name} welcomer**', colour = ctx.author.colour)
        embed.set_author(name= 'Tommy Welcomer',icon_url= ctx.guild.icon_url)
        if wcchannel != None :
            embed.add_field(name = 'Welcome channel', value = f'<#{wcchannel}> \n type {prefix}wcchannel to set it or change it ', inline =True)
        else :
            embed.add_field(name = 'Welcome channel', value = f'`None` \n type {prefix}wcchannel to set it or change it', inline =True)

        if  wcmessage != None :
            embed.add_field(name = 'Welcome Message', value = f'{wcmessage} \n type {prefix}wcmessage to set it or change it', inline =False)

        else :
            embed.add_field(name = 'Welcome Message', value = f'`None` \n type {prefix}wcmessage to set it or change it', inline =False)

        if leavechannel != None :
            embed.add_field(name = 'Leave channel', value = f'<#{leavechannel}> \n type {prefix}leavechannel to set it or change it', inline =False)
        else :
            embed.add_field(name = 'Leave channel', value = f'`None`\n type {prefix}leavechannel to set it or change it', inline =False)
        if leavemessage != None :
            embed.add_field(name = 'Leave Message', value = f'{leavemessage} \n type {prefix}leavemessage to set it or change it', inline =False)
        else : 
            embed.add_field(name = 'Leave Message', value = f'`None`\n type {prefix}leavemessage to set it or change it', inline =False)

        if custombanner != None :
            embed.add_field(name = 'Custom banner link', value = f'{custombanner}\n type {prefix}custombanner to set it or change it', inline =False)
        else :
            embed.add_field(name = 'Custom banner link', value = f'None \n type {prefix}custombanner to set it or change it', inline =False)

        if  welcomecard != None :
            embed.add_field(name = 'welcome card', value = f'`Enabled` \n type {prefix}enable | disable wccard to set it or change it', inline =False)
        else :
            embed.add_field(name = 'Welcome card ', value = f'`Disabled.` \n type {prefix}enable | disable wccard to set it or change it', inline =False)

        if  customwelcome!= None :
            embed.add_field(name = 'Custom welcome and Leave messages', value = f'`Enabled` \n type {prefix}enable | disable customwelcome to set it or change it', inline =False)
        else :
            embed.add_field(name = 'Custom welcome and Leave messages', value = f'`Disabled.` \n type {prefix}enable | disable customwelcome to set it or change it', inline =False)

        if  bannersetting != None :
            embed.add_field(name = 'Custom banner', value = f'`Enabled` \n type {prefix}enable | disable custombanner to set it or change it', inline =False)
        else :
            embed.add_field(name = 'Custom banner', value = f'`Disabled.` \n type {prefix}enable | disable custombanner to set it or change it', inline =False)

        await ctx.send(embed = embed)


   













            











        




    

def setup(bot):
    bot.add_cog(Settings(bot))
