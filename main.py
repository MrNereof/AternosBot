from Aternos import AternosAPI
from discord.ext import commands, tasks
import discord

headers_cookie = 'ATERNOS HEADERS'
TOKEN = 'ATERNOS TOKEN'
server = AternosAPI(headers_cookie, TOKEN)

DISCORD_TOKEN = 'DISCORD TOKEN'
bot = commands.Bot(command_prefix='a!', help_command=None)
bot.remove_command('help')

@bot.event
async def on_ready():
    updateStatus.start()
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
@bot.command()
async def help(ctx):
    helptext = ''
    for command in bot.commands:
        helptext+=f'{command}\n'
    embed=discord.Embed(title="Command list", description=helptext, color=0x00bfff)
    await ctx.send(embed=embed)
    
@bot.command()
async def start(ctx):
    result, position = server.StartServer()
    if result == True:
        description = ''
        if position != None:
            description = f'Queue pos: {position}.'
            confirmQueue.start()
        embed=discord.Embed(title="Success", description=description, color=0x00bfff)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Error", description='Server already started.', color=0x00bfff)
        await ctx.send(embed=embed)
    
@bot.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    result = server.StopServer()
    if result == True:
        embed=discord.Embed(title="Success", color=0x00bfff)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Error", description='Server already offline.', color=0x00bfff)
        await ctx.send(embed=embed)
    
@bot.command()
@commands.has_permissions(administrator=True)
async def restart(ctx):
    result = server.RestartServer()
    embed=discord.Embed(title="Success", color=0x00bfff)
    await ctx.send(embed=embed)
    
@bot.command()
async def ip(ctx):
    ip, port, dynip = server.GetIP()
    description = f'**IP**: {ip}\n**Port**: {port}'
    if dynip != None:
        description += f'\n**DynIP**: {dynip}'
    embed=discord.Embed(title="Server address", description=description, color=0x00bfff)
    await ctx.send(embed=embed)

@bot.command()
async def status(ctx):
    status = server.GetStatus()
    embed=discord.Embed(title="Server status", description=status, color=0x00bfff)
    await ctx.send(embed=embed)
    
@bot.command()
@commands.has_permissions(administrator=True)
async def adduser(ctx, *, name):
    result = server.addWhitelist(name)
    embed=discord.Embed(title="Succes", color=0x00bfff)
    await ctx.send(embed=embed)
    
@tasks.loop(seconds=30.0)
async def confirmQueue():
    confirm = server.confirmQueue()
    if confirm == True:
        confirmQueue.cancel()
    
@tasks.loop(seconds=15.0)
async def updateStatus():
    status = server.GetStatus()
    game = discord.Game(status)
    await bot.change_presence(activity=game)
    
bot.run(DISCORD_TOKEN)
