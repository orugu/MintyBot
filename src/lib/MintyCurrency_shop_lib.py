from typing import Any
from lib.sqlalchemy_lib.engine import AsyncSessionLocal
from lib.sqlalchemy_lib.model import ServerShopInfo
from sqlalchemy.future import select
from src import MintyBot

client = MintyBot.client

def check_value_type(value):
    """Checks the type of the given value and returns 'int' or 'str' accordingly.
    :param value: The value to check.
    :return: 'int' if the value is an integer or a string representing an integer, 'str' if it's a string, None otherwise.
    :rtype: str | None
    """

    # 먼저 타입 자체가 int인지 확인
    if isinstance(value, int):
        return "int"
    
    # 문자열인데 숫자로만 구성되어 있는지 확인
    elif isinstance(value, str):
        if value.isdigit():
            return "int"   # 문자열이지만 숫자만 있으면 int로 취급 가능
        else:
            return "str"
    
    # 그 외 타입은 None 반환
    return None


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

async def shop_add_item(ctx, _item_name: str, _item_price: int, _item_description: str):
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
            print(f"[MintyCurrency Shop] Attempting to add item: {_item_name}, Price: {_item_price}, Description: {_item_description}" )

            async with AsyncSessionLocal() as session:
                try:
                    new_item = ServerShopInfo(
                        item_name=_item_name,
                        item_price=_item_price,
                        item_description=_item_description
                    )
                    session.add(new_item)
                    await session.commit()
                except Exception as e:
                    print(f"[MintyCurrency Shop] Error adding item to the shop: {e}")
                    await ctx.send("[MintyCurrency Shop] An error occurred while adding the item to the shop.")
                    return
            print(f"[MintyCurrency Shop] Item '{_item_name}' added to the shop successfully.")
            await ctx.send(f"[MintyCurrency Shop] Item '{_item_name}' added to the shop successfully.")
        except Exception as e:
            print(f"[MintyCurrency Shop] Error parsing command arguments: {e}")
            await ctx.send("[MintyCurrency Shop] Error parsing command arguments. Please ensure correct format.")
            return
    else:
        await ctx.send("[MintyCurrency] You do not have permission to add items to the shop.")
        print("[MintyCurrency Shop] Admin permission denied.")

async def shop_remove_item(ctx, _item_name: str):
    """Removes an item from the shop.
    :param ctx: The context of the command.
    :param item_name: The name of the item to remove.
    
    :return: None
    :rtype: None
    """

    if MintyBot.is_admin_permisson(ctx)==True:
        print("[MintyCurrency Shop] Admin permission confirmed.")
        print(f"[MintyCurrency Shop] Removing Item from Shop in channel: {ctx.channel.name}")
        print(f"[MintyCurrency Shop] Attempting to remove item: {_item_name}")
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(
                    select(ServerShopInfo)
                )
                item = result.scalars().all()
                item = next((i for i in item if i.item_name == _item_name), None)
                

                if item:
                    await session.delete(item)
                    await session.commit()
                    await ctx.send(f"[MintyCurrency Shop] Item '{_item_name}' removed from the shop successfully.")
                else:
                    await ctx.send(f"[MintyCurrency Shop] Item '{_item_name}' not found in the shop.")
            except Exception as e: 
                print(f"[MintyCurrency Shop] Error removing item: {e}")
                await ctx.send("[MintyCurrency Shop] An error occurred while removing the item from the shop.")
    else:
        await ctx.send("[MintyCurrency] You do not have permission to remove items from the shop.")

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

async def search_item(ctx):
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

async def set_item(ctx, fix_type: str, old_value: str, new_value: str):
    """Sets the name of an item in the shop.
    :param ctx: The context of the command.
    :param item_id: The ID of the item to update.
    :param item_name: The new name of the item.
    
    :return: None
    :rtype: None
    """

    if MintyBot.is_admin_permisson(ctx)==True:
        if check_value_type(old_value) == "int":
            old_value = int(old_value)
        elif check_value_type(old_value) == "str":
            old_value = str(old_value)
        else:
            await ctx.send("[MintyCurrency] Invalid value. Must be item ID or item name.")
            return

        if fix_type=="name":
            await set_item_name(ctx, old_value)
        elif fix_type=="price":
            await set_item_price(ctx, old_value, int(new_value))
        elif fix_type=="description":
            await set_item_description(ctx, old_value)

    else:
        await ctx.send("[MintyCurrency] You do not have permission to set item values.")
        print("[MintyCurrency Shop] Admin permission denied."   )


async def set_item_price(ctx, old_value, new_value: int):
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
            try:
                if type(old_value) ==int: 
                    result = await session.execute(
                        select(ServerShopInfo).where(ServerShopInfo.item_id == old_value)
                    )
                    item = result.scalars().first()
                    if item:
                        item.item_price = new_value
                        await session.commit()
                        await ctx.send(f"[MintyCurrency Shop] Item ID '{item.item_id}' price updated to {new_value} MintyCoins.")
                        print(f"[MintyCurrency Shop] Item ID '{item.item_id}' price updated to {new_value} MintyCoins.")
                    else:
                        await ctx.send(f"[MintyCurrency Shop] Item ID '{old_value}' not found in the shop.")
                        print(f"[MintyCurrency Shop] Item ID '{old_value}' not found in the shop.")

                elif type(old_value) ==str:
                    result = await session.execute(
                        select(ServerShopInfo).where(ServerShopInfo.item_name == old_value)
                    )
                    item = result.scalars().first()
                    if item:
                        item.item_price = new_value
                        await session.commit()
                        await ctx.send(f"[MintyCurrency Shop] Item Name '{item.item_name}' price updated to {new_value} MintyCoins.")
                        print(f"[MintyCurrency Shop] Item Name '{item.item_name}' price updated to {new_value} MintyCoins.")
                    else:
                        await ctx.send(f"[MintyCurrency Shop] Item Name '{old_value}' not found in the shop.")
                        print(f"[MintyCurrency Shop] Item Name '{old_value}' not found in the shop.")
            except Exception as e:
                print(f"[MintyCurrency Shop] Error setting item price: {e}")
                await ctx.send("[MintyCurrency Shop] An error occurred while setting the item price.")
    
    else:
        await ctx.send("[MintyCurrency] You do not have permission to set item prices.")
        print("[MintyCurrency Shop] Admin permission denied."   )


