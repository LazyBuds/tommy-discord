import discord
from discord.ext import commands
import arrow
import asyncpraw
import os
from discord.ext import commands
import asyncprawcore
# from helpers import emojis, utilityfunctions as util
from discord.ext.commands import Cog, command
from ..db import db





UPVOTE = "<:redditupvote:805411532400754699>"

GREEN_UP = "<:green_triangle_up:749966847788449822>"
RED_DOWN = "<:red_triangle_down:749966805908455526>"

LOADING = "<a:loading:749966819514777690>"
TYPING = "<a:typing:749966793480732694>"
CLIENT_ID = 'Koj2wUuGJ06FNg'
CLIENT_SECRET = 'Z5CGO0EfLmQFpDJoe_rTt7FplE9rFw'
class RedditError(commands.CommandError):
    pass

class Reddit(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot = bot
        self.timespans = ["all", "day", "hour", "week", "month", "year"]
        self.human_ts = {
            "all": "all-time",
            "day": "daily",
            "hour": "hourly",
            "week": "weekly",
            "month": "monthly",
            "year": "yearly",
        }
        self.client = asyncpraw.Reddit(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent="tommy"
        )
        
        

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







       

    # COMMANDS

    @commands.group(name="reddit", description ="Reddit commands." , usage = '+reddit')
    @custom_check()
    @commands.cooldown(2,30,commands.BucketType.user)
    async def reddit(self, ctx):
      
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @reddit.command(name="random", aliases=["r"], description = "Get random post from given subreddit.", usage = '+reddit random <subreddit>')
    async def reddit_random(self, ctx, subreddit):
        '''+reddit random dogs'''
      
        subreddit = await self.client.subreddit(subreddit.lower())
        try:
            post = await subreddit.random()
        except asyncprawcore.exceptions.NotFound as e:
            if e.response.status == 404:
                return await ctx.send(
                    f":warning: `r/{subreddit}` is either banned or doesn't exist!"
                )
            elif e.response.status == 403:
                return await ctx.send(
                    f":warning: `r/{subreddit}` is either quarantined or private!"
                )
            else:
                raise e

        if post is None:
            return await ctx.send(
                "Sorry, this subreddit does not support the random post feature!"
            )

       

        await self.send_post(ctx, subreddit, post, f"Random post from r/{subreddit}")

    @reddit.command(name="hot", aliases=["h"], description  = "Get hot post from given subreddit.", usage  = '+reddit hot <subreddit> <index>')
    async def reddit_hot(self, ctx, subreddit, number="1"):
        """"+reddit hot saimansays 5"""
        if not await self.check_n(ctx, number):
            return

        subreddit = await self.client.subreddit(subreddit.lower())
        post = await get_n_post(subreddit.hot(), number)

        await self.send_post(ctx, subreddit, post, f"#{number} hottest post from r/{subreddit}")

    @reddit.command(name="controversial", aliases=["c"], description = "Get controversial post from given subreddit.", usage = '+reddit c <subreddit> <index> <timespan>')
    async def reddit_controversial(self, ctx, subreddit, number="1", timespan="all"):
        """"+reddit controversial saimansays 1 all"""
        timespan = await self.check_ts(ctx, timespan)
        if timespan is None or not await self.check_n(ctx, number):
            return

        subreddit = await self.client.subreddit(subreddit.lower())
        post = await get_n_post(subreddit.controversial(timespan), number)

        await self.send_post(
            ctx,
            subreddit,
            post,
            f"#{number} most controversial {self.human_ts[timespan]} post from r/{subreddit}",
        )

    @reddit.command(name="top", aliases=["t"], description ="Get top post from given subreddit.", usage = '+reddit top <subreddit> <index> <timespan>' )
    async def reddit_top(self, ctx, subreddit, number="1", timespan="all"):
        """+reddit top saimansays 1 all"""
        timespan = await self.check_ts(ctx, timespan)
        if timespan is None or not await self.check_n(ctx, number):
            return

        subreddit = await self.client.subreddit(subreddit.lower())
        post = await get_n_post(subreddit.top(timespan), number)

        await self.send_post(
            ctx,
            subreddit,
            post,
            f"#{number} top {self.human_ts[timespan]} post from r/{subreddit}",
        )

    @reddit.command(name="new", aliases=["n"], description = "Get new post from given subreddit.", usage = '+reddit new <subreddit> <index>')
    async def reddit_new(self, ctx, subreddit, number="1"):
        """"+reddit new saimansays 1"""
        if not await self.check_n(ctx, number):
            return

        subreddit = await self.client.subreddit(subreddit.lower())
        post = await get_n_post(subreddit.new(), number)

        await self.send_post(ctx, subreddit, post, f"#{number} newest post from r/{subreddit}")

    # FUNCTIONS

    async def send_post(self, ctx, subreddit, post, footer=""):
        """Checks for eligibility for sending submission and sends it."""
        try:
            await subreddit.load()
        except asyncprawcore.exceptions.NotFound:
            if str(subreddit) != "all":
               return await ctx.send('subreddit not found')

        if not can_send_nsfw(ctx, subreddit):
            return await ctx.send(
                ":underage: NSFW subreddits can only be viewed in an NSFW channel!"
            )

        try:

            content, message_content = await self.render_submission(post, not ctx.channel.is_nsfw())
            content.set_footer(text=footer)
            await ctx.send(embed=content)
            if message_content is not None:
                await ctx.send(message_content)

        except:
            await ctx.send('empty submission')

    async def render_submission(self, submission, censor=True):
        """Turns reddit submission into a discord embed."""
        if submission is not None:


            message_text = None
            content = discord.Embed(color  = 0xff2d33)
            content.title = (
                f"`[{submission.link_flair_text}]` "
                if hasattr(submission, "link_flair_text") and submission.link_flair_text is not None
                else ""
            )
            try:
                content.title += submission.title
            except:
                pass


            try:

    

                content.timestamp = arrow.get(submission.created_utc).datetime
            except:
                pass

            redditor = submission.author
            if redditor is None:
                # deleted user
                content.set_author(name="[deleted]")
            else:
                await redditor.load()
                content.set_author(
                    name=f"u/{redditor.name}",
                    url=f"https://old.reddit.com/u/{redditor.name}",
                    icon_url=(
                        redditor.icon_img if hasattr(redditor, "icon_img") else discord.Embed.Empty
                    ),
                )

            suffix_elements = [
                f"{UPVOTE} {submission.score} ({int(submission.upvote_ratio*100)}%)",
                f"{submission.num_comments} comment" + ("s" if submission.num_comments > 1 else ""),
                f"[Permalink](https://old.reddit.com{submission.permalink})",
            ]
            suffix = "\n\n**" + " | ".join(suffix_elements) + "**"

            if submission.is_self:
                submission.selftext = submission.selftext.replace("&#x200B;", "")
                if len(submission.selftext + suffix) > 2044:
                    content.description = submission.selftext[: (2044 - len(suffix) - 3)] + "..."
                else:
                    content.description = submission.selftext
            else:
                hide = submission.spoiler or (submission.over_18 and censor)
                content.description = ""
                if not hide and is_image_post(submission):
                    content.set_image(url=submission.url)
                else:
                    url = submission.url
                    if hide:
                        url = "||" + url + "||"
                    if self_embeds(submission.url):
                        message_text = url
                    else:
                        content.description = url

            content.description.strip()
            if submission.over_18:
                content.title = "`[NSFW]` " + content.title

            elif submission.spoiler:
                content.title = "`[SPOILER]` " + content.title

            if submission.is_self and ((censor and submission.over_18) or submission.spoiler):
                content.description = "||" + content.description + "||"

            content.description += suffix
            return content, message_text

        


    async def check_ts(self, ctx, timespan):
        """Validates timespan argument."""
        timespan = timespan.lower()
        if timespan not in self.timespans:
            await ctx.send(
                f":warning: Invalid timespan `{timespan}` please use one of: `{self.timespans}`"
            )
            return None
        return timespan

    async def check_n(self, ctx, number):
        """Validates number argument."""
        try:
            number = int(number)
        except ValueError:
            await ctx.send(f":warning: `number` must be an integer, not `{number}`")
            return False

        if number < 1 or number > 50:
            await ctx.send(":warning: `number` must be between `1` and `50`")
            return False
        else:
            return True


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("reddit")


async def get_n_post(gen, n, ignore_sticky=True):
    """Gets the n:th submission from given PRAW ListingGenerator."""
    if gen is not None:
        n = int(n)
        i = 1
        try:
            async for post in gen:
                if post.stickied and ignore_sticky:
                    n += 1
                if i >= n:
                    return post
                else:
                    i += 1
        except asyncprawcore.exceptions.Redirect:
            # raise RedditError("this subreddit doesn't seem to exist!")
            pass
        except asyncprawcore.exceptions.NotFound:
            pass


def is_image_post(submission):
    """is submission content embedable image."""
    return (not submission.is_self) and submission.url.endswith((".png", ".jpg", ".jpeg", ".gif"))


def self_embeds(url):
    """Does this url generate a usable embed on it's own when sent on discord?"""
    return (
        url.startswith("https://www.youtube.com")
        or url.startswith("https://youtu.be")
        or url.startswith("https://imgur.com")
        or url.startswith("https://www.imgur.com")
        or url.startswith("https://gfycat.com")
        or url.startswith("https://www.gfycat.com")
        or url.startswith("https://redgifs.com")
        or url.startswith("https://www.redgifs.com")
    )


def can_send_nsfw(ctx, content):
    """Checks whether content is NSFW and if so whether it can be sent in current channel."""
    if isinstance(content, asyncpraw.models.Submission):
        is_nsfw = content.over_18
    elif isinstance(content, asyncpraw.models.Subreddit):
        is_nsfw = content.over18
    else:
        return True

    if is_nsfw:
        return ctx.channel.is_nsfw()
    else:
        return True


    
            
            


def setup(bot) :
    
    bot.add_cog(Reddit(bot))