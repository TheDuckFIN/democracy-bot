"""Application main class"""

from discord.ext import commands

from .config import Config


def run():
    """Creates a bot instance and runs it"""

    config = Config.from_environ()
    bot = commands.Bot(command_prefix="!")

    @bot.event
    async def on_ready():  # pylint: disable=unused-variable
        print("Bot running")

    bot.run(config.bot_token)
