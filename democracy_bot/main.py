"""Application main class"""

from discord.ext import commands

from .config import Config
from .commands.voting import Voting

# pylint: disable=unused-variable


def run():
    """Creates a bot instance and runs it"""

    config = Config.from_environ()
    bot = commands.Bot(command_prefix="!")

    bot.add_cog(Voting(bot))

    @bot.event
    async def on_ready():
        print("Bot running")

    @bot.event
    async def on_command_error(ctx, error):
        # Ignore errors that are expected (e.g. from checks)
        if isinstance(error, commands.NoPrivateMessage):
            return
        raise error

    bot.run(config.bot_token)
