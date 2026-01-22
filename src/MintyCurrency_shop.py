from src import MintyBot

from lib.sqlalchemy_lib.model import Base
from lib.sqlalchemy_lib.engine import AsyncSessionLocal
from src.lib.MintyCurrency_shop_lib import set_item, shop_view, shop_add_item, shop_remove_item, set_item_name, set_item_price, set_item_description,shop_initialize,search_item

client = MintyBot.client

#redesign shop commands
@client.command()
async def shop(ctx, command: str = None, option1: str = None, option2: str = None, option3: str = None):
    """Handles shop-related commands.
    :param ctx: The context of the command.
    :param command: The specific shop command to execute.
    
    :return: None
    :rtype: None
    """
    print(f"shop command invoked with command: {command}, option1: {option1}, option2: {option2}, option3: {option3}")
    if command is None:
        await ctx.send("Available shop commands: view, add, remove, set_name, set_price, set_description, search, initialize.")
        return

    command = command.lower()

    if command == "view":
        await shop_view(ctx)

    elif command == "add":
        await shop_add_item(ctx, option1, option2, option3)

    elif command == "remove":
        await shop_remove_item(ctx, option1)

    elif command == "set":
        await set_item(ctx, option1, option2, option3)

    elif command == "search":
        await search_item(ctx)

    elif command == "initialize":
        await shop_initialize(ctx)
    else:
        await ctx.send(f"Unknown shop command: {command}. Available commands: view, add, remove, set_name, set_price, set_description, search, initialize.")




######현재까지 공부한것들######
#1. async def 했을때 즉 명령어를 input받을때, optional parameter의 갯수에 따라 ' '로 split이 자동으로 됨
#2. str의 경우 띄워쓰기가 포함될 경우 다음 parameter로 넘어가버림
#3. 그래서 todo: 어차피 자동으로 split되니까, set item name 이런식으로 받아서 뒤에 item id 하고 바꿀 값 입력받게끔 하면 될듯
###########################

