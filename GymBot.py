#Gymbot.py
import os
import discord
import random
import sqlite3
import asyncio
import aiosqlite
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands, tasks

load_dotenv()

#These IDs will correspond to your own IDs

TOKEN = os.getenv("DISCORD_TOKEN")

#Burger Guild
#GUILD = os.getenv("DISCORD_GUILD_1")

#UCM Gym Guild
GUILD = os.getenv("DISCORD_GUILD_2")

#Test Server IDs
# BOT_CHANNEL_ID = (int)(os.getenv("BOT_CHANNEL_0"))
# LEADERBAORD_CHANNEL_ID = (int)(os.getenv("LEADER_CHANNEL_0"))

#UCM Gym Server IDs
BOT_CHANNEL_ID = (int)(os.getenv("BOT_CHANNEL_2"))
LEADERBAORD_CHANNEL_ID = (int)(os.getenv("LEADER_CHANNEL_2"))

#Gym Leaderboard status
showcase = False
#'storage' of top users and their prs
top_squat_users = []
top_squat_prs = []
top_bench_users = []
top_bench_prs = []
top_deadl_users = []
top_deadl_prs = []

intents = discord.Intents.default() 
intents.messages = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#database variables
database = sqlite3.connect('lifts.db')
cursor = database.cursor()
database.execute("CREATE TABLE IF NOT EXISTS lifts(user STRING, is_squat INT, is_bench INT, is_deadlift INT, pr INT)")

async def sort_squat_prs():
    cursor.execute("SELECT * FROM lifts WHERE is_squat = 1 ORDER BY pr DESC")
    results = cursor.fetchall()
    #includes only squat prs
    for row in results:
        top_squat_users.append(row[0])
        top_squat_prs.append(row[4])
        
async def sort_bench_prs():
    cursor.execute("SELECT * FROM lifts WHERE is_bench = 1 ORDER BY pr DESC")
    results = cursor.fetchall()
    #includes only bench press prs
    for row in results:
        top_bench_users.append(row[0])
        top_bench_prs.append(row[4])
        
async def sort_deadl_prs():
    cursor.execute("SELECT * FROM lifts WHERE is_deadlift = 1 ORDER BY pr DESC")
    results = cursor.fetchall()
    #includes only deadlift prs
    for row in results:
        top_deadl_users.append(row[0])
        top_deadl_prs.append(row[4])
async def sort_prs():
    #need to still make sort functions for Bench Press and Deadlift
    await sort_squat_prs()   
    await sort_bench_prs()
    await sort_deadl_prs()

async def update_channel():
    channel = bot.get_channel(LEADERBAORD_CHANNEL_ID)
    await channel.purge()
    await sort_prs()
    
    squat_embed = discord.Embed(
        title = "Squat Leaderboard",
        color = discord.Color.blue()
    )
    if len(top_squat_prs) > 0:
        squat_embed.add_field(name = f"**:first_place: {top_squat_users[0]}**", value = f"{top_squat_prs[0]} lbs.", inline=False)
    if len(top_squat_prs) > 1:
        squat_embed.add_field(name = f"**:second_place: {top_squat_users[1]}**", value = f"{top_squat_prs[1]} lbs.", inline=False)
    if len(top_squat_prs) > 2:
        squat_embed.add_field(name = f"**:third_place: {top_squat_users[2]}**", value = f"{top_squat_prs[2]} lbs.")

    #Change it so it reflects bench stuff
    bench_embed = discord.Embed(
        title = "Bench Press Leaderboard",
        color = discord.Color.blue()
    )
    if len(top_bench_prs) > 0:
        bench_embed.add_field(name = f"**:first_place: {top_bench_users[0]}**", value = f"{top_bench_prs[0]} lbs.", inline=False)
    if len(top_bench_prs) > 1:
        bench_embed.add_field(name = f"**:second_place: {top_bench_users[1]}**", value = f"{top_bench_prs[1]} lbs.", inline=False)
    if len(top_bench_prs) > 2:
        bench_embed.add_field(name = f"**:third_place: {top_bench_users[2]}**", value = f"{top_bench_prs[2]} lbs.")
    
    deadl_embed = discord.Embed(
        title = "Deadlift Leaderboard",
        color = discord.Color.blue()
    )
    if len(top_deadl_prs) > 0:
        deadl_embed.add_field(name = f"**:first_place: {top_deadl_users[0]}**", value = f"{top_deadl_prs[0]} lbs.", inline=False)
    if len(top_deadl_prs) > 1:
        deadl_embed.add_field(name = f"**:second_place: {top_deadl_users[1]}**", value = f"{top_squat_prs[1]} lbs.", inline=False)
    if len(top_deadl_prs) > 2:
        deadl_embed.add_field(name = f"**:third_place: {top_deadl_users[2]}**", value = f"{top_deadl_prs[2]} lbs.")
    #can control when you want the leaderboard to show via 'showcase'
    if showcase:
        await channel.send(embed=squat_embed)
        await channel.send(embed=bench_embed)
        await channel.send(embed=deadl_embed)

