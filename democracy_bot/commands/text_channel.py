""""Contains commands related to text channels"""

from typing import Optional

import discord
from discord.ext import commands

from ..utils import get_name


class TextChannel(commands.Cog):
    """Cog containing commands for text channels"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voting = bot.get_cog("voting")

    @commands.command("textchannel.create")
    @commands.guild_only()
    async def create(
        self,
        ctx: commands.Context,
        name: str,
        category: Optional[discord.CategoryChannel] = None,
    ):
        """Starts a vote to create a new text channel.

        Arguments:
        - name: Name for the text channel
        - category (optional): If specified, the text channel will be created under this category.
        """

        async def callback():
            await ctx.guild.create_text_channel(name, category=category)

        description = ""

        if category is None:
            description = f"""
                {get_name(ctx.message.author)} wants to create text channel "{name}"
                without any category.
            """
        else:
            description = f"""
                {get_name(ctx.message.author)} wants to create text channel "{name}"
                under the category "{category.name}".
            """

        await self.voting.create_vote(
            ctx, f'Create text channel "{name}"', description, callback
        )
