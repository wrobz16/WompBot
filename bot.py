import os
import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import json
from json import JSONDecodeError


#################################################
# SETUP
#################################################
def load_token():
    with open("token.txt", "r") as file:
        return file.readline().strip()
TOKEN = load_token()

def load_prefix():
    with open("prefix.txt", "r") as file:
        return file.readline().strip()
PREFIX = load_prefix() + " "

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

# BOSS ------------------------------------------
async def boss_message(message):
    # Skip if the bot itself sent the message
    if message.author == bot.user:
        return

    if 'boss' in message.content.lower():
        await message.reply("You better be talking about DADDY NIEK when saying boss!")


# ON MESSAGE ------------------------------------
@bot.event
async def on_message(message):
    print(f"Received message: {message.content}")  # Debugging line
    await boss_message(message)
    await bot.process_commands(message)  # This line is crucial to process commands.

#################################################
# COMMANDS
#################################################
command_descriptions = {}

# HELP ------------------------------------------
bot.remove_command('help')

command_descriptions['help'] = "Displays this help message."
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

command_descriptions['kos'] = "Displays the list of players that are KOS."
@bot.command(name='kos')
async def display_kos(ctx):
    if kos_list:
        kos_str = '\n'.join(kos_list)
        await ctx.send(f'KOS List:\n{kos_str}')
    else:
        await ctx.send('KOS List is empty.')

command_descriptions["kos_add <player>"] = "Adds a player to the KOS list"
@bot.command(name='kos_add')
async def kos_add(ctx, name: str):
    if name not in kos_list:
        kos_list.append(name)
        save_kos()
        await ctx.send(f'Added `{name}` to the KOS list.')
    else:
        await ctx.send(f'`{name}` is already in the KOS list.')

command_descriptions['kos_remove <player>'] = "Removes a player from the KOS list."
@bot.command(name='kos_remove')
async def kos_remove(ctx, name: str):
    if name in kos_list:
        kos_list.remove(name)
        save_kos()
        await ctx.send(f'Removed `{name}` from the KOS list.')
    else:
        await ctx.send(f'`{name}` is not in the KOS list.')

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

command_descriptions['allies'] = "Displays the list of players that are allies."
@bot.command(name='allies')
async def display_allies(ctx):
    if allies_list:
        allies_str = '\n'.join(allies_list)
        await ctx.send(f'allies List:\n{allies_str}')
    else:
        await ctx.send('allies List is empty.')

command_descriptions['allies_add <player>'] = "Adds a player to the allies list"
@bot.command(name='allies_add')
async def allies_add(ctx, name: str):
    if name not in allies_list:
        allies_list.append(name)
        save_allies()
        await ctx.send(f'Added `{name}` to the allies list.')
    else:
        await ctx.send(f'`{name}` is already in the allies list.')

command_descriptions['allies_remove <player>'] = "removes a player from the allies list."
@bot.command(name='allies_remove')
async def allies_remove(ctx, name: str):
    if name in allies_list:
        allies_list.remove(name)
        save_allies()
        await ctx.send(f'Removed `{name}` from the allies list.')
    else:
        await ctx.send(f'`{name}` is not in the allies list.')

# PLAY (YOUTUBE) --------------------------------
command_descriptions['play <YouTube URL or search query>'] = "Plays a song from YouTube."

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
command_descriptions['stop'] = "Stops the currently playing song."
@bot.command()
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        voice_client.stop()

# LEAVE -----------------------------------------
command_descriptions['leave'] = "Makes the bot leave the voice channel."
@bot.command()
async def leave(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        await voice_client.disconnect()

# CLEAR -----------------------------------------
command_descriptions['clear <amount>'] = "Clears the most recent <amount> of messages (default is 10)"
@bot.command(name='clear')
async def clear(ctx, amount: int = 10):
    if ctx.message.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Deleted {amount} messages.", delete_after=5)  # The message will be deleted after 5 seconds
    else:
        await ctx.send("You do not have permission to clear messages.")

#################################################
# MARKET
#################################################
sale_message = None
sell_file = "sell_data.json"
buy_file = "buy_data.json"

def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)

def load_from_file(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        return {}

user_sales = load_from_file(sell_file)
user_buys = load_from_file(buy_file)

# MARKET ----------------------------------------
@bot.command(name='market')
async def market(ctx):
    global sale_message, user_sales, user_buys, sell_file, buy_file

    if sale_message:
        try:
            await sale_message.delete()
        except discord.NotFound:
            print("Previous sale_message not found. It might have been deleted.")

    await ctx.message.delete()

    if not user_sales:
        save_to_file(user_sales, sell_file)
    if not user_buys:
        save_to_file(user_buys, buy_file)

    # Update the market message
    await update_market_message(ctx)

command_descriptions['buy/sell <item>'] = "Adds the item under your buying/selling list in the market."
command_descriptions['buy_remove/sell_remove'] = "Removes the item from your buying/selling list in the market."
# SELL ------------------------------------------
@bot.command(name='sell')
async def sell(ctx, *, item: str):
    global sale_message, user_sales
    author_name = str(ctx.author)

    if author_name not in user_sales:
        user_sales[author_name] = []
    user_sales[author_name].append(item)

    save_to_file(user_sales, sell_file)
    await update_market_message(ctx)

# BUY -------------------------------------------
@bot.command(name='buy')
async def buy(ctx, *, item: str):
    global sale_message, user_buys
    author_name = str(ctx.author)

    if author_name not in user_buys:
        user_buys[author_name] = []
    user_buys[author_name].append(item)

    save_to_file(user_buys, buy_file)
    await update_market_message(ctx)

# REMOVES ---------------------------------------
@bot.command(name='sell_remove')
async def sell_remove(ctx, *, item: str):
    global sale_message, user_sales
    author_name = str(ctx.author)

    if author_name in user_sales and item in user_sales[author_name]:
        user_sales[author_name].remove(item)

    if not user_sales[author_name]:
        del user_sales[author_name]

    save_to_file(user_sales, sell_file)
    await update_market_message(ctx)

@bot.command(name='buy_remove')
async def buy_remove(ctx, *, item: str):
    global sale_message, user_buys
    author_name = str(ctx.author)

    if author_name in user_buys and item in user_buys[author_name]:
        user_buys[author_name].remove(item)

    if not user_buys[author_name]:
        del user_buys[author_name]

    save_to_file(user_buys, buy_file)
    await update_market_message(ctx)

# UPDATE MESSAGE --------------------------------
async def update_market_message(ctx):
    global sale_message

    header = "**WOMP MARKET**\nDo `w! help` to learn more\n\n"

    sell_content = "**__SELLING__**\n"
    for username, items in user_sales.items():
        if items:
            sell_content += f"__{username}:__\n"
            for item in items:
                sell_content += f"- {item}\n"

    buy_content = "\n**__BUYING__**\n"
    for username, items in user_buys.items():
        if items:
            buy_content += f"__{username}:__\n"
            for item in items:
                buy_content += f"- {item}\n"

    # Combined the header with the rest of the content.
    new_content = header + sell_content + buy_content

    if sale_message is None:
        sale_message = await ctx.send(new_content)
    else:
        await sale_message.edit(content=new_content)


#################################################
# RUN
#################################################
bot.run(TOKEN)
