import discord


async def embed_music_added_to_queue(ctx, name, url, channel, duration, url_thumbnail, queue_position):
    embed_image = discord.Embed(
        title=name,
        # url=url,
        # description='',
        color=discord.Colour.from_rgb(242, 160, 200)
    )
    embed_image.set_author(name=f'{ctx.author.name} - Adicionou uma música a fila',
                           icon_url=ctx.author.avatar_url)
    embed_image.set_thumbnail(url=url_thumbnail)
    embed_image.add_field(name="Canal", value=channel)
    embed_image.add_field(name="Duração", value=duration)
    embed_image.add_field(name="Posição na Fila", value=queue_position)

    return await ctx.send(embed=embed_image)
