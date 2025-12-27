import MintyBot

from lib.sqlalchemy_lib.model import ServerShopInfo, Base
from lib.sqlalchemy_lib.engine import AsyncSessionLocal


client = MintyBot.client


@client.command()
async def shop_initialize(ctx):
    """Displays the shop items available for purchase.
    :param ctx: The context of the command.
    
    :return: None
    :rtype: None
    """

    if MintyBot.is_admin_permisson(ctx) is True:
        print("[MintyCurrency Shop] Admin permission confirmed.")
        print(f"[MintyCurrency Shop] Shop Initialization Started in channel: {ctx.channel.name}")
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                ServerShopInfo.__table__.select()
            )
            items = result.scalars().all()

        if not items:
            await ctx.send("The shop is currently empty.")
            return

        shop_message = "**Shop Items:**\n"
        for item in items:
            shop_message += f"**{item.item_name}** - {item.item_price} MintyCoins\n{item.item_description}\n\n"

        await ctx.send(shop_message)