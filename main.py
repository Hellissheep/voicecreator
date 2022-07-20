import discord
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['PREFIX'])

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("/help"))
    print (f"Logged on as {settings['NAME BOT']}")

@bot.slash_command(name = "help" , description = "Commands list")
async def help(ctx):
    await ctx.respond(f'I have only two command:\n'
                f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                f'🥇 /change_channel - change the channel to click on\n'
                f'🥈 /change_category - change the category where channels are created'
                )

@bot.slash_command(name = "change_channel", description = "Change the channel to click on")
async def change_channel(ctx , channel_name_or_id):
        role_1 = discord.utils.get(ctx.guild.roles, name = settings['ADMIN ROLE 1'])
        role_2 = discord.utils.get(ctx.guild.roles, name = settings['ADMIN ROLE 2'])
        if role_1 not in ctx.author.roles or role_2 not in ctx.author.roles:
            await ctx.respond(f'🛑YOU DONT HAVE NECESSARY PERMISSIONS🛑')
            return
        try:
            channel = discord.utils.get(ctx.guild.channels, id = int(channel_name_or_id))
            settings['CHANEL ID'] = str(channel.id)
            await ctx.respond(f'✅ Chanel was changed:\n'
                              f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                              f'📻 Channel name:     ' + channel.name + '\n'
                              f'📟 Chanel id:     ' + settings['CHANEL ID'])
        except:
            try:
                channel1 = discord.utils.get(ctx.guild.channels, name = channel_name_or_id)
                settings['CHANEL ID'] = str(channel1.id)
                await ctx.respond(f'✅ Chanel was changed:\n'
                                  f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                  f'📻 Channel name:     ' + channel1.name + '\n'
                                  f'📟 Chanel id:     ' + settings['CHANEL ID'])
            except:
                await ctx.respond(f'🛑ERROR! CHANNEL DOESNT EXIST!🛑')

@bot.slash_command(name = "change_category", description = "Change the category where channels are created")
async def change_category(ctx , category_name_or_id):
        role_1 = discord.utils.get(ctx.guild.roles, name=settings['ADMIN ROLE 1'])
        role_2 = discord.utils.get(ctx.guild.roles, name=settings['ADMIN ROLE 2'])
        if role_1 not in ctx.author.roles or role_2 not in ctx.author.roles:
            await ctx.respond(f'🛑YOU DONT HAVE NECESSARY PERMISSIONS🛑')
            return
        for guild in bot.guilds:
            try:
                category = discord.utils.get(guild.categories, name = str(category_name_or_id))
                settings['CATEGORY ID'] = str(category.id)
                await ctx.respond(f'✅ Category was changed:\n'
                                  f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                  f'📻 Category name:     ' + category.name + '\n'
                                  f'📟 Category id:     ' + settings['CATEGORY ID'])
            except:
                try:
                    category = discord.utils.get(guild.categories, id = int(category_name_or_id))
                    settings['CATEGORY ID'] = str(category.id)
                    await ctx.respond(f'✅ Category was changed:\n'
                                      f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                      f'📻 Category name:     ' + category.name + '\n'
                                      f'📟 Category id:     ' + settings['CATEGORY ID'])
                except:
                    await ctx.respond(f'🛑ERROR! CATEGORY DOESNT EXIST!🛑')

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel != None:
        if after.channel.id == int(settings['CHANEL ID']):
            for guild in bot.guilds:
                _category = discord.utils.get(guild.categories, id = int(settings['CATEGORY ID']))
                channel2 = await guild.create_voice_channel(
                    f'🎤   {member.display_name}',
                    category = _category,
                    bitrate = 96000
                )
                await channel2.set_permissions(member, connect=True, mute_members=True, move_members=True, manage_channels=True)
                await member.move_to(channel2)
                def check(x, y, z):
                    return len(channel2.members) == 0
                await bot.wait_for('voice_state_update', check = check)
                await channel2.delete()

bot.run (settings['TOKEN']) 