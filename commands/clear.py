from commands.help import command_descriptions

def register(bot):
    command_descriptions['clear <amount>'] = "Clears the most recent <amount> of messages (default is 10)"

    @bot.command(name='clear')
    async def clear(ctx, amount: int = 10):
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"Deleted {amount} messages.", delete_after=5)  # msg deleted after 5 seconds
        else:
            await ctx.send("You do not have permission to clear messages.")