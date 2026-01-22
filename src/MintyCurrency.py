from dotenv import load_dotenv
from .lib import MintyCurrency_lib 
from . import MintyBot
from lib.sqlalchemy_lib import init_db
from lib.sqlalchemy_lib.engine import AsyncSessionLocal
from lib.sqlalchemy_lib.model import ServerInfo
from sqlalchemy import select
client = MintyBot.client

# -----------------------------------
# .env config load
# add to .env
#
# MINTYBOT_DB_HOST="your ip or address"
# MINTYBOT_DB_PORT="your port"
# MINTYBOT_DB_USER="your user"
# MINTYBOT_DB_PASSWORD="your password"
# MINTYBOT_DB_DATABASE="your database"
# -----------------------------------

load_dotenv()

# -----------------------------------
# Connect to MariaDB
# -----------------------------------

async def MCORM_Init():
    """
    Initialize MintyCurrency ORM Service
    """
    print("[MintyCurrency] MintyCurrency DB Connection Started")
    try:
        await init_db.init_db()
        print("[MintyCurrency] MintyCurrency DB Connection Completed")
    except Exception as e:
        print(f"[MintyCurrency] MintyCurrency DB Connection Failed: {e}")


async def Currency_process(message):
    """
    Process MintyCurrency Commands
    args: message(discord.Message)
    returns: None
    """
    if message.author.bot:
        return
    try:
        async with AsyncSessionLocal() as db:
            # Process currency related commands here
            stmt = select(ServerInfo).where(ServerInfo.user_id == message.author.id)
            result = await db.execute(stmt)
            user = result.scalars().first()
            if user is None:
                pass    
            else:
                try:
                    # Update user currency data as needed
                    message_length = len(message.content)
                    user.user_balance += message_length  # Example: Earn currency based on message length
                    await db.commit()
                    
                except Exception as e:
                    print(f"[MintyCurrency] Currency Update Failed: {e}")
    except Exception as e:
        print(f"[MintyCurrency] Currency Process Failed: {e}")




@client.command()

async def register(ctx):
    """
    Register to MintyCurrency
    This command registers the user to MintyCurrency, which is required to use currency commands.
    """
    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.register(ctx)


@client.command()
async def daily(ctx):

    """
    Check if today is your daily check day.
    If it is, you will receive a bonus of 1000 currency.
    """
    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.daily_check(ctx)

@client.command()
async def money(ctx):
    """
    Check your current balance.
    """
    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_balance_check(ctx)

@client.command()
async def transfer(ctx, name, amount):

    """
    Transfer currency to another user: 1. Mention the user you want to transfer currency to
    2. Specify the amount of currency you want to transfer
    """
    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_transfer(ctx)


@client.command()
async def work(ctx):
    """
    Work to earn currency: 1. Earn currency by working
    2. The amount of currency earned will be randomly determined
    """
    
    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_work(ctx)


@client.command()
async def crime(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_crime(ctx)


@client.command()
async def gamble(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_gamble(ctx)


@client.command()
async def leaderboard(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_leaderboard(ctx)


@client.command()
async def profile(ctx):
    
    if MintyBot.is_channel_enabled(ctx.channel.id):
        await ctx.send(f"{MintyCurrency_lib.UserCurrency.__repr__()}")
        await ctx.send("[MintyCurrency] 사용자 정보 체크")
        print(f"{MintyCurrency_lib.UserCurrency.__repr__()}")
        print("[MintyCurrency] 사용자 정보 체크")

