import discord
from discord.ext import commands
from config import settings

def have_roles(ctx):
    role_1 = discord.utils.get(ctx.guild.roles, name=settings['ADMIN ROLE 1'])
    role_2 = discord.utils.get(ctx.guild.roles, name=settings['ADMIN ROLE 2'])
    if settings['NEED ROLES'] == '1':
        if role_1 not in ctx.author.roles:
            return  False
    elif settings['NEED ROLES'] == '2':
        if role_1 not in ctx.author.roles or role_2 not in ctx.author.roles:
            return False
    elif settings['NEED ROLES'] == 'any':
        if role_1 not in ctx.author.roles and role_2 not in ctx.author.roles:
            return False
    return True

bot = commands.Bot(command_prefix = settings['PREFIX'])

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("/help"))
    print (f"Logged on as {settings['NAME BOT']}")

@bot.slash_command(name = "help" , description = "Commands list")
async def help(ctx):
    if not have_roles(ctx):
        await ctx.respond(f'🛑YOU DONT HAVE NECESSARY PERMISSIONS🛑')
        return
    await ctx.respond(f'📒 Main commands list:\n'
                f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                f'1️⃣ /change_channel - change the channel to click on\n'
                f'〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n'
                f'2️⃣ /change_category - change the category where channels are created\n'
                f'〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n'
                f'3️⃣ /roles_list - check roles need to manage the bot\n'
                f'〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n'
                f'4️⃣ /change_role_1 - change role 1 to manage the bot\n'
                f'〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n'
                f'5️⃣ /change_role_2 - change role 2 to manage the bot\n'
                f'〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n'
                f'6️⃣ /change_need_roles - change count roles need to manage bot\n'
                f'〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n'
                f'        The command \"/change_need_roles\" have 4 type of argument:\n'
                f'〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n'
                f'          1️⃣  0  - ❗ATTENTION❗ If set 0 , anyone will be able to use the bot commands\n'
                f'          2️⃣  1  - only who have FIRST role will be able to manage the bot\n'
                f'          2️⃣  2  - only who have BOTH role will be able to manage the bot\n'
                f'          4️⃣ any - only who have at least ONE of the TWO roles will be able to mange the bot \n'
                f'〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n'
                )

@bot.slash_command(name = "roles_list" , description = "Check roles need to manage the bot")
async def roles_list(ctx):
    if not have_roles(ctx):
        await ctx.respond(f'🛑YOU DONT HAVE NECESSARY PERMISSIONS🛑')
        return
    if settings['NEED ROLES'] == '1':
        await ctx.respond(f'Roles need to manage bot:\n'
                          f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                          f'1️⃣ Role 1 - ' + settings['ADMIN ROLE 1']
                          )
    elif settings['NEED ROLES'] == '2':
        await ctx.respond(f'Roles need to manage bot:\n'
                          f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                          f'1️⃣ Role 1 - ' + settings['ADMIN ROLE 1'] + '\n'
                          f'2️⃣ Role 2 - ' + settings['ADMIN ROLE 2'] + '\n'
                          )
    elif settings['NEED ROLES'] == 'any':
        await ctx.respond(f'Roles need to manage bot:\n'
                          f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                          f'1️⃣ Role 1 - ' + settings['ADMIN ROLE 1'] + '\n'
                          f'➖➖➖➖➖➖  OR  ➖➖➖➖➖➖\n'                          
                          f'2️⃣ Role 2 - ' + settings['ADMIN ROLE 2'] + '\n'
                          )
    else:
        await ctx.respond(f'❗ANYONE CAN MANAGE THE BOT❗')

@bot.slash_command(name = "change_channel", description = "Change the channel to click on")
async def change_channel(ctx , channel_name_or_id):
        if not have_roles(ctx):
            await ctx.respond(f'🛑YOU DONT HAVE NECESSARY PERMISSIONS🛑')
            return
        try:
            try:
                channel = discord.utils.get(ctx.guild.channels, id = int(channel_name_or_id))
            except:
                channel = discord.utils.get(ctx.guild.channels, name = str(channel_name_or_id))
            settings['CHANEL ID'] = str(channel.id)
            await ctx.respond(f'✅ Chanel was changed:\n'
                              f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                              f'📻 Channel name:     ' + channel.name + '\n'
                              f'📟 Chanel id:     ' + settings['CHANEL ID'])
        except:
            await ctx.respond(f'🛑ERROR! CHANNEL DOESNT EXIST!🛑')

