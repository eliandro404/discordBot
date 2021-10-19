from discord.ext import commands, tasks
from decouple import config


class Ready(commands.Cog):
    """Em desenvolvimento..."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.say_its_ready.start()

    @tasks.loop(count=1)
    async def say_its_ready(self):
        canal_texto = int(config("ID_CANAL_TEXTO"))
        channel = self.bot.get_channel(canal_texto)
        await channel.send("Olá, estou pronta.")


def setup(bot):
    bot.add_cog(Ready(bot))
