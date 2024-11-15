import discord
import requests
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix='.', case_insensitive=True)

@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms is your ping ')

@client.event
async def on_ready():
    await client.tree.sync()
    print(f'We have logged in as {client.user}')
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name="who? TAO"))

url = 'https://api.waifu.im/search'

@client.hybrid_command()
async def waifu(ctx):
    waifu_params = {'included_tags': ['waifu']}
    waifu_response = requests.get(url, params=waifu_params)
    if waifu_response.status_code == 200:
       waifu_image = waifu_response.json()['images'][0]['url']
    else:
       await ctx.send('Sorry, I couldn\'t find the waifu!')
    await ctx.send(waifu_image)

@client.hybrid_command()
async def hentai(ctx):
    if ctx.channel.is_nsfw():
        hentai_params = {'included_tags': ['hentai', 'ero']}
        hentai_response = requests.get(url, params=hentai_params)
        if hentai_response.status_code == 200:
            hentai_image = hentai_response.json()['images'][0]['url']
        else:
            await ctx.send('Sorry, I couldn\'t find the hentai!')
        await ctx.send(hentai_image)
    else:
        await ctx.send('this channel ain\'t nsfw enough for the both of us')

client.run('Bot Token :)')
