import discord
import sys
import os
import io
import asyncio
import aiohttp
import textwrap
from discord.ext import commands
from ..utils.paginator import HelpPaginator, CannotPaginate
from ..utils.datpaginator import DatPaginator
from datetime import datetime
from ..db import db


class Help(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
       self.bot.remove_command("help")



    
    @commands.command(name='help')
    async def _help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        
        try:
            if command is None:

                # p = await HelpPaginator.from_bot(ctx)
                # await p.paginate()
                embed = discord.Embed(color =discord.Color(0x303136) ,  timestamp = datetime.utcnow())
                oldprefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)

                entries = (
                ('Prefix', f'current prefix is :-  `{oldprefix}`',False),
                ('Commands ', '[checkout all commands here](https://www.lazybuds.xyz/tommy)',False),
                ('Support ', '[Join bot support server](https://discord.gg/gCmPWtC)',False),
                ('Fiverr', '[check our work on fiverr](https://www.lazybuds.xyz/fiverr)',False)
                # ('Feedback ', f'Type {oldprefix}feedback ',True ),
                # ('New meme template', f'Type {oldprefix}template',False),
                # ("Guild settings ", f'Type {oldprefix}settings',False),
                # ('Welcomer settings', f'Type {oldprefix}welcomer',False)

                )

        # self.embed.add_field(name='How do I use this bot?', value='Reading the bot signature is pretty simple.')
    

                for name, value, inline in entries:
                    embed.add_field(name=name, value=value, inline=inline)
                embed.set_footer(text = '© by Lazy Buds', icon_url = ctx.bot.user.avatar_url)
                embed.set_author(name  = f'{ctx.bot.user.name} Help ', icon_url = ctx.guild.icon_url)

                await ctx.send(embed=embed)
            else:
                entity = self.bot.get_cog(command) or self.bot.get_command(command.lower())

                if entity is None:
                    clean = command.replace('@', '@\u200b')
                    return await ctx.send(f'Command or category "{clean}" not found.')
                elif isinstance(entity, commands.Command):
                    p = await HelpPaginator.from_command(ctx, entity)
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)
                    await p.paginate()

            
        except Exception as e:
            await ctx.send(e)
            
  

















# import discord
# import math
# import asyncio
# from discord.ext import commands

# from typing import Optional

# from discord import Embed
# from discord.utils import get
# from discord.ext.menus import MenuPages, ListPageSource
# from discord.ext.commands import Cog
# from discord.ext.commands import command


# class MyHelpCommand(commands.HelpCommand):
#     async def send_bot_help(self, mapping):
#         ctx = self.context
#         sg = ctx.bot.get_guild(640764065085521930)
#         nextbtn = "⏭️"
#         prevbtn = "⏮️"
#         stopbtn = "⏹️"
#         valids = [nextbtn, prevbtn, stopbtn]
#         cogs = []
#         for cog in ctx.bot.cogs.values():
#             if await ctx.bot.is_owner(ctx.author):
#                 cogs.append(cog)
#             else :
#                 cog_commands = [command for command in cog.get_commands() if command.hidden == False and command.enabled == True]
#                 if len(cog_commands) > 0:
#                     cogs.append(cog)
                    
#         page = 0
#         per_page = 15
#         total_page = math.ceil(len(cogs) / per_page)
#         while True:
#             embed = discord.Embed(color = discord.Color.blurple(),
#                                   timestamp = ctx.message.created_at,
#                                   description = f"These are the avaliable categories for {ctx.bot.user.name}\nThe bot prefix is: **`{ctx.prefix}`** \n Use {self.clean_prefix}help <Category> to get help on a category \n")
                                  
#             now = cogs[page * per_page: page * per_page + per_page]# print(now)
#             for cog in now:
#                 if await ctx.bot.is_owner(ctx.author):
#                     cog_commands = [command for command in cog.get_commands()]
#                 else :
#                     cog_commands = [command for command in cog.get_commands() if command.hidden == False and command.enabled == True]
#                 if len(cog_commands) > 0:
#                     if cog.description:
#                         cog_help = cog.description
#                     else :
#                         cog_help = "No description provided"
#                     def check(command):
#                         return command.name
                   
