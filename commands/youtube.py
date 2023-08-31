import discord
import yt_dlp as youtube_dl

from commands.help import command_descriptions

def register(bot):

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