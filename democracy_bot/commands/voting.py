"""Commands related to voting"""

import discord
from discord.ext import commands

# Limitation: works only on votes that are created after bot's startup

VOTE_YES = "\u2705"
VOTE_NO = "\u274C"


class Voting(commands.Cog):
    """Cog containing the voting logic and commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(
        self, reaction: discord.Reaction, member: discord.Member
    ) -> None:
        """Keeps track of added votes on bot's messages"""

        # Ignore own reactions
        if member.id == self.bot.user.id:
            return

        print(f"Reaction added by {member}: {reaction}")

    @commands.Cog.listener()
    async def on_reaction_remove(
        self, reaction: discord.Reaction, member: discord.Member
    ) -> None:
        """Keeps track of removed votes on bot's messages"""

        # Ignore own reactions
        if member.id == self.bot.user.id:
            return

        print(f"Reaction removed by {member}: {reaction}")

    @commands.command()
    @commands.guild_only()
    async def vote(self, ctx: commands.Context) -> None:
        """Starts a vote to execute specified administrative action.

        React to the message with \u2705 or \u274C to vote.
        """

        message: discord.Message = await ctx.send("Hello world!")

        # Add checkmark and cross reactions to the message
        await message.add_reaction(VOTE_YES)
        await message.add_reaction(VOTE_NO)
