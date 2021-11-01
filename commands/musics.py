import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
import youtube_dl
import re
from embeds import embed_music_added_to_queue

players = {}
queue = {}


def check_queue(ctx, guild_id):
    try:
        if len(queue[guild_id]) > 0:
            voice = ctx.voice_client
            source = queue[guild_id].pop(0)
            player = voice.play(source, after=lambda x=None: check_queue(ctx, guild_id))
    except:
        del players[guild_id]


class Musics(commands.Cog):
    """Works with musics in voice channels"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("**Você precisa estar em um Canal de Voz!**")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            channel = ctx.message.author.voice.channel
            await ctx.send(f'**Conectada ao Canal** ``{channel}``')
        else:
            await ctx.send(f'**Já estou conectada ao canal **``{ctx.voice_client.channel}``')

    @commands.command(aliases=['joinhere', 'come'])
    async def moveto(self, ctx):
        if ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.send(f'**Já estou conectada ao canal **``{ctx.voice_client.channel}``')
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            await ctx.reply(f'**Conectada agora ao Canal** ``{ctx.message.author.voice.channel}``')

    @commands.command(aliases=['disconnect, leave'])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(aliases=['p'], pass_context=True)
    async def play(self, ctx, *url):
        if ctx.author.voice is None:
            await ctx.send("**Você precisa estar conectado em um Canal de Voz!**")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            channel = ctx.message.author.voice.channel
            await ctx.send(f'**Conectada ao Canal** ``{channel}``')

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio'}

        url1 = ' '.join(url)
        padrao_url = re.compile('(http(s)?://)?(www.)?youtu(.be/)?(be.com)?/')
        match = padrao_url.match(url1)
        videosSearch = VideosSearch(url1, limit=1)
        data = videosSearch.result()
        video_link = data['result'][0]['link']
        video_title = data['result'][0]['title']

        if match:
            video_link = url1
            info = youtube_dl.YoutubeDL(YDL_OPTIONS).extract_info(url1, download=False)
            url2 = info['formats'][0]['url']
            await ctx.send(f" 🔎 **Procurando pela URL...**")
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        else:
            info = youtube_dl.YoutubeDL(YDL_OPTIONS).extract_info(video_link, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            await ctx.send(f" 🔎 **Procurando por: ** `{url1.title()}`")

        async with ctx.typing():

            guild_id = ctx.message.guild.id

            if guild_id not in players:
                guild_id = ctx.message.guild.id
                player = ctx.voice_client.play(source, after=lambda x=None: check_queue(ctx, guild_id))
                players[guild_id] = player
                await ctx.send(f"**Tocando:** 🎶 `{video_title}` 🎶")
            else:
                if guild_id not in queue:
                    queue[guild_id] = [source]
                else:
                    queue[guild_id].append(source)
                await embed_music_added_to_queue(ctx, video_title, video_link,
                                                 data['result'][0]['channel']['name'],
                                                 data['result'][0]['duration'],
                                                 data['result'][0]['thumbnails'][0]['url'],
                                                 len(queue[guild_id]))

    @commands.command()
    async def skip(self, ctx):
        guild_id = ctx.message.guild.id

        if len(queue[guild_id]) < 1:
            await ctx.send("**Não foi possível pular a música!**")

        elif queue:
            voice = ctx.voice_client
            voice.stop()
            await ctx.send(":fast_forward: **Tocando a próxima música.** ")

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("**A música foi pausada. `!resume` para continuar.**")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("**A música voltou a tocar.**")


def setup(bot):
    bot.add_cog(Musics(bot))
