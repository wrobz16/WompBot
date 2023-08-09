import os
import discord
from discord.ext import commands
import yt_dlp as youtube_dl

#################################################
# SETUP
#################################################
def load_token():
    with open("token.txt", "r") as file:
        return file.readline().strip()

TOKEN = load_token()

PREFIX = "! "
intents=discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord.')

#################################################
# ON ERRORS
#################################################
@bot.event
async def on_command_error(ctx, error):
    print(f"Command error: {error}")

#################################################
# MESSAGES
#################################################
@bot.event
async def on_message(message):
    print(f"Received message: {message.content}")  # Debugging line
    await bot.process_commands(message)  # This line is crucial to process commands.

#################################################
# COMMANDS
#################################################
command_descriptions = {
    "help": "Displays this help message.",
    "kos": "Displays the list of players that are KOS.",
    "kos_add <player>": "Adds a player to the KOS list",
    "kos_remove <player>": "removes a player from the KOS list.",
    "allies": "Displays the list of players that are allies.",
    "allies_add <player>": "Adds a player to the allies list",
    "allies_remove <player>": "removes a player from the allies list.",
    "play <YouTube URL or search query>": "Plays a song from YouTube.",
    "stop": "Stops the currently playing song.",
    "leave": "Makes the bot leave the voice channel."
}

# HELP ------------------------------------------
bot.remove_command('help')

@bot.command(name='help')
async def _help(ctx):
    help_text = "__**List of commands:**__\n"  # Header underlined and bold
    for command_name, description in command_descriptions.items():
        help_text += f"**{command_name}**: {description}\n"
    await ctx.send(help_text)

# KOS -------------------------------------------
def save_kos():
    with open("kos_list.txt", "w") as file:
        for name in kos_list:
            file.write(name + "\n")

def load_kos():
    if os.path.exists("kos_list.txt"):
        with open("kos_list.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

kos_list = load_kos()

@bot.command(name='kos_add')
async def kos_add(ctx, name: str):
    if name not in kos_list:
        kos_list.append(name)
        save_kos()
        await ctx.send(f'Added `{name}` to the KOS list.')
    else:
        await ctx.send(f'`{name}` is already in the KOS list.')

@bot.command(name='kos_remove')
async def kos_remove(ctx, name: str):
    if name in kos_list:
        kos_list.remove(name)
        save_kos()
        await ctx.send(f'Removed `{name}` from the KOS list.')
    else:
        await ctx.send(f'`{name}` is not in the KOS list.')

@bot.command(name='kos')
async def display_kos(ctx):
    if kos_list:
        kos_str = '\n'.join(kos_list)
        await ctx.send(f'KOS List:\n{kos_str}')
    else:
        await ctx.send('KOS List is empty.')

# ALLIES ----------------------------------------
def save_allies():
    with open("allies_list.txt", "w") as file:
        for name in allies_list:
            file.write(name + "\n")

def load_allies():
    if os.path.exists("allies_list.txt"):
        with open("allies_list.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

allies_list = load_allies()

@bot.command(name='allies_add')
async def allies_add(ctx, name: str):
    if name not in allies_list:
        allies_list.append(name)
        save_allies()
        await ctx.send(f'Added `{name}` to the allies list.')
    else:
        await ctx.send(f'`{name}` is already in the allies list.')

@bot.command(name='allies_remove')
async def allies_remove(ctx, name: str):
    if name in allies_list:
        allies_list.remove(name)
        save_allies()
        await ctx.send(f'Removed `{name}` from the allies list.')
    else:
        await ctx.send(f'`{name}` is not in the allies list.')

@bot.command(name='allies')
async def display_allies(ctx):
    if allies_list:
        allies_str = '\n'.join(allies_list)
        await ctx.send(f'allies List:\n{allies_str}')
    else:
        await ctx.send('allies List is empty.')

# PLAY (YOUTUBE) --------------------------------

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': False,
    'source_address': '0.0.0.0',
    'force_generic_extractor': True,
}

@bot.command(name='play')
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return
    channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch1:{search}", download=False)
        if 'entries' not in search_results:
            await ctx.send("No suitable format found. Please try another video.")
            return
        
        video_url = search_results['entries'][0]['url']
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=video_url, 
                        options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'),
                        after=lambda e: print(f'Player error: {e}') if e else None)

# STOP ------------------------------------------
@bot.command()
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        voice_client.stop()

# LEAVE -----------------------------------------
@bot.command()
async def leave(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        await voice_client.disconnect()

#################################################
# RUN
#################################################
bot.run(TOKEN)
