import discord
from discord.ext import commands
from discord.ext import tasks
import websockets
import asyncio
import logging

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("PHIZZNIGHTLY_TOKEN")
OWNER = os.getenv("OWNER_ID")
PREFIX = os.getenv("PREFIX")
FORMAT = os.getenv("LOGFRMT")

logging.basicConfig(level=logging.INFO, format=FORMAT)


sock = None
chan = None
ws = None

bot = commands.Bot(command_prefix=PREFIX)



@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def here(ctx):
    global chanal
    if ctx.channel:
        chan = ctx.channel
    else:
        chan = ctx.author
    await chan.send(f'`Set relay channel to {str(chan)}`')


async def on_ready():
    logging.info("up")

async def on_message(message):
    print(chan)
    print(message.channel)
    print(message.channel == chan)
    if message.author == bot.user or message.channel != chan:
        return

    logging.info(message.content)
    await message.channel.send('here')
    await ws.send('app1 ' + message.content)

async def handler(uri):
    async with websockets.connect(uri) as wst:
        ws = wst
        await ws.send('bot')
        async for message in ws:
            await chan.send(message.content)

bot.add_listener(on_ready)
bot.add_listener(on_message)

bot.run(TOKEN)