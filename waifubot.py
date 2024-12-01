#importing all the modules
import discord
import requests
from discord.ext import commands
import google.generativeai as genai
import keys

#configuring gemini api
gemini_key = keys.gemini
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")

#configuring discord intents
intents = discord.Intents.all()
intents.message_content = True

#creating client
client = commands.Bot(intents=intents, command_prefix='.', case_insensitive=True)

#ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms is your ping ')

#making sure it has turned on
#changing it's status
@client.event
async def on_ready():
    await client.tree.sync()
    print(f'We have logged in as {client.user}')
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name="who? TAO"))

#url to get waifu.im's api to work
url = 'https://api.waifu.im/search'

#command to get image of random anime character
@client.hybrid_command()
async def waifu(ctx):
    waifu_params = {'included_tags': ['waifu']}
    waifu_response = requests.get(url, params=waifu_params)
    if waifu_response.status_code == 200:
       waifu_image = waifu_response.json()['images'][0]['url']
    else:
       await ctx.send('Sorry, I couldn\'t find the waifu!')
    await ctx.send(waifu_image)

#command to get random hentai
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

#talking to hu tao
#listens for the phrase "hu tao" then replies using gemini
@client.listen('on_message')
async def hutaotalk(message):
    if 'hu tao' in message.content:
        reply_content = model.generate_content(f"respond to this as if you were hu tao from the game genshin impact BUT KEEP IT SHORTER THAN 50 WORDS: {message.content}")
        await message.channel.send(reply_content.text)

#actually running the discord bot using the key
client.run(keys.discord)
