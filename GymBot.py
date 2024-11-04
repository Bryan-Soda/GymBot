#Gymbot.py
import os
import discord
import random
import sqlite3
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands

load_dotenv()
#sqlite database setup
database = sqlite3.connect('lifts.db')
cursor = database.cursor()
database.execute("CREATE TABLE IF NOT EXISTS lifts(user STRING, is_squat INT, is_bench INT, is_deadlift INT, pr INT)")

class Leaderboard:
    def __init__(self):
        self.people = []

    def update(self, members):
        self.people.clear()
        self.people.extend(members)

async def update_channel():
    channel = bot.get_channel(LEADERBAORD_CHANNEL_ID)
    await channel.purge()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
#These IDs will correspond to your own channel IDs
BOT_CHANNEL_ID = #ChannelIDNumber
LEADERBAORD_CHANNEL_ID = #ChannelIDNumber

intents = discord.Intents.default() 
intents.messages = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
board = Leaderboard()
users = []

@bot.event

async def on_ready():
    botChannel = bot.get_channel(BOT_CHANNEL_ID)
    LeaderboardChannel = bot.get_channel(LEADERBAORD_CHANNEL_ID)
    for guild in bot.guilds:
        if guild.name == GUILD:
            print(
                f'{bot.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )
        users.clear()
        for member in guild.members:
            users.append(member.name)
    #Bot shows announces it is online
    if botChannel:
        await botChannel.send("I AM ALIVE")
    else:
        print("Channel does not exist")
    #Old Leaderboards are cleared  
    if LeaderboardChannel:
        await update_channel() 
        #!Display a new leaderbaord  
    board.update(users)
    print(board.people)

#test commands
##/squat command allows user to input their squat pr
@bot.slash_command(name="squat", description="input squat PR")
async def squat(ctx, pr: int):
    user = ctx.author
    #database input response chunk
    query = "INSERT INTO lifts VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (str(user.name), 1, 0, 0, pr))
    database.commit() #save function of the database :p
    
    await ctx.respond(f"{user.name} has inputted {pr} Lbs. as their squat PR!")

#moo command: sends a cow gif
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def moo(ctx):
    await ctx.send("http://imgur.com/gallery/YiMUiop")     
#error handling
@moo.error
async def moo_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"you are on cooldown! Try again in {round(error.retry_after, 2)} seconds")

# @bot.command()
# async def sendpr(ctx):
#     await ctx.

    #command template where the text is formatted as an embed. Will most likely use this format for most of the bots output
@bot.command()
async def embed(ctx):
    embed=discord.Embed(
    title="Text Formatting",
        #url="{url}",
        description="Here are some ways to format text",
        color=discord.Color.blue())
    #embed.set_author(name="Bot", url="{url}", icon_url="{urlimage}")
    #embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
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
#@bot.event
    
bot.run(TOKEN)
