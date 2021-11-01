import discord
from discord.ext import commands


class Help(commands.Cog):
    @commands.command(pass_context=True)
    async def help(self, ctx):
        channel = ctx.message.channel

        embed = discord.Embed(
            color=discord.Colour.from_rgb(242, 160, 200)
        )
        embed.set_author(name='Lista de comandos do Bot')
        embed.add_field(name='join', value='Chama o Bot para o seu Canal de Voz', inline=False)
        embed.add_field(name='leave', value='Disconecta o bot do canal de voz.', inline=False)
        embed.add_field(name='play', value='Toca músicas', inline=False)
        embed.add_field(name='skip', value='Pula para a próxima música caso exista uma na fila.', inline=False)
        embed.add_field(name='pause', value='Pausa a música que está tocando.', inline=False)
        embed.add_field(name='resume', value='Retorna a música que estava tocando.', inline=False)
        embed.add_field(name='stop', value='Para a música que está tocando e remove o Bot do canal de voz'
                        , inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
