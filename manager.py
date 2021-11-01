from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound


class Manager(commands.Cog):
    """Manage the bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Olá, sou Euterpe. Estou conectado como {self.bot.user}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # if "Euterpe" in message.content:
        #     await message.channel.send(f'Ei {message.author.name}, me chamou?')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("**Favor enviar todos os Argumentos! Digite !help para ver os parâmetros do comando.**")
        elif isinstance(error, CommandNotFound):
            await ctx.send("**O comando não existe. Digite !help para ver todos os comandos.**")
        else:
            raise error


def setup(bot):
    bot.add_cog(Manager(bot))
