import discord
from discord.ext import commands
import random
import asyncio

bot = commands.Bot(command_prefix='/')
client = discord.Client()

@bot.command(name='ping')
async def ping(ctx):
    """
    Check the bot's latency and response time.
    """
    message = await ctx.send('Pong!')
    latency = bot.latency
    await message.edit(content=f'Pong! {latency * 1000} ms')

@bot.command(name='clear')
@commands.has_permissions(administrator=True)
async def clear(ctx, amount='5', member: discord.Member = None):
    if amount.lower() == 'all':
        if member is not None:
            await ctx.channel.purge(check=lambda msg: msg.author == member)
        else:
            await ctx.channel.purge()
    else:
        amount = int(amount)
        if member is not None:
            await ctx.channel.purge(limit=amount + 1, check=lambda msg: msg.author == member)
        else:
            await ctx.channel.purge(limit=amount + 1)

@bot.command(name='wp')
async def wp(ctx):
    """
    Assign the "wanttoplay" role to the user.
    Usage: /wp
    """
    role_name = 'wanttoplay'
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    
    if not role:
        role = await ctx.guild.create_role(name=role_name)
    
    await ctx.author.add_roles(role)
    await ctx.send(f'{ctx.author.mention}, you have been assigned the {role.mention} role.')

@bot.command(name='nw')
async def nw(ctx):
    """
    Remove the "wanttoplay" role from the user.
    Usage: /nw
    """
    role_name = 'wanttoplay'
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send(f'{ctx.author.mention}, the {role.mention} role has been removed from you.')
    else:
        print("Nothing to remove")

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

@bot.command()
async def math(ctx, *, equation):
    author = ctx.author
    
    try:
        result = eval(equation)
        await ctx.send(f'Equation from {author.mention}:\n{equation} = {result}')
    except Exception as e:
        await ctx.send(f'An error occurred while evaluating the equation from:{author.mention}:\n{str(e)}')

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
    
bot.run('')
