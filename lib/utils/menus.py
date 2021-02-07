


# class Menus(ListPageSource):

# 	def __init__(self, ctx, data):
# 		self.ctx = ctx

# 		super().__init__(data, per_page=3)

# 	async def write_page(self, menu, fields=[]):
# 		offset = (menu.current_page*self.per_page) + 1
# 		len_data = len(self.entries)

# 		embed = Embed(title="emoji stat",
					  
# 					  colour=self.ctx.author.colour)
# 		embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
# 		embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

# 		for name, value in fields:
# 			embed.add_field(name=name, value=value, inline=False)

# 		return embed

from discord.ext import menus
import discord

class HelpMenu(menus.ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx

		super().__init__(data, per_page=4)

	async def write_page(self, menu, offset):
		

		embed = discord.Embed(title="Top suggestions", description = offset,
					  colour=self.ctx.author.colour)
		embed.set_thumbnail(url=self.ctx.guild.icon_url)
		

	
		return embed

	async def format_page(self, menu, entries):
		offset = (menu.current_page*self.per_page) + 1


		return await self.write_page(menu, offset)

