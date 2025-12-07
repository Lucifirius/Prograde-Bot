import os
import random
from pathlib import Path
from fnmatch import fnmatch

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Permissions Integer: 274878008320
# -------------------------------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# -------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # needed for attachment handling
bot = commands.Bot(command_prefix="!", intents=intents)

FILES_DIR = Path(__file__).parent / "prograde_files"
AUTHORIZED_USER_ID = 860310503578009630  # Your user ID

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")

# -------------------------------------------------
# Existing !prograde command (unchanged)
# -------------------------------------------------
@bot.command(name="prograde")
async def prograde(ctx, number: str = None):
    if not FILES_DIR.is_dir():
        await ctx.send("prograde_files folder missing!")
        return

    files = [f for f in FILES_DIR.iterdir() if f.is_file()]
    if not files:
        await ctx.send("No files in prograde_files/")
        return

    if number is None:
        chosen = random.choice(files)
        await ctx.send(file=discord.File(chosen))
        return

    if not number.isdigit():
        await ctx.send("Only numbers allowed! Use `!prograde 69` or just `!prograde` for random.")
        return

    possible_files = [
        f for f in files
        if f.stem == number and f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov', '.m4a'}
    ]

    if not possible_files:
        await ctx.send(f"No #{number} found.")
        return

    chosen = possible_files[0]
    await ctx.send(file=discord.File(chosen))

# -------------------------------------------------
# NEW: !upload command - only for authorized user
# -------------------------------------------------
@bot.command(name="upload")
async def upload(ctx):
    # --- Security check: only allow specific user ---
    if ctx.author.id != AUTHORIZED_USER_ID:
        await ctx.message.delete(delay=5)
        await ctx.send("You don't have permission to use `!upload`.", delete_after=5)
        return

    # --- Must have exactly one attachment ---
    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach a file to upload.")
        return
    if len(ctx.message.attachments) > 1:
        await ctx.send("Please attach only one file at a time.")
        return

    attachment = ctx.message.attachments[0]

    # --- Supported extensions ---
    allowed_exts = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov', '.m4a'}
    ext = Path(attachment.filename).suffix.lower()
    if ext not in allowed_exts:
        await ctx.send(f"File type `{ext}` not allowed. Supported: {', '.join(allowed_exts)}")
        return

    # --- Ensure directory exists ---
    FILES_DIR.mkdir(exist_ok=True)

    # --- Find the next available number ---
    existing_numbers = [
        int(f.stem) for f in FILES_DIR.iterdir()
        if f.is_file() and f.stem.isdigit()
    ]
    next_num = max(existing_numbers, default=0) + 1

    # --- New filename: e.g. 123.png ---
    new_filename = f"{next_num}{ext}"
    save_path = FILES_DIR / new_filename

    # --- Download and save the file ---
    await attachment.save(save_path)

    # --- Confirm success ---
    await ctx.send(f"Upload complete! Saved as `{new_filename}` (#{next_num})")

# -------------------------------------------------
@prograde.error
async def prograde_error(ctx, error):
    await ctx.send("Something went wrong with !prograde")

@upload.error
async def upload_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Failed to save the file. Check permissions or disk space.")
    else:
        await ctx.send("Something went wrong with !upload")

# -------------------------------------------------
bot.run(TOKEN)
