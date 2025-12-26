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
    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.register(ctx)


@client.command()
async def daily(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.daily_check(ctx)

@client.command()
async def money(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_balance_check(ctx)

@client.command()
async def transfer(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_transfer(ctx)
        await ctx.send("[MintyCurrency] 송금 체크")
        print("[MintyCurrency] 송금 체크")

@client.command()
async def work(ctx):
    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_work(ctx)
        await ctx.send("[MintyCurrency] 일 체크")
        print("[MintyCurrency] 일 체크")

@client.command()
async def crime(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_crime(ctx)
        await ctx.send("[MintyCurrency] 범죄 체크")
        print("[MintyCurrency] 범죄 체크")

@client.command()
async def gamble(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_gamble(ctx)
        await ctx.send("[MintyCurrency] 도박 체크")
        print("[MintyCurrency] 도박 체크")

@client.command()
async def leaderboard(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.user_leaderboard(ctx)
        await ctx.send("[MintyCurrency] 리더보드 체크")
        print("[MintyCurrency] 리더보드 체크")

@client.command()
async def profile(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await ctx.send(f"{MintyCurrency_lib.UserCurrency.__repr__()}")
        await ctx.send("[MintyCurrency] 사용자 정보 체크")
        print(f"{MintyCurrency_lib.UserCurrency.__repr__()}")
        print("[MintyCurrency] 사용자 정보 체크")

