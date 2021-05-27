import re
import discord
from discord import opus
from discord.ext import commands
from discord import Guild
import asyncio
import json
import numpy
from discord.ext.commands import Bot

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='A Movie'))


@bot.event
async def on_member_join(member):

    await member.send(
        'Hey, danke das du auf LCD gejoint bist. Wir hoffen du wirst eine gute Zeit haben. Schaue am besten am Anfang in den Chat [willkommen] und in den Chat [lcd-regeln]. Dort erhältst du weitere Infos.'
        '\nLiebe Grüße, dein LCD Team!')
    role = discord.utils.get(member.guild.roles, name='LCD')
    await member.add_roles(role)



ban_list = []
day_list = []
server_list = []
with open('BadWords.txt', 'r') as f:
    global badwords  # You want to be able to access this throughout the code
    words = f.read()
    badwords = words.split()


# Todo --------------------------------------------------------------lvl-sys------------------------------------------------------------
@bot.event
async def on_message(message):
    if not message.author.bot:
        msg = message.content
        with open('badWords.txt') as BadWords:
            if msg in BadWords.read():
                await message.delete()
        print('function load')
        #json wird geöffnet
        with open('level.json', 'r') as f:
            users = json.load(f)
            print('file load')
        #json wird behandelt
        channel = bot.get_channel(766744531479035905)

        await update_data(users, message.author, message.guild)
        await add_experience(users, message.author, 4, message.guild)
        await level_up(users, message.author, channel, message.guild, message)

        #json wird abgeschickt
        with open('level.json', 'w') as f:
            json.dump(users, f)
    await bot.process_commands(message)


