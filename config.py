settings = {
	'TOKEN': 'OTk5Mjk3MzgxMDk3MDI5NjMy.GoCSQ7.PeDhf-aM2-LkYfd2steSMjDsrlxWg3wFG-092c',
	'NAME BOT': 'damn_bot',
	'ID': '995677545905279106',
	'PREFIX': '$',
	'OWNER': 'DAMN#6054',
	'OWNER NAME': 'DAMN',
	'ADMIN ROLE 1': 'ГенСек',
    'ADMIN ROLE 2': 'SF experience',
	'CHANEL ID': '998621149053321297',
    'CATEGORY ID': '703022598782713887'
}
'''
@bot.command()
@commands.has_role(settings['ADMIN ROLE'])
async def change_channel(ctx, arg):
    channel = discord.utils.get(ctx.guild.channels , name = arg )
    try:
        settings['CHANEL ID'] = str(channel.id)
        await ctx.reply(f'Chanel was changed:\n\n'
                        f'Channel name:     ' + channel.name + '\n'
                        f'Chanel id:     ' + settings['CHANEL ID'])
    except:
        await ctx.reply(f'ERROR! CHANNEL DOESNT EXIST!')
'''