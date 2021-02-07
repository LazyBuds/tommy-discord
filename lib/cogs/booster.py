import discord
from discord.ext import commands
from discord.ext.commands import Cog, command
from ..db import db
import datetime
from discord.ext.menus import MenuPages,ListPageSource

class HelpMenu(ListPageSource):
        def __init__(self, ctx, data):
                self.ctx = ctx

                super().__init__(data, per_page=10)


        async def write_page(self, menu, offset, fields):
                len_data = len(self.entries)
                embed = discord.Embed(colour=self.ctx.author.colour,description = f'{self.ctx.guild.name} Booster Leaderboard \n')
                embed.description += f'```js{fields}```'

                return embed

        async def format_page(self, menu, entries):
                offset = (menu.current_page*self.per_page) + 1

               
                table = ("").join(f"\n {count+offset}) {entry[0]} : {entry[1]} "for count, entry in enumerate(entries))

                return await self.write_page(menu, offset, table)


class Booster(Cog):
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

   
    
            




    @command(name = 'nitro', aliases = ['booster'], description = 'check for how long someone has boosted the server', usage = '+boost <user>')
    @custom_check()
    async def nitro(self,ctx,member:discord.Member = None):
        member = member or ctx.author
        if member.premium_since is not None:
            current = datetime.datetime.utcnow()
            
            num_months = (current.year - member.premium_since.year) * 12 + (current.month - member.premium_since.month)
            num_days = (current.day- member.premium_since.day)
            num_weeks  = divmod(num_days,7)
            table = f'<a:boostergif:803314155607425055>  {member.mention}  has boosted the server since : {num_months} months {num_weeks[0]} weeks {num_weeks[1]} days'
            embed = discord.Embed(colour = ctx.author.colour, description = table)

           
        
            
            
            await ctx.send(embed = embed)
           
        else:
            await ctx.send('user has not boosted the server')


    @commands.group(name = 'boost')
    @custom_check()
    async def boost(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))


    @boost.command(name = 'lb', description = 'shows the booster leaderboard of a guild', usage = '+boost lb')
    @custom_check()
    async def booster(self,ctx):
        booster  = ctx.guild.premium_subscribers
        if len(booster) == 0 :
            await ctx.send('no one has boosted this guild')


        else :

  


            table = []
        
            for member in ctx.guild.members:
                if member.premium_since is not None :
                    
                    table.append(((f'{member.name}#{member.discriminator}',str(member.premium_since))))

                  
              

        
            sorted_list = sorted(table, key=lambda t: datetime.datetime.strptime(t[1], '%Y-%m-%d %H:%M:%S.%f'))
           
            final = []
            for num in sorted_list:
                date_time_obj = datetime.datetime.strptime(num[1], '%Y-%m-%d %H:%M:%S.%f')
                current = datetime.datetime.utcnow()

                num_months = (current.year - date_time_obj.year) * 12 + (current.month - date_time_obj.month)
                num_days = (current.day- date_time_obj.day)
                num_weeks  = divmod(num_days,7)
            
        
        
                since = f'{num_months} months {num_weeks[0]} weeks {num_weeks[1]} days'
                final.append(((num[0],since)))
               


            
      

          
            
            menu = MenuPages(source=HelpMenu(ctx, final),clear_reactions_after=True,timeout=60.0)
            await menu.start(ctx)


    @boost.command(name='embed' , description = 'set a channel to send embed when someone boost the server ',usage = '+boost embed <channelid>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def boost_embed(self, ctx, *, channel:discord.TextChannel):
      
        db.execute("UPDATE boost SET embed_ch = ? WHERE gu_id =?", channel.id, ctx.guild.id) 
        
        await ctx.send(f"embed channel for boost has been set to `{channel}` ")
        
    @boost_embed.error
    async def boost_embed_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")




    @boost.command(name='channel' , description = 'set a channel to send boost logs ',usage = '+boost channel <channelid>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def boost_channel(self, ctx, *, channel:discord.TextChannel):
      
        db.execute("UPDATE boost SET ch_id = ? WHERE gu_id =?", channel.id, ctx.guild.id) 
        
        await ctx.send(f"boost channel for boost has been set to `{channel}` ")
        
    @boost_channel.error
    async def boost_channel_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")




    @boost.command(name='message', description  = 'set thankyou message when someone boost your server\n you can use variables also : \n `{user}` mentions the user who boosted the server\n `{boost_count}` this tells total no.of boosts server has \n `{server_level}` this tells level of server i.e 0-3', usage = '+boost message <text>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True) 
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def boost_message(self, ctx, *, message):
        '''+boost message thankyou {user} for boosting the server, because of you now we have {boost_count} boosts and server is at level {server_level}'''
        message = message 
        db.execute("UPDATE boost SET boost_msg = ? WHERE gu_id = ?", message, ctx.guild.id) 
        
        await ctx.send(f"boost message has been set to `{message}` ")

    @boost_message.error
    async def boostmessage_error(self, ctx, exc):
        if isinstance(exc, commands.BotMissingPermissions):
            await ctx.send("bot require manage guild perms to run this command.")
        elif isinstance(exc,commands.MissingPermissions ):
            await ctx.send("user should have manage guild perms to run this command.")


    

    @boost.command(name = 'settings', description = 'set up booster feature for your guild')
    async def boost_setting(self, ctx):
        boost_update = db.field('SELECT ch_id FROM boost WHERE gu_id =?', ctx.guild.id)
        boost_setting  = db.field('SELECT setting FROM boost WHERE gu_id = ?', ctx.guild.id)
        boost_embed  = db.field('SELECT embed_ch FROM boost WHERE gu_id = ?', ctx.guild.id)
        boost_message  = db.field('SELECT boost_msg FROM boost WHERE gu_id = ?', ctx.guild.id)
        embed  = discord.Embed(title = '**Tommy boost settings**',description  = f'\n\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\n', colour = ctx.author.colour)
        embed.set_thumbnail(url = ctx.guild.icon_url)


        if boost_setting == 'on' :
            embed.add_field(name = 'Boost updates', value = f'`{boost_setting}` \n type {ctx.prefix}disable boost-updates to disable it', inline =True)

        else :
            embed.add_field(name = 'Boost updates', value = f'`{boost_setting}` \n type {ctx.prefix}enable boost-updates to enable it', inline =True)

        

        if boost_update != None :
            embed.add_field(name = 'Boost log channel', value = f'<#{boost_update}> \n type {ctx.prefix}boost channel <channel> to set it or change it', inline =True)

        else :
            embed.add_field(name = 'Boost log channel' , value = f'`None` \n type {ctx.prefix}boost channel <channel> to set it or change it', inline = True)

        if boost_embed != None :
            embed.add_field(name = 'Boost embed channel', value = f'<#{boost_embed}> \n type {ctx.prefix}boost embed <channel> to set it or change it', inline =True)

        else :
            embed.add_field(name = 'Boost embed channel' , value = f'`None` \n type {ctx.prefix}boost embed <channel> to set it or change it', inline = True)

        if boost_message  :
            embed.add_field(name = 'Boost message', value = f'`{boost_message}` \n type {ctx.prefix}boost message <text> to set it or change it', inline =True)

        else :
            embed.add_field(name = 'Boost message' , value = f'`None` default thankyou message will be used \n type {ctx.prefix}boost message <text> to set it or change it', inline = True)
        await ctx.send(embed=embed)







    


    
    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since is None and after.premium_since is not None:
            boost_update = db.field('SELECT ch_id FROM boost WHERE gu_id =?', after.guild.id)
            boost_embed = db.field('SELECT embed_ch FROM boost WHERE gu_id =?', after.guild.id)
            boost_setting  = db.field('SELECT setting FROM boost WHERE gu_id = ?', after.guild.id)
            if boost_update != None and  boost_setting=='on':
                channel = self.bot.get_channel(boost_update)
                embed = discord.Embed(title  = 'Booster Added', url = 'https://discord.gg/fnqCc7RZYH', colour = 0xF47fff)
                embed.add_field(name = 'User', value = f'{after.name}#{after.discriminator}', inline = False)
                embed.add_field(name = 'User id', value = f'{after.id}', inline = False)
                embed.add_field(name = "Created at", value = after.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline = True)
                embed.add_field(name = "Joined at", value = after.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline = False)
                current = datetime.datetime.utcnow()
            
                num_months = (current.year - after.premium_since.year) * 12 + (current.month - after.premium_since.month)
                num_days = (current.day- after.premium_since.day)
                num_weeks  = divmod(num_days,7)
                

                table = f'{num_months} months {num_weeks[0]} weeks {num_weeks[1]} days'
                embed.add_field(name = 'Boosting Since', value = table, inline = False)
                booster  = after.guild.premium_subscription_count
                
                embed.add_field(name = 'Total boosts', value = booster, inline = False)
                embed.add_field(name =  'Server Boost Level',value = after.guild.premium_tier, inline = False )
                embed.set_thumbnail(url= after.guild.icon_url)

                await channel.send(embed=embed)
            if boost_embed != None and  boost_setting=='on':
                channel = self.bot.get_channel(boost_embed)
                boost_count  = after.guild.premium_subscription_count
                server_level = after.guild.premium_tier
                user = after.mention

                boost_message = db.field('SELECT boost_msg FROM boost WHERE gu_id = ?',after.guild.id)
                if boost_message:
                    info = {'user': user , "boost_count" : boost_count, "server_level": server_level}
                    
                    embed = discord.Embed(description = boost_message.format(**info),colour = 0xF47fff)
                    embed.set_thumbnail(url= after.guild.icon_url)
                    await channel.send(embed= embed)

                else:
                    table = f'<a:boostergif:803314155607425055>  **{after.mention} has boosted the server! ** <a:boostergif:803314155607425055> \n \n Thank you {after.mention} for boosting the server.\n Because of you now we have {boost_count} boosts and server is at level `{server_level}`'
                    embed = discord.Embed(description = table,colour = 0xF47fff)
                    embed.set_thumbnail(url= after.guild.icon_url)
                    await channel.send(embed= embed)


        

       
                
                    



           

            

            

            
        elif before.premium_since != None and after.premium_since is None:
            boost_update = db.field('SELECT ch_id FROM boost WHERE gu_id =?', after.guild.id)
            boost_setting  = db.field('SELECT setting FROM boost WHERE gu_id = ?', after.guild.id)

            if boost_update != None and  boost_setting=='on':
                channel = self.bot.get_channel(boost_update)
                embed = discord.Embed(title  = 'Booster Removed', url = 'https://discord.gg/fnqCc7RZYH', colour = 0xF47fff)
                embed.add_field(name = 'User', value = f'{after.name}#{after.discriminator}', inline = False)
                embed.add_field(name = 'User id', value = f'{after.id}', inline = False)
                embed.add_field(name = "Created at", value = after.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline = True)
                embed.add_field(name = "Joined at", value = after.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline = False)
          
                booster = after.guild.premium_subscription_count
                embed.add_field(name = 'Total boosts', value = booster, inline = False)
                embed.add_field(name =  'Server Boost Level',value = after.guild.premium_tier, inline = False )
                embed.set_thumbnail(url= after.guild.icon_url)

                await channel.send(embed=embed)
        else:
            pass

       

          

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("booster")



def setup(bot): 
    bot.add_cog(Booster(bot)) 
