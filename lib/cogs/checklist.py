import discord
from discord.ext import commands
from discord.ext.commands import Cog, command
import time 
import re
from datetime import datetime, timedelta
import aiohttp
import typing

from ..db import db


class Checklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.group(name = 'checklist', aliases = ['cl'], case_sensitive = True, description = "Add, view and clear checklist", usage = '+cl')
    async def checklist(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))
        

        
    
    @checklist.command(name ='add', description = 'add a task to your checklist', usage = '+cl add <task>')
    async def add(self, ctx, *, text:str):
        db.execute("INSERT INTO todos(userid, content) VALUES(?, ?)", ctx.author.id, text)
        await ctx.send(f"new task added! `{text}`")

    @checklist.command(name  = 'view', description  = 'view your checklist', usage = "+cl view")
    async def _view(self, ctx):
        query = db.records(f"SELECT * FROM todos WHERE userid = ?", ctx.author.id)
        msg = ""
        count = 0
        
        for todo in query:
            count += 1
            msg += f"**{str(count)}** .  {todo[2]} \n"
        
        if count <= 0:
            await ctx.send(f"{ctx.author.mention} your checklist is empty")
        else:
            embed = discord.Embed(colour=ctx.author.color, description=f' >>> {msg}', timestamp=ctx.message.created_at)
            embed.set_author(name=ctx.author.name + "'s Checklist", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @checklist.command(name  = 'delete', usage = "+cl delete <index>", description = 'delete a task from your checklist')
    async def delete(self, ctx, index:int):
        '''+cl delete 2'''
        try:
            index = int(index)
        except:
            await ctx.send("It  must be an integer. \nTry - `cl delete 1`")
    
        res = db.records("SELECT * FROM todos WHERE userid = ?", ctx.author.id)
        todos = len(res)
        
        if todos > 0:
            if index > 0 and index <= todos:
                delete = res[index-1]
                id = delete[0]
                con = delete[2]
                db.execute(f"DELETE FROM todos WHERE id =?", id)
                await ctx.send(f"task Deleted! `{con}`")
            else:
                await ctx.send("task not found")
        else:
            await ctx.send("You dont have any task to delete!")
    
    @checklist.command(name  = 'clear', description = 'clears your entire checklist', usage = '+cl clear')
    async def clear(self, ctx):
        db.execute(f"DELETE FROM todos WHERE userid= {ctx.author.id}")
        await ctx.send("Yoru checklist has been cleared!")


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("checklist")


    


def setup(bot):
    bot.add_cog(Checklist(bot))


    
      