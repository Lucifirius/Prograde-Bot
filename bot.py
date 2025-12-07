import os
import random
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # This loads .env from /app/.env
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found! Check your .env file.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

FILES_DIR = Path(__file__).parent / "prograde_files"
AUTHORIZED_USER_IDS = {860310503578009630, 918951765188165663}  # Both of you


@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")
    # THIS LINE IS FIXED — works on discord.py 2.0+
    command_names = [cmd.name for cmd in bot.commands]
    print(f"Loaded commands: {', '.join(sorted(command_names))}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands
    raise error


# ====================== !prograde ======================
@bot.command(name="prograde")
async def prograde(ctx, number: str = None):
    if not FILES_DIR.exists():
        await ctx.send("`prograde_files` folder missing!")
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
        await ctx.send("Use a number or nothing: `!prograde 123` or `!prograde`")
        return

    matches = [
        f for f in files
        if f.stem == number and f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov', '.m4a'}
    ]

    if not matches:
        await ctx.send(f"No #{number} found.")
        return

    await ctx.send(file=discord.File(matches[0]))


# ====================== !upload (only for authorized IDs) ======================
@bot.command(name="upload")
async def upload(ctx):
    print(f"[DEBUG] !upload called by {ctx.author} ({ctx.author.id})")

    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("You don't have permission to use `!upload`.", delete_after=10)
        await ctx.message.delete(delay=10)
        return

    if len(ctx.message.attachments) != 1:
        await ctx.send("Please attach **exactly one** file.")
        return

    att = ctx.message.attachments[0]
    ext = Path(att.filename).suffix.lower()
    allowed = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov', '.m4a'}

    if ext not in allowed:
        await ctx.send(f"File type `{ext}` not allowed.\nAllowed: `{', '.join(allowed)}`")
        return

    FILES_DIR.mkdir(exist_ok=True)

    existing_nums = [int(f.stem) for f in FILES_DIR.iterdir() if f.is_file() and f.stem.isdigit()]
    next_num = max(existing_nums, default=0) + 1
    new_filename = f"{next_num}{ext}"
    save_path = FILES_DIR / new_filename

    await att.save(save_path)
    await ctx.send(f"Upload complete! Saved as `{new_filename}` (#{next_num})")


# Optional nice error messages
@prograde.error
@upload.error
async def command_error(ctx, error):
    await ctx.send("Something went wrong with the command.")


bot.run(TOKEN)