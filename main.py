import os
import json
import discord
from discord.ext import commands

with open("config.json", "r") as file:
    config = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(config["prefix"], intents=intents, help_command=DefaultHelpCommand())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

#automod

@bot.command()
async def rules(ctx):
    rules = [
    "Rule 1: Be polite and respect other members.",
    "Rule 2: Do not post inappropriate content, spam or advertising.",
    "Rule 3: Follow the instructions of the server administration.",
    "Rule 4: No blasphemy",
    "Rule 5: No Dos/Ddos",
    "Rule 6: No adult content",
    "Rule 7: No swearing",
    "Rule 8: You can't tag a developer",
    "Rule 9: Inappropriate chat is requested",
    "Rule 10: Discussion of politics is forbidden"
    ]
    embed = discord.Embed(title="Server Rules", color=discord.Color.blue())
    for rule in rules:
        embed.add_field(name="\u200b", value=rule, inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if contains_prohibited_words(message.content):
        await message.delete()

    await bot.process_commands(message)


def contains_prohibited_words(content):

    prohibited_words = ['гитлер', 'Гитлер', 'дурак', "Дурак", "Идиот", "идиот", "тупой", "Тупой", "мразь", "Мразь", 'Hitler', 'Hitler', 'Fool', "Fool", "Idiot", "Idiot", "Stupid", "Dumb", "Scum", "Scum"]

    for word in prohibited_words:
        if word in content:
            return True

    return False

#auto server generation

@bot.command()
@commands.has_permissions(administrator=True)
async def create(ctx):
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }

    moderators_category = await guild.create_category_channel('moderators')
    await guild.create_text_channel('moderators', category=moderators_category, overwrites=overwrites)
    await guild.create_text_channel('chat staff', category=moderators_category, overwrites=overwrites)

    communication_category = await guild.create_category_channel('rules')
    rules_channel = await guild.create_text_channel('rules', category=communication_category)
    await rules_channel.set_permissions(guild.default_role, read_messages=True)

    communication_category = await guild.create_category_channel('communication')
    await guild.create_text_channel('general 1', category=communication_category)
    await guild.create_text_channel('general 2', category=communication_category)

    learn_category = await guild.create_category_channel('learn')
    learn_overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    await guild.create_text_channel('homework', category=learn_category, overwrites=learn_overwrites)
    await guild.create_text_channel('science', category=learn_category, overwrites=learn_overwrites)
    await guild.create_text_channel('tech-code', category=learn_category, overwrites=learn_overwrites)

    gaming_category = await guild.create_category_channel('gaming')
    gaming_overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    await guild.create_text_channel('workspace', category=gaming_category, overwrites=gaming_overwrites)
    await guild.create_text_channel('gaming', category=gaming_category, overwrites=gaming_overwrites)
    await guild.create_text_channel('pc-build', category=gaming_category, overwrites=gaming_overwrites)

    mini_games_category = await guild.create_category_channel('mini-games')
    mini_games_overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    await guild.create_text_channel('village', category=mini_games_category, overwrites=mini_games_overwrites)
    await guild.create_text_channel('casino', category=mini_games_category, overwrites=mini_games_overwrites)
    await guild.create_text_channel('would-you-rather', category=mini_games_category, overwrites=mini_games_overwrites)
    await guild.create_text_channel('rock-paper-scissors', category=mini_games_category, overwrites=mini_games_overwrites)

#want to play

@bot.command(name='wp')
async def wp(ctx):
    role_name = 'wanttoplay'
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    
    if not role:
        role = await ctx.guild.create_role(name=role_name)
    
    await ctx.author.add_roles(role)
    await ctx.send(f'{ctx.author.mention}, you have been assigned the {role.mention} role.')

@bot.command(name='nw')
async def nw(ctx):

    role_name = 'wanttoplay'
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send(f'{ctx.author.mention}, the {role.mention} role has been removed from you.')
    else:
        print("Nothing to remove")
    
#about

@bot.command()
async def about(ctx):
    commands_info = {'/marketplace': 'Displays a list of items available for purchase in the store.',
                    '/join': 'Joins you to the game, creating a player profile.',
                    '/buy <item> [quantity]': 'Buys the specified quantity of items from the store.',
                    '/village': 'Shows information about your village, including level, number of houses, population, food consumption, and reputation.',
                    '/upgrade': 'Upgrades your village if you have accumulated enough population.',
                    '/buy_house [quantity]': 'Buys the specified quantity of houses, increasing the population in your village.',
                    '/sell <item> [quantity]': 'Sells the specified quantity of items from your inventory.',
                    '/ban @name':'Only for moderators',
                    '/delete @name' :'Only for moderators',
                    '/mute @name' :'Only for moderators',
                    '/wyr': 'Would you rather game',
                    '/casino': 'Play to casino',
                    '/rps [stone or scissors or papper]': 'Stone, Scissors, Papper',
                    '/rules': 'List of server rules'
    }

    # Ваш код для отправки информации о командах
    # Пример: отправка в канал, из которого была вызвана команда
    response = ">>> ** Available commands:\n\n"
    for command, description in commands_info.items():
        response += f"{command}: {description}\n"

    await ctx.send(response)

#ping

