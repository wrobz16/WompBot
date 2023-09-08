import os
import json

from discord.ext import commands
from commands.help import command_descriptions

kos_message = None
kos_list = []

async def initialize_kos(bot):
    global kos_message, kos_list
    with open('kos_id.json', 'r') as f:
        config = json.load(f)
        channel_id = config['kos_channel_id']
    kos_channel = bot.get_channel(channel_id)
    
    if kos_channel is None:
        print(f"Could not find the channel with ID {channel_id}. Please make sure the bot has access and the channel ID is correct.")
        return

    last_messages = []
    async for message in kos_channel.history(limit=1):
        last_messages.append(message)

    if last_messages:
        kos_message = last_messages[0]
    else:
        kos_message = await kos_channel.send("Initializing KOS list...")
    
    kos_list = load_kos()
    await update_kos()

async def update_kos():
    kos_str = '\n'.join(kos_list) if kos_list else 'KOS List is empty.'
    await kos_message.edit(content=f'KOS List:\n{kos_str}')

def save_kos():
    kos_list.sort(key=str.lower)
    with open("kos_list.txt", "w") as file:
        for name in kos_list:
            file.write(name + "\n")

def load_kos():
    if os.path.exists("kos_list.txt"):
        with open("kos_list.txt", "r") as file:
            return sorted([line.strip() for line in file.readlines()], key=str.lower)
    return []

def register(bot):
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
            await update_kos()
        else:
            await ctx.send(f'`{name}` is already in the KOS list.')

    command_descriptions['kos_remove <player>'] = "Removes a player from the KOS list."
    @bot.command(name='kos_remove')
    async def kos_remove(ctx, name: str):
        if name in kos_list:
            kos_list.remove(name)
            save_kos()
            await ctx.send(f'Removed `{name}` from the KOS list.')
            await update_kos()
        else:
            await ctx.send(f'`{name}` is not in the KOS list.')