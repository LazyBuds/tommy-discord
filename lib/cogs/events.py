import discord
from discord.ext import commands
import random
import datetime
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import command, Cog
from ..db import db
from discord.ext import tasks

class Events(Cog):
    def __init__(self, bot):
        self.bot = bot
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("events")

    @Cog.listener()
    async def on_guild_join(self, guild):
        db.execute("INSERT INTO permission (guildId) VALUES (?)",guild.id)
        db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)
        db.execute("INSERT INTO shoob (guildid) VALUES (?)", guild.id)
        db.execute("INSERT INTO captcha (guid) VALUES (?)",guild.id)
        db.execute("INSERT INTO boost (gu_id) VALUES (?)",guild.id)
        db.execute("INSERT INTO guild_counters (guilds) VALUES (?)",guild.id)
        prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", guild.id)
        channel = self.bot.get_channel(738415035918843916)
        await channel.send(f"Joined a new server!!\n\
                    Server name: {guild.name}\n\
                    Server ID: {guild.id}\n\
                    Server owner: {guild.owner}\n\
                    Server membercount: {guild.member_count}")
        for channel in guild.text_channels:
            if channel.name =='general' or channel.name =='general-chat':
                await channel.send(f'hey there! thanks for adding me . type `{prefix}settings` to see your guild settings and `{prefix}help` to see all the bot commands')

            elif channel.permissions_for(guild.me).send_messages:
                await channel.send(f'hey there! thanks for adding me . type `{prefix}settings` to see your guild settings and `{prefix}help` to see all the bot commands')

            break

   
        

    @Cog.listener()
    async def on_member_remove(self, member):
         
        leavemessage = db.field("SELECT leavemessage FROM guilds WHERE GuildID = ?", member.guild.id)
        
        channell = db.field("SELECT leavechannel FROM guilds WHERE GuildID = ?", member.guild.id)
        if channell and leavemessage :
            a = len(member.guild.members)
            b = member.mention

            info = {'user': b , "membercount" : a}


            await member.guild.get_channel(channell).send(leavemessage.format(**info))
            

    @Cog.listener()
    async def on_guild_remove(self, guild):
        db.execute("DElETE FROM permission WHERE guildId = ?",guild.id)

        db.execute("DELETE FROM guilds WHERE GuildID =?", guild.id)
        db.execute("DELETE FROM captcha WHERE guid =?", guild.id)

        db.execute("DELETE FROM shoob WHERE guildid =?", guild.id)
        db.execute("DELETE FROM boost WHERE gu_id =?", guild.id)
        db.execute("DELETE FROM guild_counters WHERE guilds =?", guild.id)
        channel = self.bot.get_channel(738415101387866243)
        await channel.send(f"Left a server:(\n\
                    Server name: {guild.name}\n\
                    Server ID: {guild.id}\n\
                    Server owner: {guild.owner}\n\
                    Server membercount: {guild.member_count}")
         




def setup(bot) :
    
    bot.add_cog(Events(bot))
  