async def update_data(users, user, server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 2
            users[str(server.id)][str(user.id)]['level'] = 1
            users[str(server.id)][str(user.id)]['coins'] = 0

    elif not str(user.id) in users[str(server.id)]:
        users[str(server.id)][str(user.id)] = {}
        users[str(server.id)][str(user.id)]['experience'] = 2
        users[str(server.id)][str(user.id)]['level'] = 1
        users[str(server.id)][str(user.id)]['coins'] = 0


async def add_experience(users, user, exp, server):
    users[str(user.guild.id)][str(user.id)]['experience'] += exp + 4


async def level_up(users, user, channel, server, message):
    experience = users[str(user.guild.id)][str(user.id)]['experience']
    lvl_start = users[str(user.guild.id)][str(user.id)]['level']
    lvl_end = int(experience ** (1 / 4))
    if str(user.guild.id) != '403649371352334352':
        if lvl_start < lvl_end:
            await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
            users[str(user.guild.id)][str(user.id)]['level'] = lvl_end
            await add_coins(users, message.author, message.channel, message.guild)

async def add_coins(users, user, channel ,server):
    lvl = users[str(user.guild.id)][str(user.id)]['level']
    coins = users[str(server.id)][str(user.id)]['coins']
    if lvl == 0:
        users[str(server.id)][str(user.id)]['coins'] = 0
    if lvl == 2:
        users[str(server.id)][str(user.id)]['coins'] = 20
    if lvl == 5:
        users[str(server.id)][str(user.id)]['coins'] = 50 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 10:
        users[str(server.id)][str(user.id)]['coins'] = 100 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 20:
        users[str(server.id)][str(user.id)]['coins'] = 150 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 30:
        users[str(server.id)][str(user.id)]['coins'] = 200 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 40:
        users[str(server.id)][str(user.id)]['coins'] = 250 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 50:
        users[str(server.id)][str(user.id)]['coins'] = 500 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 75:
        users[str(server.id)][str(user.id)]['coins'] = 500 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 100:
        users[str(server.id)][str(user.id)]['coins'] = 600 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 200:
        users[str(server.id)][str(user.id)]['coins'] = 600 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 300:
        users[str(server.id)][str(user.id)]['coins'] = 700 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 400:
        users[str(server.id)][str(user.id)]['coins'] = 800 + users[str(server.id)][str(user.id)]['coins']
    if lvl == 500:
        users[str(server.id)][str(user.id)]['coins'] = 1000 + users[str(server.id)][str(user.id)]['coins']
    print(coins)



@bot.command(aliases=['rank', 'lvl'])
async def level(ctx, member: discord.Member = None):
    if not member:
        user = ctx.message.author
        with open('level.json', 'r') as f:
            users = json.load(f)
        print(ctx.guild.id)
        serverid = ctx.guild.id
        lvl = users[str(ctx.guild.id)][str(user.id)]['level']
        exp = users[str(ctx.guild.id)][str(user.id)]['experience']
        coins = users[str(ctx.guild.id)][str(user.id)]['coins']
        embed = discord.Embed(title='Level {}'.format(lvl), description=f"{exp} XP ", color=discord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        with open('level.json', 'w') as f:
            json.dump(users, f)
    else:
        with open('level.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(member.id)]['level']
        exp = users[str(ctx.guild.id)][str(member.id)]['experience']
        coins = users[str(ctx.guild.id)][str(member.id)]['coins']
        embed = discord.Embed(title='Level {}'.format(lvl), description=f"{exp} XP", color=discord.Color.green())
        embed.set_author(name=member, icon_url=member.avatar_url)
        await ctx.send(embed=embed)
        with open('level.json', 'w') as f:
            json.dump(users, f)

# Todo -------------------------------------------------------------casino------------------------------------------------------------
@bot.command()
async def casino(ctx, amount: int = None, number: int = None):
    channel = bot.get_channel(766744531319783454)
    if channel == ctx.channel:
        random = numpy.random.randint(1,5)
        user = ctx.message.author
        with open('level.json', 'r') as f:
            users = json.load(f)
        print(ctx.guild.id)
        serverid = ctx.guild.id
        coins = users[str(ctx.guild.id)][str(user.id)]['coins']
        if number <= 5 and number > 0:
            if amount <= coins:
                if int(random) == int(number):
                    users[str(serverid)][str(user.id)]['coins'] = users[str(serverid)][str(user.id)]['coins'] + int(amount)
                    await ctx.send("Gewonnen! Du bekommst {} lcd Coins!".format(amount))
                else:
                    users[str(serverid)][str(user.id)]['coins'] = users[str(serverid)][str(user.id)]['coins'] - int(amount)
                    await ctx.send("Niete! Du verlierst {} lcd Coins!".format(amount))
            else:
                await ctx.send("du hast nicht genug Coins dafür, bitte gib eine andere Zahl ein")
        else:
            await ctx.send("bitte gebe eine zahl zwischen 1 und 5 an")
        with open('level.json', 'w') as f:
            json.dump(users, f)
# Todo -------------------------------------------------------------addcoins---------------------------------------------------------
@bot.command(aliases=['coinsadd'])
@commands.has_permissions(administrator=True)
async def addcoins(ctx, member: discord.Member = None, amount: int = None):
    if not member:
        user = ctx.message.author
        with open('level.json', 'r') as f:
            users = json.load(f)
        print(ctx.guild.id)
        serverid = ctx.guild.id
        coins = users[str(ctx.guild.id)][str(user.id)]['coins']
        users[str(serverid)][str(user.id)]['coins'] = users[str(serverid)][str(user.id)]['coins'] + int(amount)
        embed = discord.Embed(title='{} du hast'.format(member), description="{} lcd coins bekommen".format(amount), color=discord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        with open('level.json', 'w') as f:
            json.dump(users, f)
    else:
        user = member
        with open('level.json', 'r') as f:
            users = json.load(f)
        print(ctx.guild.id)
        serverid = ctx.guild.id
        coins = users[str(ctx.guild.id)][str(user.id)]['coins']
        users[str(serverid)][str(user.id)]['coins'] = users[str(serverid)][str(user.id)]['coins'] + int(amount)
        embed = discord.Embed(title='{} du hast'.format(member), description="{} lcd coins bekommen".format(amount), color=discord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        with open('level.json', 'w') as f:
            json.dump(users, f)
# Todo -------------------------------------------------------------removecoins------------------------------------------------------
@bot.command(aliases=['coinsremove'])
@commands.has_permissions(administrator=True)
async def removecoins(ctx, member: discord.Member = None, amount: int = None):
    if not member:
        user = ctx.message.author
        with open('level.json', 'r') as f:
            users = json.load(f)
        print(ctx.guild.id)
        serverid = ctx.guild.id
        coins = users[str(ctx.guild.id)][str(user.id)]['coins']
        users[str(serverid)][str(user.id)]['coins'] = users[str(serverid)][str(user.id)]['coins'] - int(amount)
        embed = discord.Embed(title='{} dir wurden'.format(member), description="{} lcd coins entfernt!".format(amount), color=discord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        with open('level.json', 'w') as f:
            json.dump(users, f)
    else:
        user = member
        with open('level.json', 'r') as f:
            users = json.load(f)
        print(ctx.guild.id)
        serverid = ctx.guild.id
        coins = users[str(ctx.guild.id)][str(user.id)]['coins']
        users[str(serverid)][str(user.id)]['coins'] = users[str(serverid)][str(user.id)]['coins'] - int(amount)
        embed = discord.Embed(title='{} dir wurden'.format(member), description="{} lcd coins entfernt!".format(amount), color=discord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        with open('level.json', 'w') as f:
            json.dump(users, f)
# Todo -------------------------------------------------------------buy---------------------------------------------------------------
@bot.command(aliases=['kauf', 'einkaufen'])
async def buy(ctx, thing: str = None):
    #print(thing)+
    user = ctx.message.author
    with open('level.json', 'r') as f:
        users = json.load(f)
    lvl = users[str(ctx.guild.id)][str(user.id)]['level']
    exp = users[str(ctx.guild.id)][str(user.id)]['experience']
    coins = users[str(ctx.guild.id)][str(user.id)]['coins']
    print("hello")
    if thing == "supreme" or thing == "Supreme":
        role = discord.utils.get(user.guild.roles, name='Supreme')
        if role in user.roles:

            await ctx.send("du hast den Supreme Rang schon!")

        else:

            if coins >= 1000:
                role = discord.utils.get(user.guild.roles, name='Supreme')
                await user.add_roles(role)
                serverid = ctx.guild.id
                users[str(serverid)][str(user.id)]['coins'] = users[str(serverid)][str(user.id)]['coins'] - 1000
                await ctx.send("du hast nun den Supreme Rang!")

            else:
                await ctx.send("du hast nicht genug Coins dafür!")
    with open('level.json', 'w') as f:
        json.dump(users, f)
    #embed = discord.Embed(title='Level {}'.format(lvl), description=f"{exp} XP ", color=discord.Color.green())
    #embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    #await ctx.send(embed=embed)



# Todo -------------------------------------------------------------coins--------------------------------------------------------------
@bot.command(aliases=['geld', 'money'])
async def coins(ctx, member: discord.Member = None):
    if not member:
        user = ctx.message.author
        with open('level.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(user.id)]['level']
        exp = users[str(ctx.guild.id)][str(user.id)]['experience']
        coins = users[str(ctx.guild.id)][str(user.id)]['coins']
        embed = discord.Embed(title='du hast', description=f"{coins} lcd coins", color=discord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        with open('level.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(member.id)]['level']
        exp = users[str(ctx.guild.id)][str(member.id)]['experience']
        coins = users[str(ctx.guild.id)][str(member.id)]['coins']
        #embed = discord.Embed(title='Level {}'.format(lvl), description=f"{exp} XP", color=discord.Color.green())
        embed = discord.Embed(title='{} hat'.format(member), description=f"{coins} lcd coins ", color=discord.Color.green())
        embed.set_author(name=member, icon_url=member.avatar_url)
        await ctx.send(embed=embed)
# Todo -------------------------------------------------------------clan---------------------------------------------------------------
@bot.command()
async def clan(ctx, thing: str = None, member: discord.Member = None, name: str = None):
    channel = bot.get_channel(825652826289864714)
    if channel == ctx.channel:
        author = ctx.message.author
        print(author)
        role = discord.utils.find(lambda r: r.name == "Supreme", ctx.message.guild.roles)
        if role in author.roles:
            if thing == "help" and member == None:
                embed = discord.Embed(title='this is the help',
                                      description='!clan create [creates your clan] \n !clan add {username} [adds people to yor clan] \n !clan remove {username} [removes people to your clan] \n !clan delete [deletes your server]\n\n for more help for other commands type !help')
                await ctx.send(embed=embed)
                #await ctx.send("this is the help\n !clan create [creates your clan] \n !clan add {username} [adds people to yor clan] \n !clan remove {username} [removes people to your clan] \n !clan delete [deletes your server]\n\n for more help for other commands type !help")
            if thing == "create" and member == None:
                cate = discord.utils.get(author.guild.categories, name="{}´s Clan".format(author.name))
                if not cate in author.guild.categories:
                    await ctx.send("Dein Clan wurde erstellt!\n Um deine Freunde hinzuzufügen gebe einfach !clan add {username} ein!")
                    guild = ctx.message.guild
                    author = ctx.message.author
                    await guild.create_role(name='{}-clanmember'.format(author.name))
                    category = await ctx.guild.create_category("{}´s Clan".format(author.name))
                    lcd = discord.utils.get(author.guild.roles, name='LCD')
                    clanmember = discord.utils.get(author.guild.roles, name='{}-clanmember'.format(author.name))

                    await category.set_permissions(author, read_messages=True, send_messages=True, connect=True, speak=True, create_instant_invite=True, manage_channels=True,stream=True,manage_messages=True,move_members=True,mute_members=True,use_voice_activation=True,manage_permissions=True)
                    await category.set_permissions(lcd, read_messages=False, send_messages=False, connect=False, speak=False,
                                                   create_instant_invite=False, manage_channels=False, stream=False,
                                                   manage_messages=False, move_members=False, mute_members=False,
                                                   use_voice_activation=False, manage_permissions=False)

                    await category.set_permissions(clanmember, read_messages=True, send_messages=True, connect=True, speak=True,
                                                   create_instant_invite=False, manage_channels=False, stream=True,
                                                   manage_messages=False, move_members=False, mute_members=False,
                                                   use_voice_activation=False, manage_permissions=False)
                    await guild.create_text_channel('clan-text', category=category)
                    await guild.create_voice_channel('Clan Talk 1', category=category)
                else:
                    await ctx.send("es gibt schon einee Kategorie namens:{}´s Clan".format(author.name))
            if thing == "add":
                if member == None:
                    await ctx.send("Du musst einen Namen dazuschreiben!")
                else:
                    author = ctx.message.author
                    clanmemberjoin = '{}-clanmember'.format(author.name)
                    role = discord.utils.find(lambda r: r.name == clanmemberjoin, ctx.message.guild.roles)

                    if not role in member.roles:

                        clanmember = discord.utils.get(author.guild.roles, name='{}-clanmember'.format(author.name))
                        await member.add_roles(clanmember)
                        await ctx.send("{} ist nun in deinem Clan!".format(member))

                    else:

                        await ctx.send("{} ist schon in deinem Clan!".format(member))
            if thing == "remove":

                if member == None:
                    await ctx.send("Du musst einen Namen dazuschreiben!")
                else:
                    await ctx.send("Dein Clan wurde gelöscht!")
                    author = ctx.message.author
                    clanmemberjoin = '{}-clanmember'.format(author.name)
                    role = discord.utils.find(lambda r: r.name == clanmemberjoin, ctx.message.guild.roles)

                    if role in member.roles:

                        clanmember = discord.utils.get(author.guild.roles, name='{}-clanmember'.format(author.name))
                        await member.remove_roles(clanmember)
                        await ctx.send("{} ist nun nicht mehr in deinem Clan!".format(member))

                    else:

                        await ctx.send("{} ist nicht in deinem Clan!".format(member))

            if thing == "delete":
                cate = discord.utils.get(author.guild.categories, name="{}´s Clan".format(author.name))
                if cate in author.guild.categories:
                    author = ctx.message.author
                    server = author.guild.roles
                    clanmember = discord.utils.get(author.guild.roles, name='{}-clanmember'.format(author.name))
                    await clanmember.delete()

                    cate = discord.utils.get(author.guild.categories, name="{}´s Clan".format(author.name))
                    for channel in cate.voice_channels:
                        await channel.delete()
                    for channel in cate.text_channels:
                        await channel.delete()
                    await cate.delete()

                else:
                    await ctx.send("es gibt keine Kategorie namens: {}´s Clan".format(author.name))
        else:
            await ctx.send("Du kannst nicht einen clan Gründen!")

# Todo -------------------------------------------------------------überweisung------------------------------------------------------
@bot.command()
async def transfer(ctx, user: discord.Member = None, amount: int = None):
    author = ctx.message.author
    role = discord.utils.find(lambda r: r.name == "Supreme", ctx.message.guild.roles)

    if role in author.roles:

        if user == None or amount == None:
            await ctx.send("Du musst einen Namen und einen Betrag angeben!")
        with open('level.json', 'r') as f:
            users = json.load(f)
            coins = users[str(ctx.guild.id)][str(author.id)]['coins']
        if coins >= amount:

            users[str(ctx.guild.id)][str(author.id)]['coins'] = users[str(ctx.guild.id)][str(author.id)]['coins'] - int(amount)
            print(users[str(ctx.guild.id)][str(author.id)]['coins'] - int(amount))
            print(users[str(ctx.guild.id)][str(author.id)]['coins'])
            users[str(ctx.guild.id)][str(user.id)]['coins'] = users[str(ctx.guild.id)][str(user.id)]['coins'] + int(amount)
            print(amount)
            await ctx.send(f"es wurden {amount} an {user} übertragen!")
            with open('level.json', 'w') as f:
                json.dump(users, f)
        else:
            await ctx.send("du hast zu wenig Coins!")
    else:
        await ctx.send("Du hast keine berechtigung dazu!")

# Todo -------------------------------------------------------------userinfo-----------------------------------------------------------
@bot.command()
# !userinfo DobbCraft
async def userinfo(ctx, *, user: discord.Member = None):
    try:
        if user == None:
            # !userinfo
            user = ctx.message.author
            serverid = ctx.guild.id
            with open('level.json', 'r') as f:
                users = json.load(f)
            joined_at = user.joined_at.strftime("%b %d, %Y")
            created_at = user.created_at.strftime("%b %d, %Y")
            coins = users[str(ctx.guild.id)][str(user.id)]['coins']
            exp = users[str(ctx.guild.id)][str(user.id)]['experience']
            level = users[str(ctx.guild.id)][str(user.id)]['level']
            embed = discord.Embed(title='Userinfo für {}'.format(user),
                                  description='Dies ist eine Userinfo für den User {}'.format(user))
            embed.add_field(name="Beigetreten?", value=joined_at, inline=False)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Discord heruntergeladen?", value=created_at, inline=False)
            embed.add_field(name="Nickname", value=user.nick, inline=False)
            embed.add_field(name="top rolle", value=user.top_role, inline=False)
            embed.add_field(name="Coins",value=coins, inline=False)
            embed.add_field(name="XP",value=exp, inline=False)
            embed.add_field(name="Level", value=exp, inline=False)
            await ctx.send(embed=embed)

        else:
            # !userinfo Name
            if ctx.message.author.top_role.permissions.administrator:
                serverid = ctx.guild.id
                with open('level.json', 'r') as f:
                    users = json.load(f)
                joined_at = user.joined_at.strftime("%b %d, %Y")
                created_at = user.created_at.strftime("%b %d, %Y")
                coins = users[str(ctx.guild.id)][str(user.id)]['coins']
                exp = users[str(ctx.guild.id)][str(user.id)]['experience']
                level = users[str(ctx.guild.id)][str(user.id)]['level']
                embed = discord.Embed(title='Userinfo für {}'.format(user),
                                      description='Dies ist eine Userinfo für den User {}'.format(user))
                embed.add_field(name="Beigetreten?", value=joined_at, inline=False)
                embed.set_thumbnail(url=user.avatar_url)
                embed.add_field(name="Discord heruntergeladen?", value=created_at, inline=False)
                embed.add_field(name="Nickname", value=user.nick, inline=False)
                embed.add_field(name="top rolle", value=user.top_role, inline=False)
                embed.add_field(name="Coins", value=coins, inline=False)
                embed.add_field(name="XP", value=exp, inline=False)
                embed.add_field(name="Level", value=exp, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send('du hast keine Berechtigungen dafür')
    except:
        pass

# Todo -------------------------------------------------------------clear---------------------------------------------------------------
@bot.command()
async def clear(ctx, limit: int = None):
    print(limit)
    if limit == None:
        await ctx.channel.purge(limit=2)
    else:
        passed = 0
        failed = 0
        await ctx.channel.purge(limit=limit + 1)
        # async for msg in ctx.message.channel.history(limit=limit):
        # if msg.author.id == bot.user.id:
        # try:

        # passed += 1
        # except:
        # failed += 1
        # print(f"[Complete] Removed {passed} messages with {failed} fails")

    if limit == None:

        await ctx.send(f'Ich hab eine Nachricht gelöscht')

    else:
        limit = str(limit)
        await ctx.send(f'Ich habe: ' + limit + ' Nachrichten gelöscht!')


#@bot.command()
#async def hilfe(ctx):
    #role = discord.utils.find(lambda r: r.name == 'Member', ctx.message.server.roles)
    print(ctx.message.author.roles)
    # print(role)
    #if role in ctx.message.author.roles:
        #print('hello')


# Todo -------------------------------------------------------------clearall------------------------------------------------------------
@bot.command()
async def clearall(ctx, amount=1000000):
    if commands.has_permissions(manage_messages=True):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Ich habe ein paar Nachrichten gelöscht!')
        return


@bot.command()
async def servus(ctx):
    await ctx.send('MOIN MEISTER')

# Todo -------------------------------------------------------------youtube------------------------------------------------------------
@bot.command()
async def youtube(ctx):
    embed = discord.Embed(title='Youtube',
                          description='----------------------------------------------------------------------------------------------')
    embed.add_field(name='Lumale008', value="https://www.youtube.com/channel/UCXZKOmenDvZOrt5LOUZT2Gw \n")
    embed.add_field(name="Chandrix", value='https://www.youtube.com/channel/UCftuH9u81GgHrG8Q7bvMe_A \n')
    embed.add_field(name="DobbCraft", value="https://www.youtube.com/channel/UCjaF2xTKNPd4sBr490yBT4Q \n\n")

    embed.add_field(name="Nicksonice",
                    value="https://www.youtube.com/channel/UCbEp_jIN2iIv7WlNhWSwiNg \n \n Wir würden uns alle über ein Abbo und ein Like freuen")
    # embed.add_field(name="Lumale008:LUMALE008SHEAD: :\n"
    # "https://www.youtube.com/channel/UCXZKOmenDvZOrt5LOUZT2Gw \n"
    # "Chandrix:CHANDRIXSHEAD: : \n"
    # "https://www.youtube.com/channel/UCftuH9u81GgHrG8Q7bvMe_A \n"
    # "DobbCraft:DOBBCRAFTSHEAD: : \n"
    # "https://www.youtube.com/channel/UCjaF2xTKNPd4sBr490yBT4Q \n"
    # "\n"
    ##"Nicksonice:NICKSONICESHEAD: : \n"
    # "https://www.youtube.com/channel/UCbEp_jIN2iIv7WlNhWSwiNg \n"
    # "\n"
    # "Wir würden uns alle über ein Abbo und ein Like freuen.")
    await ctx.send(embed=embed)


@bot.command()
async def DobbCraft(ctx):
    await ctx.send('Hi, ich bin Dobbcraft (oder Oskar) \n'
                   'Ich bin einer der Owner hier. Kein wunder oder? Ich meine sonst würde es diesen Befehl gar nicht '
                   'geben :laughing:. Aber jetzt mal Spaß bei Seite. Was ihr über mich wissen müsst ist: Diesen Bot '
                   'habe ich fast allein gecodet, ich arbeite sehr gerne mit Luca und Chandri an Projekten wie zum '
                   'Beispiel der LCD Website :LCDwebsite:, Minecraft Projekten oder an diesem Bot hier. \n '
                   'PS: Mein YT:https://www.youtube.com/channel/UCjaF2xTKNPd4sBr490yBT4Q \n'
                   'Twitch: https://www.twitch.tv/dobbcraft  ')


@bot.command()
async def Chandrix(ctx):
    await ctx.send('Moin Moin. Chandrix hier!(egt heiß Ich Chandri). \n'
                   'Ich bin auch einer der freshen Owner hier.Ich habe euch auch ein bischen was, was ich euch über '
                   'mich erzählen kann. Ich liebe es mit Oskar und Luca Sachen an unserem Discord zu Verbessern. '
                   'Außerdem Checkt mein Youtube aus:sunglasses:.  \n '
                   'https://www.youtube.com/channel/UCftuH9u81GgHrG8Q7bvMe_A')


@bot.command()
async def Lumale008(ctx):
    await ctx.send(
        'Hallo meine Lieben Freunde. Schön das du meinen Command benützt hast. Dann erzähl ich dir mal was von mir ('
        'Lumale008 oder Luca) :LUMALE008HEAD:. \n '
        'Ich bin natürlich wie Chandrix und Dobbcraft auch ein Owner. Ich bin der Dude, der z.B die ganzen Texte von '
        'diesem Bot verfasst hat. Checkt mein Youtube ab!!!  \n '
        'https://www.youtube.com/channel/UCXZKOmenDvZOrt5LOUZT2Gw')

# Todo -------------------------------------------------------------ban----------------------------------------------------------------
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member = None, duration: int = None, time: str = None):
    if time == "s":
        await ctx.guild.ban(user)  #
        embed = discord.Embed(title='{} wurde für'.format(user) + time + " sekunden Gebannt!",
                              description='.')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
        await asyncio.sleep(duration)
        await ctx.guild.unban(user)
    elif time == "m":
        await ctx.guild.ban(user)
        embed = discord.Embed(title='{} wurde für'.format(user) + time + " Minuten Gebannt!",
                              description='.')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
        await asyncio.sleep(duration * 60)
        await ctx.guild.unban(user)
    elif time == "h":
        await ctx.guild.ban(user)
        embed = discord.Embed(title='{} wurde für'.format(user) + time + " Stunden Gebannt!",
                              description='.')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
        await asyncio.sleep(duration * 3600)
        await ctx.guild.unban(user)
    elif time == "d":
        await ctx.guild.ban(user)
        embed = discord.Embed(title='{} wurde für'.format(user) + time + " Tage Gebannt!",
                              description='.')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
        await asyncio.sleep(duration * 86400)
        await ctx.guild.unban(user)
    elif time == "-":
        await ctx.guild.ban(user)
        embed = discord.Embed(title='{} wurde für keine bestimmte Zeit gebannt!'.format(user),
                              description='.')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
    elif time == None:
        embed = discord.Embed(title='Um {} zu bannen brauchen wir eine Zeit!'.format(user),
                              description='s = Sekunden \n m = Minuten \n h = Stunden \n d = Tage \n - = kein limit ')
        await ctx.send(embed=embed)
        # await ctx.send('wir brauchen eine Zeit zum Bannen \n s = Sekunden \n m = Minuten \n h = Stunden \n d = Tage \n - = kein limit ')
    # await ctx.send("du hast keine Berechtigungen!")

# Todo -------------------------------------------------------------kick----------------------------------------------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member = None):
    if not user == None:
        await ctx.guild.kick(user)
        embed = discord.Embed(title='{} wurde gekickt!'.format(user),
                              description='.')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("wir brauchen einen Name")

        # await ctx.send('wir brauchen eine Zeit zum Bannen \n s = Sekunden \n m = Minuten \n h = Stunden \n d = Tage \n - = kein limit ')
        # await ctx.send("du hast keine Berechtigungen!")

# Todo -------------------------------------------------------------mute---------------------------------------------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def tmute(ctx, user: discord.Member = None):
    if not user == None:
        role = discord.utils.get(user.guild.roles, name='talk-mute')
        await user.add_roles(role)
        embed = discord.Embed(title='{} wurde talk-gemutet!'.format(user),
                              description='.')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("wir brauchen einen Name")
@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, user: discord.Member = None):
    if not user == None:
        mute1 = discord.utils.get(user.guild.roles, name='talk-mute')
        await user.remove_roles(mute1)

        mute2 = discord.utils.get(user.guild.roles, name='chat-Mute')
        await user.remove_roles(mute2)
        embed = discord.Embed(title='{} wurde unmutet!'.format(user),
                              description='.')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("wir brauchen einen Name")

@bot.command()
@commands.has_permissions(kick_members=True)
async def cmute(ctx, user: discord.Member = None):
    if not user == None:
        role = discord.utils.get(user.guild.roles, name='chat-Mute')
        await user.add_roles(role)
        embed = discord.Embed(title='{} wurde chat-gemutet!'.format(user),
                              description='.')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("wir brauchen einen Name")



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MemberNotFound):
        await ctx.send("Spieler ist nicht auf dem Server")
    elif isinstance(error, discord.errors.NotFound):
        pass
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Du hast keine Berechtigung dazu")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='A Movie'))
    print('Wir sind eingeloggt als User {}'.format(bot.user.name))
    # await  bot.change_presence(status=discord.Status.idle, activity=discord.Game('https://discord.gg/pcnG6BYq3R'))
    bot.loop.create_task(status_task())

    # if re.compile('|'.join(f_contents), re.IGNORECASE).search(message.content):
    # await message.delete()


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game('LCD BOT!'))
        await asyncio.sleep(3)
        await bot.change_presence(activity=discord.Game('https://lcd-website.webador.de/'))
        await asyncio.sleep(3)
        await bot.change_presence(activity=discord.Game('https://discord.gg/pcnG6BYq3R'))
        await asyncio.sleep(3)


bot.run('ODIxNDM1NzExODMxODAxODU2.YFDrnw.la8G5wac2NYpR5YX9EnimbGo5cg')
