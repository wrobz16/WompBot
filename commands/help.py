from discord.ext import commands

command_descriptions = {}

def register(bot):
    bot.remove_command('help')

    command_descriptions['help'] = "Displays this help message."
    @bot.command(name='help')
    async def _help(ctx):
        help_text = "__**List of commands:**__\n"  # Header underlined and bold
        for command_name, description in command_descriptions.items():
            help_text += f"**{command_name}**: {description}\n"
        await ctx.send(help_text)