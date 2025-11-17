import os
import random
from pathlib import Path
from fnmatch import fnmatch

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
async def prograde(ctx, *, filename: str = None):
    if not FILES_DIR.is_dir():
        await ctx.send("❌ prograde_files folder is missing!")
        return
    files = [f for f in FILES_DIR.iterdir() if f.is_file()]
    if not files:
        await ctx.send("❌ No files in prograde_files/")
        return
# ── EXACT match only (case-insensitive) ──
    filename_lower = filename.lower()
# Try exact full filename first (including extension if user typed it)
    chosen = next((f for f in files if f.name.lower() == filename_lower), None)
    # If not found and user didn't type an extension, try stem-only match
    if not chosen and '.' not in filename:
        chosen = next(
            (f for f in files if f.stem.lower() == filename_lower),
            None
        )
    if not chosen:
        await ctx.send(f"No file matching `{filename}` found.")
        return
    matches = matches[0]
    await ctx.send(
        file=discord.File(chosen),
        content=f""
    )
    # Optional: nice error message if something explodes
@prograde.error
async def prograde_error(ctx, error):
    await ctx.send("⚠️ Something went wrong with !prograde")
bot.run(TOKEN)