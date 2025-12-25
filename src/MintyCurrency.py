from dotenv import load_dotenv
from .lib import MintyCurrency_lib 
from . import MintyBot
from lib.sqlalchemy_lib import init_db


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





@client.command()

async def register(ctx):
    if MintyBot.is_channel_enabled(ctx.channel.id):
        await MintyCurrency_lib.UserCurrency.register(ctx)
        await ctx.send("[MintyCurrency] 회원가입 완료 메세지")


@client.command()
async def daily(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        #미완성. 완성 시 주석 해제
        await MintyCurrency_lib.UserCurrency.daily_check(ctx)
        await ctx.send("[MintyCurrency] 출석 체크")
        print("[MintyCurrency] 출석 체크")

@client.command()
async def money(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        MintyCurrency_lib.UserCurrency.user_balance_check()
        await ctx.send("[MintyCurrency] 돈 체크 ")
        print("[MintyCurrency] 돈 체크")

@client.command()
async def transfer(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        MintyCurrency_lib.UserCurrency.user_transfer()
        await ctx.send("[MintyCurrency] 송금 체크")
        print("[MintyCurrency] 송금 체크")

@client.command()
async def work(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        MintyCurrency_lib.UserCurrency.user_work()
        await ctx.send("[MintyCurrency] 일 체크")
        print("[MintyCurrency] 일 체크")

@client.command()
async def crime(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        MintyCurrency_lib.UserCurrency.user_crime()
        await ctx.send("[MintyCurrency] 범죄 체크")
        print("[MintyCurrency] 범죄 체크")

@client.command()
async def gamble(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        MintyCurrency_lib.UserCurrency.user_gamble()
        await ctx.send("[MintyCurrency] 도박 체크")
        print("[MintyCurrency] 도박 체크")

@client.command()
async def leaderboard(ctx):
    
    MintyBot.is_channel_enabled(ctx.channel.id)
    if  MintyBot.MintyBot_cur.fetchone()[0] == 1:
        MintyCurrency_lib.UserCurrency.user_leaderboard()
        await ctx.send("[MintyCurrency] 일 체크")
        print("[MintyCurrency] 일 체크")

@client.command()
async def profile(ctx):

    if MintyBot.is_channel_enabled(ctx.channel.id):
        await ctx.send(f"{MintyCurrency_lib.UserCurrency.__repr__()}")
        await ctx.send("[MintyCurrency] 사용자 정보 체크")
        print(f"{MintyCurrency_lib.UserCurrency.__repr__()}")
        print("[MintyCurrency] 사용자 정보 체크")

