import os
from decouple import config
from discord.ext import commands, tasks

bot = commands.Bot("!")
bot.remove_command('help')


def load_cogs(bot):
    bot.load_extension("manager")
    bot.load_extension("tasks.ready")
    bot.load_extension("tasks.change_status")

    for file in os.listdir("commands"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f"commands.{cog}")


load_cogs(bot)

TOKEN = config("TOKEN")
bot.run(TOKEN)
