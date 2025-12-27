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
        item_name = str(ctx.message.content.split(' ')[1])
        item_price = int(ctx.message.content.split(' ')[2])
        item_description = str(ctx.message.content.split(' ', 3)[3])

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