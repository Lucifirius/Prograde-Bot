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
async def prograde(ctx, number: str = None):
    """
    !prograde          → random crow pill
    !prograde 123      → posts 123.png (or .jpg/.gif/.webp) if it exists
    """
    if not FILES_DIR.is_dir():
        await ctx.send("prograde_files folder missing!")
        return

    files = [f for f in FILES_DIR.iterdir() if f.is_file()]
    if not files:
        await ctx.send("No files in prograde_files/")
        return

    # ── No argument → random ──
    if number is None:
        chosen = random.choice(files)
        await ctx.send(file=discord.File(chosen), content="")
        return

    # ── Argument given → must be digits only ──
    if not number.isdigit():
        await ctx.send("Only numbers allowed! Use `!prograde 69` or just `!prograde` for random.")
        return

    # Look for a file that starts with the number followed by a dot (e.g. 69.png)
    possible_files = [f for f in files if f.stem == number and f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}]

    if not possible_files:
        await ctx.send(f"No #{number} found.")
        return

    # If multiple extensions exist (rare), pick the first
    chosen = possible_files[0]

    await ctx.send(
        file=discord.File(chosen),
        content=f""
    )
# Optional: nice error message if something explodes
@prograde.error
async def prograde_error(ctx, error):
    await ctx.send("Something went wrong with !prograde")
bot.run(TOKEN)