#                     commandss = [command for command in cog.get_commands() if command.hidden == False and command.enabled == True]
#                     command = get(commandss)
#                     embed.description +=(f"**__{cog.qualified_name}__**\n `{cog_help}`\n")
#             embed.set_thumbnail(url = ctx.bot.user.avatar_url)
#             embed.set_author(name = f"{ctx.bot.user.name} Help", icon_url = ctx.guild.icon_url)

#             try:
#                 await msg.edit(embed = embed)
#             except:
#                 msg = await ctx.send(embed = embed)
#             await msg.add_reaction(prevbtn)
#             await asyncio.sleep(0.1)
#             await msg.add_reaction(stopbtn)
#             await asyncio.sleep(0.1)
#             await msg.add_reaction(nextbtn)
#             def check(r, u):
#                 return (u.id == ctx.author.id) and((r.message.id == msg.id) and r.emoji in valids)
#             try:
#                 r, u = await ctx.bot.wait_for("reaction_add", timeout = 60, check = check)
#                 if r.emoji == nextbtn:
#                     page += 1
#                     if page > total_page - 1:
#                         page = total_page - 1
#                         desc = ""
#                 elif r.emoji == prevbtn:
#                     page -= 1
#                     if page < 0:
#                         page = 0
#                         desc = ""
#                 elif r.emoji == stopbtn:
#                     try:
#                         return await msg.delete()
#                     except:
#                         return
#                 try:
#                     await msg.remove_reaction(r.emoji, u)
#                 except:
#                     pass
#             except:
#                 try:
#                     await msg.clear_reactions()
#                     break
#                 except:
#                     pass
#                 break
#     async def send_cog_help(self, cog):
#         ctx = self.context
#         pre = self.clean_prefix
#         embed = discord.Embed(color = discord.Color.gold(),
#                               timestamp = ctx.message.created_at, #description = f"Use {self.clean_prefix}help <command> to get help on a command. \n"
#                               description = "")
#         if await ctx.bot.is_owner(ctx.author):
#             shown_commands = [command for command in cog.get_commands()]
#         else :
#             shown_commands = [command for command in cog.get_commands() if command.hidden == False and command.enabled == True]
#         if len(shown_commands) == 0:
#             return await ctx.send("This cog has no command.")
#         if cog.description:
#             cog_help = cog.description
#         else :
#             cog_help = "No description provided for this cog"
#         embed.title = f"{cog.qualified_name}"
#         embed.description += f"{cog_help}\nUse `{self.clean_prefix}help <command>` to get help on a command.\n\n**Commands :** \n"
#         for command in shown_commands:
#             embed.description += f"▪︎{pre}{command.qualified_name} "
#             if command.signature:
#                 embed.description += f"{command.signature} \n"
#             else :
#                 embed.description += "\n"
#         # embed.description += " - ".join(command.qualified_name for command in shown_commands)
#         embed.set_thumbnail(url = ctx.bot.user.avatar_url)

#         await ctx.send(embed = embed)

# Command Help
# async def send_command_help(self, command):
#   ctx = self.context

# embed = discord.Embed(
#   color = discord.Color.green(),
#   timestamp = ctx.message.created_at,
#   description = ""
# )

# if (command.hidden == True or command.enabled == False) and await ctx.bot.is_owner(ctx.author) == False:
#   return await ctx.send(f"No command called \"{command.qualified_name}\" found.")

# msg = ""
# if command.signature:
#   embed.title = f"{command.qualified_name} {command.signature} \n"
# else :
#   embed.title = f"{command.qualified_name}\n"

# if command.help:
#   embed.description += f"{command.help}"
# else :
#   embed.description += "No description provided\n"

# if len(command.aliases) > 0:
#   embed.description += "Aliases : " + ", ".join(command.aliases)

# embed.set_thumbnail(url = ctx.bot.user.avatar_url)
# await ctx.send(embed = embed)

# # Group Help
# async def send_group_help(self, group):
#   ctx = self.context
# pre = self.clean_prefix
# embed = discord.Embed(
#   color = discord.Color.blurple(),
#   timestamp = ctx.message.created_at
# )

# if group.signature:
#   embed.title = f"{group.qualified_name} {group.signature}"
# else :
#   embed.title = group.qualified_name + " - group"

