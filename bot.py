import discord
from discord.ext import commands
import importlib
import os

import settings
import messages
from commands.market import initialize_market


# Initialize bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents, case_insensitive=True)

# Register commands
commands_folder_path = "./commands"
for filename in os.listdir(commands_folder_path):
    if filename.endswith(".py"):
        module_name = filename[:-3]  # Remove the '.py' from the filename to get the module name
        module = importlib.import_module(f"commands.{module_name}")
        module.register(bot)

# When bot is loaded
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord.')
    await initialize_market(bot) # Market message

# For messages
@bot.event
async def on_message(message):
    await messages.on_message_event(bot, message)

# On error
@bot.event
async def on_command_error(ctx, error):
    print(f"Command error: {error}")

# Run the bot
bot.run(settings.TOKEN)
