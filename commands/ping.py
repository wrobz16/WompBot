import json
from discord.ext import tasks
from datetime import datetime

async def ping_at_time(bot):
    # Read the JSON file
    with open('ping.json', 'r') as f:
        config = json.load(f)

    ping_hours = [1, 4, 7, 10, 13, 16, 19, 22]  # 12am to 9pm
    ping_minute = 45

    @tasks.loop(minutes=1.0)
    async def _task():
        now = datetime.now()
        if now.hour in ping_hours and now.minute == ping_minute:  # Check if it's one of the specified times
            guild_id = config['guild_id']
            guild = bot.get_guild(guild_id)
            if guild:
                role_id = config['role_id']
                role = guild.get_role(role_id)
                channel_id = config['channel_id']
                channel = bot.get_channel(channel_id)
                if role and channel:
                    await channel.send(f'{role.mention} TOMB Pond in 15 minutes, get in soon to avoid cooldown timer.')
    
    _task.start()

def register(bot):
    @bot.command(name='ping_pond')
    async def ping(ctx):
        # Read the JSON file
        with open('config.json', 'r') as f:
            config = json.load(f)

        POND_ROLE = config['role_id']
        role = ctx.guild.get_role(POND_ROLE)
        if role:
            await ctx.send(f'{role.mention} Pond in 15 minutes, get in soon to avoid cooldown timer.')
        else:
            await ctx.send('Role not found.')
