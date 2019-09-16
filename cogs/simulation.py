from random import choice
from asyncio import TimeoutError as AsyncTimeoutError

import discord
from discord.ext.commands import command, Context, cooldown
from discord.ext.commands import MissingRequiredArgument, CommandOnCooldown, BadArgument
from discord.ext.commands.cooldowns import BucketType

from cogs.utils.custom_bot import CustomBot
from cogs.utils.family_tree.family_tree_member import FamilyTreeMember
from cogs.utils.custom_cog import Cog
from cogs.utils.random_text.copulate import CopulateRandomText
from cogs.utils.checks.bot_is_ready import bot_is_ready, BotNotReady
from cogs.utils.acceptance_check import AcceptanceCheck


class Simulation(Cog):
    """A class to handle the simulation commands inside of the bot"""

    def __init__(self, bot:CustomBot):
        super().__init__(self.__class__.__name__)
        self.bot = bot

    async def cog_command_error(self, ctx:Context, error):
        """Local error handler for the cog - mostly cooldown and missing args"""

        # Throw errors properly for me
        if ctx.original_author_id in self.bot.owners and not isinstance(error, CommandOnCooldown):
            text = f'```py\n{error}```'
            await ctx.send(text)
            raise error

        # Missing argument
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("You need to specify a person for this command to work properly.")
            return

        # Cooldown
        elif isinstance(error, CommandOnCooldown):
            if ctx.original_author_id in self.bot.owners:
                await ctx.reinvoke()
            else:
                await ctx.send(f"You can only use this command once every `{error.cooldown.per:.0f} seconds` per server. You may use this again in `{error.retry_after:.2f} seconds`.")
            return

        # Argument conversion error
        elif isinstance(error, BadArgument):
            argument_text = self.bot.bad_argument.search(str(error)).group(2)
            await ctx.send(f"User `{argument_text}` could not be found.")
            return

        # Bot ready
        elif isinstance(error, BotNotReady):
            await ctx.send("The bot isn't ready to start processing that command yet - please wait.")
            return

    @command(aliases=['snuggle'])
    @cooldown(1, 5, BucketType.user)
    async def hug(self, ctx:Context, user:discord.Member):
        """Hugs a mentioned user"""

        if user == ctx.author:
            await ctx.send(f"*You hug yourself... and start crying.*")
        else:
            await ctx.send(f"*Hugs {user.mention}*")

    @command()
    @bot_is_ready()
    @cooldown(1, 5, BucketType.user)
    async def kiss(self, ctx:Context, user:discord.Member):
        """Kisses a mentioned user"""

        # Check if they're themself
        if user == ctx.author:
            await ctx.send(f"How would you even manage to do that?")
            return

        # Check if they're related
        x = FamilyTreeMember.get(ctx.author.id)
        y = FamilyTreeMember.get(user.id)
        async with ctx.channel.typing():
            relationship = x.get_relation(y)

        # Generate responses
        if relationship == None or relationship.casefold() == 'partner':
            responses = [
                f"*Kisses {user.mention}*"
            ]
        else:
            responses = [
                f"Woah woah, you two are family!",
                f"Incest is wincest, I guess.",
                f"You two are related but go off I guess.",
            ]

        # Boop an output
        await ctx.send(choice(responses))

    @command()
    @cooldown(1, 5, BucketType.user)
    async def slap(self, ctx:Context, user:discord.Member):
        """Slaps a mentioned user"""

        if user == ctx.author:
            await ctx.send(f"*You slapped yourself... for some reason.*")
        else:
            await ctx.send(f"*Slaps {user.mention}*")

    @command()
    @cooldown(1, 5, BucketType.user)
    async def punch(self, ctx:Context, user:discord.Member):
        """Punches a mentioned user"""

        if user == ctx.author:
            await ctx.send("*You punched yourself... for some reason.*")
        else:
            await ctx.send(f"*Punches {user.mention} right in the nose*")

    @command()
    @cooldown(1, 5, BucketType.user)
    async def cookie(self, ctx:Context, user:discord.Member):
        """Gives a cookie to a mentioned user"""

        if user == ctx.author:
            await ctx.send("*You gave yourself a cookie.*")
        else:
            await ctx.send(f"*Gives {user.mention} a cookie*")

    @command()
    @cooldown(1, 5, BucketType.user)
    async def poke(self, ctx:Context, user:discord.Member):
        """Pokes a given user"""

        if user == ctx.author:
            await ctx.send("You poke yourself.")
        else:
            await ctx.send(f"*Pokes {user.mention}.*")

    @command()
    @cooldown(1, 5, BucketType.user)
    async def stab(self, ctx:Context, user:discord.Member):
        """Stabs a mentioned user"""

        if user == ctx.author:
            responses = [
                f"You stab yourself.",
                f"Looks like you don't have a knife, oops!",
                f"No.",
            ]
        else:
            responses = [
                f"You stab {user.mention}.",
                f"{user.mention} has been stabbed.",
                f"*stabs {user.mention}.*",
                f"Looks like you don't have a knife, oops!",
                "You can't legally stab someone without thier consent.",
                "Stab? Isn't that, like, illegal?",
                "I wouldn't recommend doing that tbh.",
            ]
        await ctx.send(choice(responses))

    @command(hidden=True, aliases=['murder'])
    async def kill(self, ctx:Context, user:discord.Member=None):
        """Kills a person :/"""

        responses = [
            "That would violate at least one of the laws of robotics.",
            "I am a text-based bot. I cannot kill.",
            "Unfortunately, murder isn't supported in this version of MarriageBot.",
            "Haha good joke there, but I'd never kill a person! >.>",
            "To my knowledge, you can't kill via the internet. Let me know when that changes.",
            "I am designed to bring people together, not murder them.",
        ]
        await ctx.send(choice(responses))

    @command(aliases=['vore'], hidden=True)
    async def eat(self, ctx:Context, user:discord.Member=None):
        """Eats a person OwO"""

        responses = [
            f"You swallowed {user.mention}... through the wrong hole.",
            f"You've eaten {user.mention}. Gross.",
            f"Are you into this or something? You've eaten {user.mention}.",
            f"I guess lunch wasnt good enough. You eat {user.mention}.",
            f"You insert {user.mention} into your mouth and proceed to digest them.",
        ]
        await ctx.send(choice(responses))

    @command(hidden=True)
    async def sleep(self, ctx:Context):
        """Todd Howard strikes once more"""

        await ctx.send("You sleep for a while and when you wake up you're in a cart "
                       "with your hands bound. A man says \"Hey, you. You're finally "
                       "awake. You were trying to cross the border, right?\"")

    @command(aliases=['intercourse', 'fuck', 'smash'])
    @bot_is_ready()
    @cooldown(1, 5, BucketType.user)
    async def copulate(self, ctx:Context, user:discord.Member):
        """Let's you... um... heck someone"""

        # Check for NSFW channel
        if not ctx.channel.is_nsfw():
            await ctx.send("This command can't be run in a non-NSFW channel.")
            return

        # Check for the most common catches
        text_processor = CopulateRandomText(self.bot)
        text = text_processor.process(ctx.author, user)
        if text:
            await ctx.send(text)
            return

        # Check if they are related
        x = FamilyTreeMember.get(ctx.author.id)
        y = FamilyTreeMember.get(user.id)
        async with ctx.channel.typing():
            relationship = x.get_relation(y)
        if relationship == None or relationship.casefold() == 'partner':
            pass
        elif not self.bot.allows_incest(ctx.guild.id):
            pass
        else:
            await ctx.send(text_processor.target_is_relation(ctx.author, user))
            return

        # Ping out a message for them
        await ctx.send(text_processor.valid_target(ctx.author, user))

        # Wait for a response
        try:
            check = AcceptanceCheck(user.id, ctx.channel.id).check
            m = await self.bot.wait_for('message', check=check, timeout=60.0)
            response = check(m)
        except AsyncTimeoutError:
            await ctx.send(text_processor.proposal_timed_out(ctx.author, user), ignore_error=True)
            return

        # Process response
        if response == "NO":
            await ctx.send(text_processor.request_denied(ctx.author, user))
            return
        await ctx.send(text_processor.request_accepted(ctx.author, user))


def setup(bot:CustomBot):
    x = Simulation(bot)
    bot.add_cog(x)
