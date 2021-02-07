import discord
from discord.ext import commands
from discord.ext.commands import Cog, command
from aiohttp import request
import requests
import json
from ..utils.util import Pag
from ..db import db
class Usage(Cog):
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


    @commands.Cog.listener()
    async def on_command_completion(self, ctx):

        try:
       
            command  = ctx.command.root_parent.name.lower() if ctx.command.parent else ctx.command.name.lower()
            amount  = db.field('SELECT amount FROM global_counters WHERE command = ?', command)
            guild_amount  = db.field('SELECT amount FROM guild_counters WHERE guilds = ?', ctx.guild.id)

            db.execute('UPDATE global_counters set amount  = ? WHERE command = ?', amount + 1, command)

            db.execute('UPDATE guild_counters set amount  = ? WHERE guilds = ?', guild_amount + 1, ctx.guild.id)

        except :
            pass


    @custom_check()


    @commands.command(
        name="commandstats",
        description="Show an overall usage for each command!",
        usage = '+commandstats',
        aliases = ['cmdstats']
    )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def command_stats(self, ctx):
        data = db.records('SELECT * FROM global_counters')
        command_map = {item[0]: item[1] for item in data}

       
        total_commands_run = sum(command_map.values())

      
        sorted_list = sorted(command_map.items(), key=lambda x: (x[1]), reverse=True)


        sorted_list = [p for p in sorted_list if p[1]!=0 and p[0] != 'commandstats' and p[0] != 'guildlb' and p[0]!='help' and p[0] != 'botinfo']
    
      
        pages = []
        cmd_per_page = 8

        for i in range(0, len(sorted_list), cmd_per_page):
            message = "Command Name: `Usage % | Num of command runs`\n\n"
            next_commands = sorted_list[i: i + cmd_per_page]

            for item in next_commands:
                use_percent = item[1] / total_commands_run
                message += f"**{item[0]}**: `{use_percent: .2%} | Ran {item[1]} times`\n"

            pages.append(message)

        await Pag(title="Command Usage Statistics!", color=0xC9B4F4, entries=pages, length=1).start(ctx)




    

    @commands.command(
        name="guildlb",
        description="Shows you the list of top 5 guilds",
        usage = '+guildlb'
    )
    @custom_check()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def guild_stats(self, ctx):
    




  
 
        data = db.records('SELECT * FROM guild_counters')
        command_map = {item[0]: item[1] for item in data}

        # get total commands run
        total_commands_run = sum(command_map.values())

        # Sort by value
        sorted_list = sorted(command_map.items(), key=lambda x: x[1], reverse=True)

        sorted_list = [p for p in sorted_list if not p[0]==704217816940675072]
  
       

        message = "Guild Name: `Usage % | Num of time command used`\n\n"

      

        for item in sorted_list[0:5]:
            
        
         
            guild_name = ctx.bot.get_guild(item[0])
            use_percent = item[1] / total_commands_run
            message += f"**{guild_name.name}**: `{use_percent: .2%} | used {item[1]} times`\n"

  

        embed = discord.Embed(title="Top 5 Servers",url = "https://discord.gg/EVPRsknwvx", color=0xC9B4F4, description = message)
        await ctx.send(embed = embed)



    





    
    @commands.command(
        name="guilds",
        description="Shows you the list of top 20 guilds",
        usage = '+guilds',
        hidden = True
    )
    @commands.is_owner()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def gustats(self, ctx):
    




  
 
        data = db.records('SELECT * FROM guild_counters')
        command_map = {item[0]: item[1] for item in data}

        # get total commands run
        total_commands_run = sum(command_map.values())

        # Sort by value
        sorted_list = sorted(command_map.items(), key=lambda x: x[1], reverse=True)

        pages = []
        cmd_per_page = 6

        for i in range(0, len(sorted_list), cmd_per_page):
            message = "Guild Name: `Usage % | Num of time command used`\n\n"
            next_commands = sorted_list[i: i + cmd_per_page]

            for item in next_commands:
                guild_name = ctx.bot.get_guild(item[0])
                use_percent = item[1] / total_commands_run
                message += f"**{guild_name.name}**: `{use_percent: .2%} | used {item[1]} times`\n"

            pages.append(message)

        await Pag(title="Guild lb Command Usage!", color=0xC9B4F4, entries=pages, length=1).start(ctx)




    #     @commands.command(
    #     name="userlb",
    #     description="Shows top user according to tommy usage"
    # )
    # @commands.cooldown(1, 5, commands.BucketType.guild)
    # async def guild_stats(self, ctx, arg = None):
    




  
 
    #     data = db.records('SELECT * FROM user_counters')
    #     command_map = {item[0]: item[1] : item[2] for item in data}

    #     # get total commands run
    #     total_commands_run = sum(command_map.values())

    #     # Sort by value
    #     sorted_list = sorted(command_map.items(), key=lambda x: x[1], reverse=True)

    #     pages = []
    #     cmd_per_page = 5

    #     for i in range(0, 14, cmd_per_page):
    #         message = "Guild Name: `Usage % | Num of time command used`\n\n"
    #         next_commands = sorted_list[i: i + cmd_per_page]

    #         for item in next_commands:
    #             guild_name = ctx.bot.get_guild(item[0])
    #             use_percent = item[1] / total_commands_run
    #             message += f"**{guild_name.name}**: `{use_percent: .2%} | used {item[1]} times`\n"

    #         pages.append(message)

    #     await Pag(title="Guild lb Command Usage!", color=0xC9B4F4, entries=pages, length=1).start(ctx)



   
        
              
                
            
            


                

        
                  
        



    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("usage")
            
            


def setup(bot) :
    
    bot.add_cog(Usage(bot))