from discord.ext.buttons import Paginator
import asyncio

import discord

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


async def reaction_buttons(
    ctx, message, functions, timeout=300.0, only_author=False, single_use=False, only_owner=False
):
    """Handler for reaction buttons
    :param message     : message to add reactions to
    :param functions   : dictionary of {emoji : function} pairs. functions must be async.
                         return True to exit
    :param timeout     : time in seconds for how long the buttons work for.
    :param only_author : only allow the user who used the command use the buttons
    :param single_use  : delete buttons after one is used
    """

    try:
        for emojiname in functions:
            await message.add_reaction(emojiname)
    except discord.errors.Forbidden:
        return

    def check(payload):
        return (
            payload.message_id == message.id
            and str(payload.emoji) in functions
            and not payload.member == ctx.bot.user
            and (
                (payload.member.id == ctx.bot.owner_id)
                if only_owner
                else (payload.member == ctx.author or not only_author)
            )
        )

    while True:
        try:
            payload = await ctx.bot.wait_for("raw_reaction_add", timeout=timeout, check=check)

        except asyncio.TimeoutError:
            break
        else:
            exits = await functions[str(payload.emoji)]()
            try:
                await message.remove_reaction(payload.emoji, payload.member)
            except discord.errors.NotFound:
                pass
            except discord.errors.Forbidden:
                await ctx.send(
                    "`error: I'm missing required discord permission [ manage messages ]`"
                )
            if single_use or exits is True:
                break

    for emojiname in functions:
        try:
            await message.clear_reaction(emojiname)
        except (discord.errors.NotFound, discord.errors.Forbidden):
            pass
async def page_switcher(ctx, pages):
    """
    :param ctx   : Context
    :param pages : List of embeds to use as pages
    """

    if len(pages) == 1:
        return await ctx.send(embed=pages[0])

    pages = TwoWayIterator(pages)

    # add all page numbers
    for i, page in enumerate(pages.items, start=1):
        old_footer = page.footer.text
        if old_footer == discord.Embed.Empty:
            old_footer = None
        page.set_footer(
            text=f"{i}/{len(pages.items)}" + (f" | {old_footer}" if old_footer is not None else "")
        )

    msg = await ctx.send(embed=pages.current())

    async def switch_page(content):
        await msg.edit(embed=content)

    async def previous_page():
        content = pages.previous()
        if content is not None:
            await switch_page(content)

    async def next_page():
        content = pages.next()
        if content is not None:
            await switch_page(content)

    functions = {"◀️": previous_page, "▶️": next_page}
    asyncio.ensure_future(reaction_buttons(ctx, msg, functions))
class TwoWayIterator:
    """Two way iterator class that is used as the backend for paging."""

    def __init__(self, list_of_stuff):
        self.items = list_of_stuff
        self.index = 0

    def next(self):
        if self.index == len(self.items) - 1:
            return None
        else:
            self.index += 1
            return self.items[self.index]

    def previous(self):
        if self.index == 0:
            return None
        else:
            self.index -= 1
            return self.items[self.index]

    def current(self):
        return self.items[self.index]