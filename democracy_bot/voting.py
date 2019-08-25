"""Cog containing voting logic and event handlers"""

from dataclasses import dataclass
from typing import Callable, Dict

import discord
from discord import Embed, Color
from discord.ext import commands

from .utils import get_name

# Limitation: works only on votes that are created after bot's startup

VOTE_YES = "\u2705"

VOTING_THRESHOLD = 1

ONGOING_VOTE_COLOR = Color.from_rgb(231, 180, 22)
SUCCESSFUL_VOTE_COLOR = Color.from_rgb(45, 201, 55)


@dataclass
class Vote:
    """Class for storing data for single vote"""

    message: discord.Message
    embed: Embed
    # Votes are user id - nickname pairs
    votes: Dict[str, str]
    success_callback: Callable[[], None]


class Voting(commands.Cog, name="voting"):
    """Cog containing the voting logic"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Vote is message ID - Vote pair (message id is the id of the message
        # that the bot posted announcing the vote)
        self.votes: Dict[str, Vote] = dict()

    @commands.Cog.listener()
    async def on_reaction_add(
        self, reaction: discord.Reaction, member: discord.Member
    ) -> None:
        """Keeps track of added vote reactions on bot's messages"""

        # Ignore own reactions
        if member.id == self.bot.user.id:
            return

        message_id = str(reaction.message.id)

        if reaction.emoji == VOTE_YES and message_id in self.votes:
            user_id = str(member.id)
            vote = self.votes[message_id]

            vote.votes[user_id] = get_name(member)

            if len(vote.votes) >= VOTING_THRESHOLD:
                await self.vote_successful(message_id)

    @commands.Cog.listener()
    async def on_reaction_remove(
        self, reaction: discord.Reaction, member: discord.Member
    ) -> None:
        """Keeps track of removed vote reactions on bot's messages"""

        message_id = str(reaction.message.id)

        if reaction.emoji == VOTE_YES and message_id in self.votes:
            user_id = str(member.id)

            self.votes[message_id].votes.pop(user_id, None)

    async def create_vote(
        self,
        ctx: commands.Context,
        title: str,
        description: str,
        callback: Callable[..., None],
    ) -> None:
        """Starts a vote to execute specified administrative action.

        React to the message with \u2705 to vote.
        """

        voting_embed = Embed(
            title=f"Vote: {title}", description=description, color=ONGOING_VOTE_COLOR
        )
        voting_embed.add_field(
            name="Status", value=f"Voting in progress. React with {VOTE_YES} to vote."
        )

        message: discord.Message = await ctx.send(embed=voting_embed)

        # Add checkmark reaction to the message for ease of use
        await message.add_reaction(VOTE_YES)

        # Add vote to
        self.votes[str(message.id)] = Vote(
            message=message, embed=voting_embed, votes=dict(), success_callback=callback
        )

    async def vote_successful(self, message_id: str) -> None:
        """Finishes the vote and executes desired action"""

        vote = self.votes[message_id]

        voters = ", ".join([name for name in vote.votes.values()])

        new_embed = Embed(
            title=vote.embed.title,
            description=vote.embed.description,
            color=SUCCESSFUL_VOTE_COLOR,
        )
        new_embed.add_field(name="Status", value=f"{VOTE_YES} vote successful")
        new_embed.add_field(name="Voters", value=voters)

        # Update embed to display new status
        await vote.message.edit(embed=new_embed)

        # Execute operation that we were voting for
        await vote.success_callback()

        self.votes.pop(message_id, None)
