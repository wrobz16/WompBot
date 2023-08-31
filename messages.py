import asyncio

# Boss - Niek
async def boss_message(message, bot):
    if message.author == bot.user:
        return

    if 'boss' in message.content.lower():
        await message.reply("You better be talking about DADDY NIEK when saying boss!")

# Peypel
async def peypel_message(message, bot):
    if message.author == bot.user:
        return

    if 'peypel' in message.content.lower():
        await message.reply("'PeyPel? More like GayPel.' - Taylor Swift, probably")
    
# Worst PvPer
async def worst_pvper(message, bot):
    if message.content.lower() == "hey womp bot, who is the worst pvper on complex?":
        async with message.channel.typing():
            await asyncio.sleep(2)  # Wait for 2 seconds while typing
            await message.channel.send("Stupid question, it is ICraftYouDont.")

# On Messages
async def on_message_event(bot, message):
    print(f"Received message: {message.content}")  # Debugging line

    await boss_message(message, bot)
    await peypel_message(message, bot)
    await worst_pvper(message, bot)
    await bot.process_commands(message)  # This line is crucial to process commands.
