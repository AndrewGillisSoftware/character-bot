import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import fakeyou
from fakeyou import *
from utilities import *
from discord import FFmpegPCMAudio
import sys
from chatgpt import *

@dataclass
class Session:
    fy: FakeYou = None

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Hello! Character bot is ready!")
    session.fy = getFakeYou()

@bot.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Not in Voice channel")

@bot.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Disconnected")
    else:
        await ctx.send("Not in Voice channel")

# !say "Peter Griffin" "Joe is very stupid"
@bot.command(pass_context = True)
async def say(ctx, name, text):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        characterResponseRawWav = speak(session.fy, name, text)
        filename = str(random.randint(0, sys.maxsize)) + '.wav'
        saveBytesToFile(characterResponseRawWav, filename)
        if ctx.voice_client is None:
            voice = await channel.connect()
        else:
            voice = ctx.voice_client
            
        source = FFmpegPCMAudio(filename)
        player = voice.play(source)

    else:
        await ctx.send("Not in Voice channel")

# !ask "Peter Griffin" "Hows the Weather Today?"
@bot.command(pass_context = True)
async def ask(ctx, name, questionText):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        response = question(name, questionText)
        characterResponseRawWav = speak(session.fy, name, response)
        filename = str(random.randint(0, sys.maxsize)) + '.wav'
        saveBytesToFile(characterResponseRawWav, filename)
        if ctx.voice_client is None:
            voice = await channel.connect()
        else:
            voice = ctx.voice_client
            
        source = FFmpegPCMAudio(filename)
        player = voice.play(source)

    else:
        await ctx.send("Not in Voice channel")

config = getConfigYaml()
bot.run(config['discord_token'])