@bot.command(name='ping')
async def ping(ctx):
    message = await ctx.send('Pong!')
    latency = bot.latency
    await message.edit(content=f'Pong! {latency * 1000} ms')

#clear

@bot.command(name='clear')
@commands.has_permissions(administrator=True)
async def clear(ctx, amount='5'):

    if amount.lower() == 'all':
        await ctx.channel.purge()
    else:
        amount = int(amount)
        await ctx.channel.purge(limit=amount + 1)

#raffle

@bot.command(name='raffle')
async def raffle(ctx, *, prizes):
    participants = ctx.channel.members
    winners = random.sample(participants, 3)
    await ctx.send(f'The winners of the raffle for {prizes} are: {", ".join(winner.mention for winner in winners)}!')

#reputation

reputation = {}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!rep+'):
        user_id = str(message.author.id)
        if user_id not in reputation:
            reputation[user_id] = 0
        reputation[user_id] += 1
        await message.channel.send(f'{message.author.mention}, your reputation is increased. Current reputation: {reputation[user_id]}')
        
        if reputation[user_id] >= 20:
            role = discord.utils.get(message.guild.roles, name='Popular')
            if role is None:
                role = await message.guild.create_role(name='Popular')
            await message.author.add_roles(role)

    if message.content.startswith('!rep-'):
        user_id = str(message.author.id)
        if user_id not in reputation:
            reputation[user_id] = 0
        reputation[user_id] -= 1
        await message.channel.send(f'{message.author.mention}, your reputation is down. Current reputation: {reputation[user_id]}')
        
        if reputation[user_id] <= -20:
            await message.author.kick(reason='Low reputation')

    await bot.process_commands(message)

@bot.command()
async def get_reputation(ctx, member: discord.Member = None):
    member = member or ctx.author
    user_id = str(member.id)
    if user_id in reputation:
        await ctx.send(f'Member reputation {member.mention}: {reputation[user_id]}')
    else:
        await ctx.send(f'Member reputation {member.mention} not found.')

async def update_status():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            member_count = guild.member_count
            guild_name = guild.name
            guild_description = f"{guild_name} ({member_count} members)"
            await bot.change_presence(activity=discord.Game(name="VS Code"), status=discord.Status.online)
            await asyncio.sleep(600)

#moderation command

@bot.command(name='set_roles')
@commands.has_permissions(administrator=True)
async def set_roles(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f'{user.mention} was given the {role.mention} role.')

@bot.command(name='remove_role')
@commands.has_permissions(administrator=True)
async def remove_role(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f'{user.mention} lost the {role.mention} role.')

@bot.command(name='raffle')
async def raffle(ctx, *, prizes):
    participants = ctx.channel.members
    winners = random.sample(participants, 3)
    await ctx.send(f'The winners of the raffle for {prizes} are: {", ".join(winner.mention for winner in winners)}!')

@bot.command(name='mute')
@commands.has_role('Moderator')
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.add_roles(role)
    await ctx.send(f'{member.mention} has been muted for 24 hours.')
    await asyncio.sleep(86400)
    await member.remove_roles(role)
    await ctx.send(f'{member.mention} has been unmuted.')

@bot.command(name='delete')
@commands.has_role('Moderator')
async def delete(ctx, member: discord.Member):
    await member.kick(reason='Deleted by moderator')
    await ctx.send(f'{member.mention} has been kicked.')

@bot.command(name="ban")
@commands.has_role('Moderator')
async def ban(ctx, member: discord.Member):
    await member.ban(reason='Banned by moderator')
    await ctx.send(f'{member.mention} has been banned.')

@bot.command(name='info')
async def info(ctx):
    embed = discord.Embed(title='Bot Commands and Functionality', color=discord.Color.blue())
    embed.add_field(name='ping', value='Checks the bot\'s latency. Usage: /ping', inline=False)
    embed.add_field(name='clear', value='Clears a specified number of messages in the channel. Usage: /clear [amount]', inline=False)
    embed.add_field(name='wp', value='Assigns the "wanttoplay" role to the user. Usage: /wp', inline=False)
    embed.add_field(name='nw', value='Removes the "wanttoplay" role from the user. Usage: /nw', inline=False)
    embed.add_field(name='set_roles', value='Assigns a role to a user. Usage: /set_roles [user] [role]', inline=False)
    embed.add_field(name='remove_role', value='Removes a role from a user. Usage: /remove_role [user] [role]', inline=False)
    embed.add_field(name='raffle', value='Performs a raffle and selects winners from channel participants. Usage: /raffle [prizes]', inline=False)
    embed.add_field(name='tr', value='Translates the provided text. Usage: /tr [text]', inline=False)
    embed.add_field(name='mute', value='Mutes a member for 24 hours. Usage: /mute [member]', inline=False)
    embed.add_field(name='delete', value='Kicks a member from the server. Usage: /delete [member]', inline=False)
    embed.add_field(name='ban', value='Bans a member from the server. Usage: /ban [member]', inline=False)
    embed.add_field(name='!rep+', value='Reputation +', inline=False)
    embed.add_field(name='!rep-', value='Reputation -', inline=False)
    await ctx.send(embed=embed)
    
bot.run(config["token"])
