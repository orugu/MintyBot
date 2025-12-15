#official library
import mariadb, dotenv, os, random
#MintyBot library
from src import MintyBot

#load environment
dotenv.load_dotenv()

##########################################################################################
# this module doesn't need execute or fetchone, because of initialization for channel_id #
##########################################################################################

client = MintyBot.client

@client.command()
async def hello(ctx):
    await ctx.send(f"Hello! I'm MintyBot! Anything you needed, type {os.getenv('COMMAND_PREFIX','+')}help")

@client.command()
async def ping(ctx):
    await ctx.send('pong!')

@client.command()
async def 주사위(ctx):
        a = random.randrange(1,7)
        b = random.randrange(1,7)

        if a > b:
            await ctx.send("패배")
            await ctx.send("봇의 숫자: " + str(a) + " 당신의 숫자: " +  str(b))
        elif a == b:
            await ctx.send("무승부")
            await ctx.send("봇의 숫자: " + str(a) + " 당신의 숫자: " +  str(b))
        elif a < b:
            await ctx.send("승리")
            await ctx.send("봇의 숫자: " + str(a) + " 당신의 숫자: " +  str(b))

@client.command()
async def mintyhelp(ctx):
     await ctx.send("아직 준비중입니다.")


