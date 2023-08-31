import os

from discord.ext import commands
from commands.help import command_descriptions

def register(bot):
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