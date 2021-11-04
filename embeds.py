from discord import Embed, Colour


async def embed_music_added_to_queue(ctx, name, url, channel, duration, url_thumbnail, queue_position):
    embed_image = Embed(
        title=name,
        # url=url,
        # description='',
        color=Colour.from_rgb(242, 160, 200)
    )
    embed_image.set_author(name=f'{ctx.author.name} - Adicionou uma música a fila',
                           icon_url=ctx.author.avatar_url)
    embed_image.set_thumbnail(url=url_thumbnail)
    embed_image.add_field(name="Canal", value=channel)
    embed_image.add_field(name="Duração", value=duration)
    embed_image.add_field(name="Posição na Fila", value=queue_position)

    return await ctx.send(embed=embed_image)


async def embed_music_queue_list(ctx, playing_now, queue_names_list):
    embed_list = ''
    embed = Embed(
        title='**Fila atual:**',
        color=Colour.from_rgb(242, 160, 200)
    )
    for i in queue_names_list:
        embed_list += f'**`{queue_names_list.index(i) + 1}.` {i.title()}**\n'
    embed.set_thumbnail(url='https://uploads.spiritfanfiction.com/fanfics/capitulos/202010/solangelo--quando-o-sol-e'
                            '-a-lua-se-encontram-20789447-191020202011.gif')
    embed.add_field(name=f'**Tocando agora:** 🎶 `{playing_now.title()}` 🎶', value='\u200b', inline=False)
    embed.add_field(name='⬇️Próximas músicas⬇', value=embed_list)

    return await ctx.send(embed=embed)