# if group.help:
#   embed.description = group.help.split("\n")[0]
# else :
#   embed.description = f"No description provided."

# embed.description += f"\nUse `{pre}help {group.qualified_name} <sub_command>` to get help on a group command. \n\n**Subcommands : **\n"

# if await ctx.bot.is_owner(ctx.author):
#   group_commands = [command
#     for command in group.commands
#   ]
# if len(group_commands) == 0:
#   return await ctx.send("This group doesnt seem to have any sub command")
# else :
#   group_commands = [command
#     for command in group.commands
#     if command.hidden == False and command.enabled == True
#   ]

# if len(group_commands) == 0:
#   return await ctx.send(f"No command called \"{group.qualified_name}\" found.")

# for command in group_commands:
#   if command.signature:
#   command_help = f"▪︎{pre}{command.qualified_name} {command.signature} \n"
# else :
#   command_help = f"▪︎{pre}{command.qualified_name} \n"

# embed.description += command_help

# embed.set_thumbnail(url = ctx.bot.user.avatar_url)
# await ctx.send(embed = embed)

# class Help(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.bot._original_help_command = bot.help_command
#         bot.help_command = MyHelpCommand()
#         bot.help_command.cog = self
#     def cog_unload(self):
#         self.bot.help_command = self.bot._original_help_command

# def syntax(command):
#     cmd_and_aliases = "|".join([str(command), * command.aliases])
#     params = []
#     for key, value in command.params.items():
#         if key not in ("self", "ctx"):
#             params.append(f"[{key}]" if"NoneType" in str(value) else f"<{key}>")
#     params = " ".join(params)
#     return f"`{cmd_and_aliases} {params}`"

# class HelpMenu(ListPageSource):
#     def __init__(self, ctx, data):
#         self.ctx = ctx
#         super().__init__(data, per_page = 6)
#     async def write_page(self, menu, fields = []):
#         offset = (menu.current_page * self.per_page) + 1
#         len_data = len(self.entries)
#         embed = Embed(description = f"These are the avaliable categories for {self.ctx.bot.user.name}\nThe bot prefix is: **`{self.ctx.prefix}`** \n Use {self.ctx.prefix}help <Category> to get help on a category \n",
#                       colour = self.ctx.author.colour)
#         embed.set_author(name = f"{self.ctx.bot.user.name} Help", icon_url = self.ctx.guild.icon_url)
#         embed.set_footer(text = f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.", icon_url = self.ctx.bot.user.avatar_url)
#         embed.set_thumbnail(url = self.ctx.bot.user.avatar_url)
#         for name, value in fields:
#             embed.add_field(name = name, value = value, inline = False)
#         return embed
#     async def format_page(self, menu, entries):
#         fields = []
#         for entry in entries:
#             fields.append((entry.brief or "No description", syntax(entry)))
#         return await self.write_page(menu, fields)

# class Help(Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.bot.remove_command("help")
        
#     async def cmd_help(self, ctx, command):
#         embed = Embed(timestamp = ctx.message.created_at,
#                       colour = ctx.author.colour,
#                       title = f" **{command.qualified_name}** :")
#         embed.add_field(name = "❯ **Command description**", value = command.help, inline = False)
#         embed.add_field(name = "❯ **Aliases**", value = command.aliases, inline = False)
#         embed.add_field(name= "❯ **Usage**", value = command.usage, inline = False)
#         embed.set_author(name =f"{ctx.bot.user.name} Help", icon_url = ctx.guild.icon_url )
#         embed.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.bot.user.avatar_url)
#         embed.set_thumbnail(url = ctx.bot.user.avatar_url)
#         await ctx.send(embed = embed)

#     @command(name="help")
#     async def show_help(self, ctx, cmd: Optional[str]):
#         """Shows this message."""
#         if cmd is None:
#             menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)),
#                              delete_message_after=True,
#                              timeout=60.0)
#             await menu.start(ctx)
#         else:
#             if (command := get(self.bot.commands, name=cmd)):
#                 await self.cmd_help(ctx, command)
#             else:
#                 await ctx.send("That command does not exist.")
                
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")


def setup(bot):
	bot.add_cog(Help(bot))


