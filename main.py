#file name : main.py

#todo: module당 폴더 1개씩 refac.

#imports
import os,sys
from config import minty_env
minty_env.minty_config()

import asyncio, discord
import atexit
from MGPT2 import MGPT2_function
from gtts import gTTS
from src import MintyBot,channel_init,etcfunction,MintyCurrency,MintyMusic, MintyCurrency_shop
from dotenv import load_dotenv
from mintyrank import rank, rankprocess
from MintyGPT2 import MGPT2

#private variables

os.system('cls' if os.name == 'nt' else 'clear')  #windows and linux clear console

client = MintyBot.client

#chat events
@client.event
async def on_ready():

    print(f"봇이 로그인되었습니다: {client.user.name}")

    #MintyBot-Main DB Connection
    MintyBot.get_db()  #Main DB Connection

    #rank DB Connection
    rank.get_db()   #rank DB Connection 

    #MintyCurrency DB Connection
    await MintyCurrency.MCORM_Init()

    #MGPT2-Load
    await MGPT2_function.initialize()
    # 봇 이름 변경


@client.event
async def on_message(message):
    if message.author == client.user: # 봇 자신이 보내는 메세지는 무시
        return       
    
    print(f"[채널 ID] {message.channel.id}")  # Mintybot 채널 감지
    # 여기서 필요한 코드 추가 가능
    print(f"[Mintybot_dev] message.author={message}")
    print(f"[Mintybot_dev] message.channel={message.channel}")
    
    #channel checker
    if MintyBot.is_channel_enabled(message.channel.id):



        #from here, auto process rank and other commands

        await rankprocess.rank_process(message)
        await MintyCurrency.Currency_process(message)
    await client.process_commands(message)




@client.command()
async def on_avatar(ctx):
    await ctx.send("test point")
    await ctx.author.getuser()


def on_exit():

    print("program halted!")


async def main():
    
    atexit.register(on_exit)
    load_dotenv()
    #if os.getenv('MGPT2_Enable') == "true":
    #    MGPT_Load_Flag = True
    await client.start(os.getenv('DISCORD_TOKEN'))



if __name__=="__main__":
    
    asyncio.run(main())







