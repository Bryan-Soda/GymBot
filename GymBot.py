# Gymbot.py
import os
import discord
import random
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default() 
intents.messages = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            print(
                f'{bot.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )
@bot.command()
async def test(ctx):
    await ctx.send("command evoked :3")

bot.run(TOKEN)