async def set_item_name(ctx, item_name_or_id: str | int):
    """Adds an item to the shop.
    :param ctx: The context of the command.
    :param item_name_or_id: The name or ID of the item to update.
    :param new_name: The new name for the item.
    :return: None
    :rtype: None
    """

    if MintyBot.is_admin_permisson(ctx)==True:
        print("[MintyCurrency Shop] Admin permission confirmed.")
        print(f"[MintyCurrency Shop] Setting Item Name in channel: {ctx.channel.name}")
        #item_name_or_id = item_name_or_id if isinstance(item_name_or_id, str) else None
        #todo: check if item_name_or_id is str or int, then search accordingly
        #즉, str이면 name으로 검색, int면 id로 검색. 따로 프로세스화 할 것
        #현재는 id로만 검색하게 되어있음

        async with AsyncSessionLocal() as session:
            try:
                if type(item_name_or_id) == str:
                    result = await session.execute(
                        select(ServerShopInfo).where(ServerShopInfo.item_name == item_name_or_id)
                    )
                    item = result.scalars().first()

                    if item:
                        item.item_name = ctx.message.content.split(' ',4)[4]
                        await session.commit()
                        await ctx.send(f"[MintyCurrency Shop] Item Name '{item.item_name}' updated to '{item.item_name}'.")
                        print(f"[MintyCurrency Shop] Item Name '{item.item_name}' updated to '{item.item_name}'.")
                    else:
                        await ctx.send(f"[MintyCurrency Shop] Item Name '{item.item_name}' not found in the shop.")
                        print(f"[MintyCurrency Shop] Item Name '{item.item_name}' not found in the shop.")
                        return
                    result = await session.execute(
                        select(ServerShopInfo).where(ServerShopInfo.item_id == item_name_or_id)
                    )
                    item = result.scalars().first()


                elif type(item_name_or_id) == int:
                    result = await session.execute(
                        select(ServerShopInfo).where(ServerShopInfo.item_id == item_name_or_id)
                    )
                    item = result.scalars().first()

                    if item:
                        item.item_name = ctx.message.content.split(' ',4)[4]
                        await session.commit()
                        await ctx.send(f"[MintyCurrency Shop] Item ID '{item.item_id}' name updated to '{item.item_name}'.")
                        print(f"[MintyCurrency Shop] Item ID '{item.item_id}' name updated to '{item.item_name}'.")
                    else:
                        await ctx.send(f"[MintyCurrency Shop] Item ID '{item_name_or_id}' not found in the shop.")
                        print(f"[MintyCurrency Shop] Item ID '{item_name_or_id}' not found in the shop.")

            except Exception as e:
                print(f"[MintyCurrency Shop] Error setting item name: {e}")
                await ctx.send("[MintyCurrency Shop] An error occurred while setting the item name.")
    else:
        await ctx.send("[MintyCurrency] You do not have permission to set item names.")
        print("[MintyCurrency Shop] Admin permission denied."   )

async def set_item_description(ctx, item_name_or_id: str | int):
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
            if type(item_name_or_id) == str:
                result = await session.execute(
                    select(ServerShopInfo).where(ServerShopInfo.item_name == item_name_or_id)
                )
                item = result.scalars().first()

                if item:
                    item.item_description = ctx.message.content.split(' ',4)[4]
                    await session.commit()
                    await ctx.send(f"[MintyCurrency Shop] Item Name '{item_name_or_id}' description updated.")
                    print(f"[MintyCurrency Shop] Item Name '{item_name_or_id}' description updated.")
                else:
                    await ctx.send(f"[MintyCurrency Shop] Item Name '{item_name_or_id}' not found in the shop.")
                    print(f"[MintyCurrency Shop] Item Name '{item_name_or_id}' not found in the shop.")
                return
            elif type(item_name_or_id) == int:
                result = await session.execute(
                    select(ServerShopInfo).where(ServerShopInfo.item_id == item_name_or_id)
                )
                item = result.scalars().first()

                if item:
                    item.item_description = ctx.message.content.split(' ',4)[4]
                    await session.commit()
                    await ctx.send(f"[MintyCurrency Shop] Item ID '{item_name_or_id}' description updated.")
                    print(f"[MintyCurrency Shop] Item ID '{item_name_or_id}' description updated.")
                else:
                    await ctx.send(f"[MintyCurrency Shop] Item ID '{item_name_or_id}' not found in the shop.")
                    print(f"[MintyCurrency Shop] Item ID '{item_name_or_id}' not found in the shop.")
            else:
                await ctx.send("[MintyCurrency] Invalid value. Must be item ID or item name.")
                return    
    else:
        await ctx.send("[MintyCurrency] You do not have permission to set item descriptions.")
        print("[MintyCurrency Shop] Admin permission denied."   )


