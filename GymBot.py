#Gymbot.py
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
        elif guild.name != GUILD:
            print(f'{bot.user} is being dmed')

@bot.command()
async def test(ctx):
    await ctx.send("command evoked")
@bot.command()
async def moo(ctx):
    await ctx.send("http://imgur.com/gallery/YiMUiop")     
# @bot.command()
# async def sendpr(ctx):
#     await ctx.

    #command template where the text is formatted as an embed. Will most likely use this format for most of the bots output
@bot.command()
async def embed(ctx):
    embed=discord.Embed(
    title="Text Formatting",
        #url="url",
        description="Here are some ways to format text",
        color=discord.Color.blue())
    #embed.set_author(name="Bot", url="url", icon_url="urlimage")
    #embed.set_author(name=ctx.author.display_name, url="url", icon_url=ctx.author.avatar_url)
    #embed.set_thumbnail(url="{urlimage}")
    embed.add_field(name="*Italics*", value="Surround your text in asterisks ()", inline=False)
    embed.add_field(name="**Bold**", value="Surround your text in double asterisks ()", inline=False)
    embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
    embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
    embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
    embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
    embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
    embed.set_footer(text="Foot")
    await ctx.send(embed=embed)
#@bot.command()
bot.run(TOKEN)