async def insert_pr(username, lift_type, pr):
    lift_map = {
        "squat": (1, 0, 0),
        "bench": (0, 1, 0),
        "deadlift": (0, 0, 1)
    }
    if lift_type in lift_map:
        is_squat, is_bench, is_deadlift = lift_map[lift_type]
    async with aiosqlite.connect("lifts.db") as db:
        query = "INSERT INTO lifts VALUES (?, ?, ?, ?, ?)"
        try:
            await db.execute(query, (str(username), is_squat, is_bench, is_deadlift, pr))
            await db.commit()
            print("Insert successful.")
        except Exception as e:
            print(f"An error occurred: {e}")


@bot.event

async def on_ready():
    botChannel = bot.get_channel(BOT_CHANNEL_ID)
    LeaderboardChannel = bot.get_channel(LEADERBAORD_CHANNEL_ID)
    #bot announces in terminal that it has connected to the server
    for guild in bot.guilds:
        if guild.name == GUILD:
            print(
                f'{bot.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )
    #Bot shows announces it is online
    if botChannel:
        await botChannel.send(f"{bot.user} is now online!")
    else:
        print("Channel does not exist")
    #Old Leaderboards are cleared  
    if LeaderboardChannel:
        await update_channel() 

@bot.event
async def on_disconnect():
    channel = bot.get_channel(BOT_CHANNEL_ID)
    if channel:
        await channel.send(f"{bot.user} is now offline :(. Until next time!")

#squat pr command allows user to input their prs
@bot.slash_command(name="squat", description="input your squat PR (lbs.)")
@commands.cooldown(1, 5, commands.BucketType.user)
async def squat(ctx, pr: int):
    user = ctx.author
    #old sqlite database interaction
        # query = "INSERT INTO lifts VALUES (?, ?, ?, ?, ?)"
        # #1 0 0 = squat
        # cursor.execute(query, (str(user.name), 1, 0, 0, pr))
        # database.commit() #save function of the database :p
    await ctx.defer()
    await ctx.respond(f"{user.name} has inputted {pr} lbs. as their squat PR!")
    #new sqlite database interaction
    await insert_pr(str(user.name), "squat", pr)
#error handling
@squat.error
async def squat_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You are on cooldown! Try again in {round(error.retry_after, 2)} seconds")

#bench press pr command
@bot.slash_command(name="bench", description="input your bench press PR (lbs.)")
@commands.cooldown(1, 5, commands.BucketType.user)
async def bench(ctx, pr: int):
    user = ctx.author
    await ctx.defer()
    await ctx.respond(f"{user.name} has inputted {pr} lbs. as their bench press PR!")
    await insert_pr(str(user.name), "bench", pr)
#error handling
@bench.error
async def bench_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You are on cooldown! Try again in {round(error.retry_after, 2)} seconds")

#deadlift pr command
@bot.slash_command(name="deadlift", description="input your deadlift PR (lbs.)")
@commands.cooldown(1, 5, commands.BucketType.user)
async def deadlift(ctx, pr: int):
    user = ctx.author
    await ctx.defer()
    await ctx.respond(f"{user.name} has inputted {pr} lbs. as their deadlift PR!")
    await insert_pr(str(user.name), "deadlift", pr)
#error handling
@deadlift.error
async def deadlift_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You are on cooldown! Try again in {round(error.retry_after, 2)} seconds")
        
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def h(ctx):
    embed = discord.Embed(
        title = "List of Commands",
        description= "Currently server-relient, therefore if bot is not online, its commands will not be recieved :( " ,
        color = discord.Color.blue()
    )
    embed.add_field(name="/squat", value="command to insert your squat pr", inline=False)
    embed.add_field(name="/bench", value="command to insert your bench pr", inline=False)
    embed.add_field(name="/deadlift", value="command to insert your deadlift pr")
    await ctx.send(embed=embed)

bot.run(TOKEN)