@bot.slash_command(name = "change_category", description = "Change the category where channels are created")
async def change_category(ctx , category_name_or_id):
        if not have_roles(ctx):
            await ctx.respond(f'🛑YOU DONT HAVE NECESSARY PERMISSIONS🛑')
            return

        for guild in bot.guilds:
            try:
                try:
                     category = discord.utils.get(guild.categories, id = int(category_name_or_id))
                except:
                     category = discord.utils.get(guild.categories, name = str(category_name_or_id))
                settings['CATEGORY ID'] = str(category.id)
                await ctx.respond(f'✅ Category was changed:\n'
                                  f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n' 
                                  f'📻 Category name:     ' + category.name + '\n'
                                  f'📟 Category id:     ' + settings['CATEGORY ID'])
            except:
                await ctx.respond(f'🛑ERROR! CATEGORY DOESNT EXIST!🛑')

@bot.slash_command(name = "change_role_1", description = "Change role 1 to manage the bot")
async def change_role_1(ctx , role_name_or_id):
        if not have_roles(ctx):
            await ctx.respond(f'🛑YOU DONT HAVE NECESSARY PERMISSIONS🛑')
            return
        for guild in bot.guilds:
           try:
              try:
                role_1 = discord.utils.get(guild.roles, id = int(role_name_or_id))
                await ctx.respond('Ok')
              except:
                role_1 = discord.utils.get(guild.roles, name = role_name_or_id)
                await ctx.respond('NO')
              settings['ADMIN ROLE 1'] = role_1.name
              await ctx.respond(f'✅ Role 1 was changed:\n'
                              f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                              f'📻 Role 1 name:     ' + role_1.name + '\n'
                              f'📟 Role 2 id:     ' + str(role_1.id))
           except:
              await ctx.respond(f'🛑ERROR! ROLE DOESNT EXIST!🛑')

@bot.slash_command(name = "change_role_2", description = "Change role 2 to manage the bot")
async def change_role_2(ctx , role_name_or_id):
        if not have_roles(ctx):
            await ctx.respond(f'🛑YOU DONT HAVE NECESSARY PERMISSIONS🛑')
            return
        for guild in bot.guilds:
           try:
              try:
                role_2 = discord.utils.get(guild.roles, id = int(role_name_or_id))
              except:
                role_2 = discord.utils.get(guild.roles, name = role_name_or_id)
              settings['ADMIN ROLE 2'] = role_2.name
              await ctx.respond(f'✅ Role 2 was changed:\n'
                              f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                              f'📻 Role 2 name:     ' + role_2.name + '\n'
                              f'📟 Role id:     ' + str(role_2.id))
           except:
              await ctx.respond(f'🛑ERROR! ROLE DOESNT EXIST!🛑')

@bot.slash_command(name = "change_need_roles" ,description = "Change count roles need to manage bot")
async def change_need_roles(ctx , need_roles):
        if not have_roles(ctx):
            await ctx.respond(f'🛑YOU DONT HAVE NECESSARY PERMISSIONS🛑')
            return
        if need_roles == '0':
            settings['NEED ROLES'] = '0'
            await ctx.respond(f'✅ SUCCESS ✅\n'
                              f'To list roles need to manage bot , use command \"roles_list\"')
        elif need_roles == '1':
            settings['NEED ROLES'] = '1'
            await ctx.respond(f'✅ SUCCESS ✅\n'
                              f'To list roles need to manage bot , use command \"/roles_list\"')
        elif need_roles == '2':
            settings['NEED ROLES'] = '2'
            await ctx.respond(f'✅ SUCCESS ✅\n'
                              f'To list roles need to manage bot , use command \"/roles_list\"')
        elif need_roles == 'any':
            settings['NEED ROLES'] = 'any'
            await ctx.respond(f'✅ SUCCESS ✅\n'
                              f'To list roles need to manage bot , use command \"/roles_list\"')
        else:
            await ctx.respond(f'🛑ERROR! INVALID ARGUMENT!🛑')

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
                def check(x,y,z):
                    return len(channel2.members) == 0
                await bot.wait_for('voice_state_update', check = check)
                await channel2.delete()

bot.run (settings['TOKEN'])