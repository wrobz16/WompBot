import discord
import json

from json import JSONDecodeError
from commands.help import command_descriptions


sale_message = None

def save_ids_to_file(channel_id, message_id, filename='ids.json'):
    data = {
        'channel_id': channel_id,
        'message_id': message_id
    }
    with open(filename, 'w') as f:
        json.dump(data, f)


def load_ids_from_file(filename='ids.json'):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data['channel_id'], data['message_id']
    except (FileNotFoundError, JSONDecodeError, KeyError):
        return None, None

async def initialize_market(bot):
    global sale_message
    channel_id, message_id = load_ids_from_file()

    if channel_id and message_id:
        channel = bot.get_channel(int(channel_id))
        if channel:
            try:
                sale_message = await channel.fetch_message(int(message_id))
            except discord.NotFound:
                print("Could not find the hardcoded message. You may need to generate a new one.")
                sale_message = None

def register(bot):
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

        new_content = header + sell_content + buy_content

        try:
            if sale_message is None:
                sale_message = await ctx.send(new_content)
            else:
                await sale_message.edit(content=new_content)
        except discord.NotFound:
            print("Previous sale_message not found. It might have been deleted.")
            sale_message = await ctx.send(new_content)


    @bot.command(name='market')
    async def market(ctx):
        global sale_message

        if sale_message:
            try:
                await sale_message.delete()
            except discord.NotFound:
                print("Previous sale_message not found. It might have been deleted.")
        await ctx.message.delete()

        await update_market_message(ctx)
        if sale_message:
            save_ids_to_file(sale_message.channel.id, sale_message.id)


    @bot.command(name='sell')
    async def sell(ctx, *, item: str):
        nonlocal user_sales

        author_name = str(ctx.author)

        if author_name not in user_sales:
            user_sales[author_name] = []
        user_sales[author_name].append(item)

        save_to_file(user_sales, sell_file)
        await update_market_message(ctx)

    @bot.command(name='buy')
    async def buy(ctx, *, item: str):
        nonlocal user_buys

        author_name = str(ctx.author)

        if author_name not in user_buys:
            user_buys[author_name] = []
        user_buys[author_name].append(item)

        save_to_file(user_buys, buy_file)
        await update_market_message(ctx)

    @bot.command(name='sell_remove')
    async def sell_remove(ctx, *, item: str):
        nonlocal user_sales

        author_name = str(ctx.author)

        if author_name in user_sales and item in user_sales[author_name]:
            user_sales[author_name].remove(item)

        if not user_sales[author_name]:
            del user_sales[author_name]

        save_to_file(user_sales, sell_file)
        await update_market_message(ctx)

    @bot.command(name='buy_remove')
    async def buy_remove(ctx, *, item: str):
        nonlocal user_buys

        author_name = str(ctx.author)

        if author_name in user_buys and item in user_buys[author_name]:
            user_buys[author_name].remove(item)

        if not user_buys[author_name]:
            del user_buys[author_name]

        save_to_file(user_buys, buy_file)
        await update_market_message(ctx)

    # Updating command descriptions
    command_descriptions['buy/sell <item>'] = "Adds the item under your buying/selling list in the market."
    command_descriptions['buy_remove/sell_remove'] = "Removes the item from your buying/selling list in the market."
