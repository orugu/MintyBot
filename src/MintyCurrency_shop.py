from src import MintyBot

from lib.sqlalchemy_lib.model import ServerShopInfo, Base
from sqlalchemy.future import select
from lib.sqlalchemy_lib.engine import AsyncSessionLocal

client = MintyBot.client


@client.command()
async def shop_initialize(ctx):
    """Displays the shop items available for purchase.
    :param ctx: The context of the command.
    
    :return: None
    :rtype: None
    """

    if MintyBot.is_admin_permisson(ctx)==True:
        print("[MintyCurrency Shop] Admin permission confirmed.")
        print(f"[MintyCurrency Shop] Shop Initialization Started in channel: {ctx.channel.name}")
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ServerShopInfo)
            )
            items = result.scalars().all()

        if not items:
            await ctx.send("[MintyCurrency Shop] The shop is currently empty.")
            return

        shop_message = "**Shop Items:**\n"
        for item in items:
            shop_message += f"**{item.item_name}** - {item.item_price} MintyCoins\n{item.item_description}\n\n"

        await ctx.send(shop_message)
    
    else:
        await ctx.send("[MintyCurrency] You do not have permission to initialize the shop.")

@client.command()
async def search_item(ctx, item_name:str):
    """Searches for an item in the shop.
    :param ctx: The context of the command.
    :param item_name: The name of the item to search for.
    
    :return: None
    :rtype: None
    """

    print(f"[MintyCurrency Shop] Searching for Item in channel: {ctx.channel.name}")
    item_name = str(ctx.message.content[13:])
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ServerShopInfo)
        )
        items = result.scalars().all()
        item = next((i for i in items if i.item_name == item_name), None)

    if item:
        shop_message = f"**{item.item_name}** - {item.item_price} MintyCoins\n{item.item_description}\n\nitem_id is {item.item_id}"
        await ctx.send(shop_message)
        print(f"[MintyCurrency Shop] Item '{item_name}' found in the shop.")
    else:
        await ctx.send(f"[MintyCurrency Shop] Item '{item_name}' not found in the shop.")
        print(f"[MintyCurrency Shop] Item '{item_name}' not found in the shop.")


######현재까지 공부한것들######
#1. async def 했을때 즉 명령어를 input받을때, optional parameter의 갯수에 따라 ' '로 split이 자동으로 됨
#2. str의 경우 띄워쓰기가 포함될 경우 다음 parameter로 넘어가버림
#3. 그래서 todo: 어차피 자동으로 split되니까, set item name 이런식으로 받아서 뒤에 item id 하고 바꿀 값 입력받게끔 하면 될듯
###########################
@client.command()
async def set_item_name(ctx, item_id:int):
    """Adds an item to the shop.
    :param ctx: The context of the command.
    :param item_name: The name of the item to add.
    
    :return: None
    :rtype: None
    """

    if MintyBot.is_admin_permisson(ctx)==True:
        print("[MintyCurrency Shop] Admin permission confirmed.")
        print(f"[MintyCurrency Shop] Setting Item Name in channel: {ctx.channel.name}")
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ServerShopInfo).where(ServerShopInfo.item_id == item_id)
            )
            item = result.scalars().first()

            if item:
                item.item_name = ctx.message.content.split(' ',2)[2]
                await session.commit()
                await ctx.send(f"[MintyCurrency Shop] Item ID '{item.item_id}' name updated to '{item.item_name}'.")
                print(f"[MintyCurrency Shop] Item ID '{item.item_id}' name updated to '{item.item_name}'.")
            else:
                await ctx.send(f"[MintyCurrency Shop] Item ID '{item_id}' not found in the shop.")
                print(f"[MintyCurrency Shop] Item ID '{item_id}' not found in the shop.")
    
    else:
        await ctx.send("[MintyCurrency] You do not have permission to set item names.")
        print("[MintyCurrency Shop] Admin permission denied."   )


@client.command()
async def set_item_price(ctx, item_id:int, item_price:int):
    """Sets the price of an item in the shop.
    :param ctx: The context of the command.
    :param item_id: The ID of the item to update.
    :param item_price: The new price of the item.
    
    :return: None
    :rtype: None
    """

    if MintyBot.is_admin_permisson(ctx)==True:
        print("[MintyCurrency Shop] Admin permission confirmed.")
        print(f"[MintyCurrency Shop] Setting Item Price in channel: {ctx.channel.name}")
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ServerShopInfo).where(ServerShopInfo.item_id == item_id)
            )
            item = result.scalars().first()

            if item:
                item.item_price = item_price
                await session.commit()
                await ctx.send(f"[MintyCurrency Shop] Item ID '{item_id}' price updated to {item_price} MintyCoins.")
                print(f"[MintyCurrency Shop] Item ID '{item_id}' price updated to {item_price} MintyCoins.")
            else:
                await ctx.send(f"[MintyCurrency Shop] Item ID '{item_id}' not found in the shop.")
                print(f"[MintyCurrency Shop] Item ID '{item_id}' not found in the shop.")
    
    else:
        await ctx.send("[MintyCurrency] You do not have permission to set item prices.")
        print("[MintyCurrency Shop] Admin permission denied."   )


