import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
import youtube_dl
import re


async def embed_generator_for_musics(ctx, name, channel, duration, url_thumbnail, queue_position):
    embed_image = discord.Embed(
        title=name,
        # description='',
        color=discord.Colour.from_rgb(242, 160, 200)
    )
    embed_image.set_author(name=f'{ctx.author.name} - Adicionou uma música a fila',
                           icon_url=ctx.author.avatar_url)
    embed_image.set_image(url=url_thumbnail)
    embed_image.add_field(name="Canal", value=channel)
    embed_image.add_field(name="Duração", value=duration)
    embed_image.add_field(name="Posição na Fila", value=queue_position)

    return await ctx.send(embed=embed_image)


players = {}
queue = {}


def check_queue(ctx, id):
    try:
        if queue != []:
            voice = ctx.voice_client
            source = queue[id].pop(0)
            print(len(queue))
            player = voice.play(source, after=lambda x=None: check_queue(ctx, id))
    except:
        del players[id]


def start_playing(voice_client, source, ctx):
    guild_id = ctx.message.guild.id

    queue[0] = source

    i = 0
    while i < len(queue):
        try:
            player = voice_client.play(queue[i], after=lambda x=None: check_queue(ctx, guild_id))
            players[guild_id] = player
        except:
            pass
        i += 1


class Musics(commands.Cog):
    """Works with musics in voice channels"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Chama o Bot para o seu Canal de Voz.")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Você precisa estar em um Canal de Voz!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            channel = ctx.message.author.voice.channel
            await ctx.send(f'**Conectada ao Canal** ``{channel}``')
        else:
            await ctx.send(f'**Já estou conectada ao canal **``{ctx.voice_client.channel}``')
            # await ctx.voice_client.move_to(voice_channel)

    @commands.command(name='leave', help="Disconecta o Bot do Canal de Voz.")
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(aliases=['p'], help="Toca músicas.", pass_context=True)
    async def play(self, ctx, *url):

        if ctx.author.voice is None:
            await ctx.send("Você precisa estar em um Canal de Voz!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            channel = ctx.message.author.voice.channel
            await ctx.send(f'**Conectada ao Canal** ``{channel}``')
        else:
            pass
            # await ctx.send(f'Já estou no canal **{ctx.voice_client.channel}**')
            # await ctx.voice_client.move_to(voice_channel)

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio'}
        vc = ctx.voice_client

        url1 = ' '.join(url)
        padrao_url = re.compile('(http(s)?://)?(www.)?youtu(.be/)?(be.com)?/')

        match = padrao_url.match(url1)
        videosSearch = VideosSearch(url1, limit=1)
        data = videosSearch.result()
        video_link = data['result'][0]['link']
        video_title = data['result'][0]['title']

        if match:
            info = youtube_dl.YoutubeDL(YDL_OPTIONS).extract_info(url1, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        else:
            info = youtube_dl.YoutubeDL(YDL_OPTIONS).extract_info(video_link, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

        async with ctx.typing():

            guild_id = ctx.message.guild.id

            if guild_id not in players:

                await ctx.send(f" 🔎 **Procurando por: ** `{url1.title()}`")
                start_playing(vc, source, ctx)
                await ctx.send(f"**Tocando:** 🎶 `{video_title}` 🎶")

            else:
                if guild_id in queue:
                    queue[guild_id].append(source)
                else:
                    queue[guild_id] = [source]
                await embed_generator_for_musics(ctx, video_title,
                                                 data['result'][0]['channel']['name'],
                                                 data['result'][0]['duration'],
                                                 data['result'][0]['thumbnails'][0]['url'],
                                                 len(queue))

    @commands.command()
    async def skip(self, ctx):
        if len(queue) == 1:
            await ctx.send("**Não foi possível pular a música!**")

        elif queue != []:
            ctx.voice_client.stop()
            voice = ctx.voice_client
            source = queue[id].pop(0)
            player = voice.play(source, after=lambda x=None: check_queue(ctx, id))
            await ctx.send(":fast_forward: **Tocando a próxima música.** ")

    @commands.command(name='stop', help='Para a música que está tocando e remove o BOT do canal de voz.')
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(help="Pausa a música que está tocando.")
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("**A música foi pausada. `!resume` para continuar.**")

    @commands.command(help="Retorna a música que estava tocando.")
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("**A música voltou a tocar.**")


def setup(bot):
    bot.add_cog(Musics(bot))
