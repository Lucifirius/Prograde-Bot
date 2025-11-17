import os
import random
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

#Permissions Integer
#274878008320

# -------------------------------------------------
# Load token from .env (recommended) or environment
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # put your token in .env → DISCORD_TOKEN=...

# -------------------------------------------------
# Bot setup
intents = discord.Intents.default()
intents.message_content = True   # needed for reading commands

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------------------------------
# Where your files live
FILES_DIR = Path(__file__).parent / "prograde_files"

# -------------------------------------------------
@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")

# -------------------------------------------------
@bot.command(name="prograde")
async def prograde(ctx):
    """Upload a random file from prograde_files/"""
    if not FILES_DIR.is_dir():
        await ctx.send("❌ The file folder is missing! Contact the bot owner.")
        return

    files = [f for f in FILES_DIR.iterdir() if f.is_file()]
    if not files:
        await ctx.send("❌ No files found in the prograde folder.")
        return

    chosen = random.choice(files)

    # Discord.py can send a Path directly (v2.0+)
    file = discord.File(chosen)
    await ctx.send(file=file, content=f"")

# -------------------------------------------------
# (Optional) Simple error handler so the bot doesn't crash on bad input
@prograde.error
async def prograde_error(ctx, error):
    await ctx.send("Something went wrong with `!prograde`.")

# -------------------------------------------------
bot.run(TOKEN)
