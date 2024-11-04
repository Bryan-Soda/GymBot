#Gymbot.py
import os
import discord
import random
import sqlite3
import asyncio
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands

load_dotenv()

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

def insert_pr(username, lift_type, pr):
    lift_map = {
        "squat": (1, 0, 0),
        "bench": (0, 1, 0),
        "deadlift": (0, 0, 1)
    }
    if lift_type in lift_map:
        is_squat, is_bench, is_deadlift = lift_map[lift_type]
    else:
        raise ValueError("Invalid lift type")

    query = "INSERT INTO lifts VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (str(username.name), is_squat, is_bench, is_deadlift, pr))
    database.commit() #save function of the database :p


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
#These IDs will correspond to your own channel IDs
BOT_CHANNEL_ID = 1302693228105039974
LEADERBAORD_CHANNEL_ID = 1302700107871027233

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
        await botChannel.send(f"{bot.user} is online!")
    else:
        print("Channel does not exist")
    #Old Leaderboards are cleared  
    if LeaderboardChannel:
        await update_channel() 
        #!Display a new leaderbaord  
    board.update(users)
    print(board.people)

#squat pr command allows user to input their prs
@bot.slash_command(name="squat", description="input squat PR")
@commands.cooldown(1, 5, commands.BucketType.user)
async def squat(ctx, pr: int):
    user = ctx.author
    #sqlite database interaction
        # query = "INSERT INTO lifts VALUES (?, ?, ?, ?, ?)"
        # #1 0 0 = squat
        # cursor.execute(query, (str(user.name), 1, 0, 0, pr))
        # database.commit() #save function of the database :p
    await ctx.respond("Processing your squat PR...")
    await insert_pr(str(user.name), pr)
    await ctx.respond(f"{user.name} has inputted {pr} Lbs. as their squat PR!")
#error handling
@squat.error
async def squat_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You are on cooldown! Try again in {round(error.retry_after, 2)} seconds")

#bench press pr command
@bot.slash_command(name="bench", description="input bench PR")
@commands.cooldown(1, 5, commands.BucketType.user)
async def bench(ctx, pr: int):
    user = ctx.author
    #sqlite database interaction
    query = "INSERT INTO lifts VALUES (?, ?, ?, ?, ?)"
    #0 1 0 = bench
    cursor.execute(query, (str(user.name), 0, 1, 0, pr))
    database.commit() #save function of the database :p
    await ctx.respond(f"{user.name} has inputted {pr} Lbs. as their bench PR!")
#error handling
@bench.error
async def bench_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You are on cooldown! Try again in {round(error.retry_after, 2)} seconds")

# #deadlift pr command
# @bot.slash_command(name="deadlift", description="input deadlift PR")
# @commands.cooldown(1, 5, commands.BucketType.user)
# async def deadlift(ctx, pr: int):
#     embed=discord.Embed(
#     title="Deadlift PR",
#         description= (f"{user.name} has inputted {pr} Lbs. as their deadlift PR!"),
#         color=discord.Color.blue())
#     user = ctx.author
#     #sqlite database interaction
#     query = "INSERT INTO lifts VALUES (?, ?, ?, ?, ?)"
#     #0 0 1 = deadlift
#     cursor.execute(query, (str(user.name), 0, 0, 1, pr))
#     database.commit() #save function of the database :p
#     #await ctx.respond(f"{user.name} has inputted {pr} Lbs. as their deadlift PR!")
#     await ctx.respond(embed=embed)
# #error handling
# @deadlift.error
# async def deadlift_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You are on cooldown! Try again in {round(error.retry_after, 2)} seconds")

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

#command template where the text is formatted as an embed. Will most likely use this format for most of the bots output
@bot.command()
async def embed(ctx):
    #!
    embed=discord.Embed(
    title="Text Formatting",
        #url="{url}",
        description="Here are some ways to format text",
        color=discord.Color.blue())
    #!
    embed.add_field(name="*Italics*", value="Surround your text in asterisks ()", inline=False)
    embed.add_field(name="**Bold**", value="Surround your text in double asterisks ()", inline=False)
    embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
    embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
    embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
    embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
    embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
    embed.set_footer(text="Foot")
    #!
    await ctx.send(embed=embed)
#@bot.event
    
bot.run(TOKEN)
