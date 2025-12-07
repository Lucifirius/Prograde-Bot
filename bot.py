import os
import random
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("No DISCORD_TOKEN found in .env")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

FILES_DIR = Path(__file__).parent / "prograde_files"
AUTHORIZED_USER_IDS = {860310503578009630, 918951765188165663}

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    print(f"Loaded commands: {', '.join(bot.commands.keys())}")  # ← THIS IS KEY


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # silently ignore unknown commands
    raise error


# ====================== !prograde ======================
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
        await ctx.send("Only numbers allowed! Example: `!prograde 69`")
        return

    matches = [f for f in files if f.stem == number and f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov', '.m4a'}]
    if not matches:
        await ctx.send(f"No #{number} found.")
        return

    await ctx.send(file=discord.File(matches[0]))


# ====================== !upload ======================
@bot.command(name="upload")
async def upload(ctx):
    print(f"!upload invoked by {ctx.author} ({ctx.author.id})")  # debug line

    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You don't have permission to use `!upload`.", delete_after=10)
        await ctx.message.delete(delay=10)
        return

    if len(ctx.message.attachments) != 1:
        await ctx.send("⚠️ Please attach **exactly one** file.")
        return

    attachment = ctx.message.attachments[0]
    ext = Path(attachment.filename).suffix.lower()
    allowed = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov', '.m4a'}
    if ext not in allowed:
        await ctx.send(f"❌ Unsupported file type `{ext}`. Allowed: {', '.join(allowed)}")
        return

    FILES_DIR.mkdir(exist_ok=True)

    existing = [int(f.stem) for f in FILES_DIR.iterdir() if f.is_file() and f.stem.isdigit()]
    next_num = max(existing, default=0) + 1
    new_name = f"{next_num}{ext}"
    save_path = FILES_DIR / new_name

    await attachment.save(save_path)
    await ctx.send(f"✅ Upload complete! Saved as `{new_name}` (#{next_num})")


# Error handlers (optional but nice)
@prograde.error
async def prograde_error(ctx, error):
    await ctx.send("Something broke in !prograde")

@upload.error
async def upload_error(ctx, error):
    await ctx.send("Something broke in !upload")


bot.run(TOKEN)