@client.command()
async def set_item_description(ctx, item_id:int, *, item_description:str):
    """Sets the description of an item in the shop.
    :param ctx: The context of the command.
    :param item_id: The ID of the item to update.
    :param item_description: The new description of the item.
    
    :return: None
    :rtype: None
    """

    if MintyBot.is_admin_permisson(ctx)==True:
        print("[MintyCurrency Shop] Admin permission confirmed.")
        print(f"[MintyCurrency Shop] Setting Item Description in channel: {ctx.channel.name}")
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ServerShopInfo).where(ServerShopInfo.item_id == item_id)
            )
            item = result.scalars().first()

            if item:
                item.item_description = item_description
                await session.commit()
                await ctx.send(f"[MintyCurrency Shop] Item ID '{item_id}' description updated.")
                print(f"[MintyCurrency Shop] Item ID '{item_id}' description updated.")
            else:
                await ctx.send(f"[MintyCurrency Shop] Item ID '{item_id}' not found in the shop.")
                print(f"[MintyCurrency Shop] Item ID '{item_id}' not found in the shop.")
    
    else:
        await ctx.send("[MintyCurrency] You do not have permission to set item descriptions.")
        print("[MintyCurrency Shop] Admin permission denied."   )

@client.command()
async def shop_add_item(ctx, item_name: str, item_price: int, *, item_description: str):
    """Adds an item to the shop.
    :param ctx: The context of the command.
    :param item_name: The name of the item to add.
    :param item_price: The price of the item to add.
    :param item_description: The description of the item to add.
    
    :return: None
    :rtype: None
    """

    if MintyBot.is_admin_permisson(ctx)==True:
        print("[MintyCurrency Shop] Admin permission confirmed.")
        print(f"[MintyCurrency Shop] Adding Item to Shop in channel: {ctx.channel.name}")
        try:
            item_name = str(ctx.message.content.split(' ')[1])
            item_price = int(ctx.message.content.split(' ')[2])
            item_description = str(ctx.message.content.split(' ', 3)[3])
            print(f"[MintyCurrency Shop] Attempting to add item: {item_name}, Price: {item_price}, Description: {item_description}" )
        except Exception as e:
            print(f"[MintyCurrency Shop] Error parsing command arguments: {e}")
            await ctx.send("[MintyCurrency Shop] Error parsing command arguments. Please ensure correct format.")
            return
        async with AsyncSessionLocal() as session:
            new_item = ServerShopInfo(
                item_name=item_name,
                item_price=item_price,
                item_description=item_description
            )
            session.add(new_item)
            await session.commit()
        print(f"[MintyCurrency Shop] Item '{item_name}' added to the shop successfully.")
        await ctx.send(f"[MintyCurrency Shop] Item '{item_name}' added to the shop successfully.")
    
    else:
        await ctx.send("[MintyCurrency] You do not have permission to add items to the shop.")
        print("[MintyCurrency Shop] Admin permission denied.")

@client.command()
async def shop_remove_item(ctx, item_name: str):
    """Removes an item from the shop.
    :param ctx: The context of the command.
    :param item_name: The name of the item to remove.
    
    :return: None
    :rtype: None
    """

    if MintyBot.is_admin_permisson(ctx)==True:
        print("[MintyCurrency Shop] Admin permission confirmed.")
        print(f"[MintyCurrency Shop] Removing Item from Shop in channel: {ctx.channel.name}")
        item_name = str(ctx.message.content.split(' ')[1])
        print(f"[MintyCurrency Shop] Attempting to remove item: {item_name}")
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(
                    select(ServerShopInfo)
                )
                item = result.scalars().all()
                item = next((i for i in item if i.item_name == item_name), None)
                

                if item:
                    await session.delete(item)
                    await session.commit()
                    await ctx.send(f"[MintyCurrency Shop] Item '{item_name}' removed from the shop successfully.")
                else:
                    await ctx.send(f"[MintyCurrency Shop] Item '{item_name}' not found in the shop.")
            except Exception as e: 
                print(f"[MintyCurrency Shop] Error removing item: {e}")
                await ctx.send("[MintyCurrency Shop] An error occurred while removing the item from the shop.")
    else:
        await ctx.send("[MintyCurrency] You do not have permission to remove items from the shop.")

@client.command()
async def shop_view(ctx):
    """Displays the shop items available for purchase.
    :param ctx: The context of the command.
    
    :return: None
    :rtype: None
    """

    print(f"[MintyCurrency Shop] Viewing Shop in channel: {ctx.channel.name}")
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ServerShopInfo)
        )
        items = result.scalars().all()

    if not items:
        await ctx.send("[MintyCurrency Shop] The shop is currently empty.")
        return
    try:
        shop_message = "**Shop Items:**\n"
        print(f"[MintyCurrency Shop] Retrieved {items} items from the shop database.")
        print(f"[MintyCurrency Shop] Type of items: {type(items)}")
        for item in items:
            shop_message += f"**{item.item_name}** - {item.item_price} MintyCoins\n{item.item_description}\n\n"
        await ctx.send(shop_message)
    except Exception as e:
        print(f"[MintyCurrency Shop] Error displaying shop items: {e}")
        await ctx.send("[MintyCurrency Shop] An error occurred while displaying the shop items.")