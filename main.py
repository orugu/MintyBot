#file name : main.py

#imports
import os 
from config import minty_env
minty_env.minty_config()

import asyncio, discord, uvicorn
import pickle, atexit
from MGPT2 import MGPT2_function
from gtts import gTTS
from src import MintyBot,channel_init,etcfunction,MintyCurrency,MintyMusic
from dotenv import load_dotenv
from mintyrank import rank, rankprocess
from fastapi import FastAPI
from contextlib import asynccontextmanager
from MintyGPT2 import MGPT2
#private variables

##############fastapi
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
   #todo: SQLAlchemy 진행 

    yield
    #endpoint
    


@app.get("/")
async def root():
    return {"status": "Mintybot is running"}
##############

client = MintyBot.client

def check_and_create_class(class_name):
    if class_name not in globals():
        globals()[class_name] =type(class_name,(object,),{"__init__":lambda self,name:setattr(self,"name",name)})
        return

#data save
def save_data(profile, filename):
    with open(filename, 'wb') as file:
        pickle.dump(profile, file)
        
#data load
def load_data(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"'{filename}' 파일이 없어서 새로 생성합니다.")
        default_data = {}
        save_data(filename, default_data)
        return default_data

serverinfo = load_data('userdata.pkl')
value =serverinfo["hertime"]

#chat events
@client.event
async def on_ready():

    print(f"봇이 로그인되었습니다: {client.user.name}")

    #MGPT2-Load
    await MGPT2_function.initialize()

    #MintyBot-Main DB Connection
    MintyBot.get_db()  #Main DB Connection

    #rank DB Connection
    rank.get_db()   #rank DB Connection

    #MintyCurrency DB Connection
    MintyCurrency.get_db()
    
    # 봇 이름 변경


@client.event
async def on_message(message):
    if message.author == client.user: # 봇 자신이 보내는 메세지는 무시
        return    
    
    #channel checker
    MintyBot.MintyBot_cur.execute("SELECT EXISTS(SELECT 1 FROM serverinfo WHERE channel_id = ?)", (message.channel.id,))
    
    if  MintyBot.MintyBot_cur.fetchone()[0] == 1:
        print(f"[채널 ID] {message.channel.id}")  # Mintybot 채널 감지
        # 여기서 필요한 코드 추가 가능
        print(f"[Mintybot_dev] message.author={message}")
        print(f"[Mintybot_dev] message.channel={message.channel}")
        
        
        if message.content.startswith('$$문장생성'):
            text= message.content[6:]
            #문장생성 함수-
            await MGPT2.MGPT_generation(message,text)

        if message.content.startswith('$$질문답변'):
            text = message.content[6:]
            await MGPT2.MGPT_question(message,text)

        



        if message.content.startswith("$$tts "):
            # 메시지 내용에서 TTS 텍스트 추출
            if message.author.voice and message.author.voice.channel:
                voice_channel = message.author.voice.channel
                print(f"User is in channel: {voice_channel}")
            else:
                await message.channel.send("먼저 음성 채널에 들어가 주세요!")
                return
            
            tts_text = message.content[6:].strip()
            print(f"Received TTS request: {tts_text}")
            if tts_text[0].encode("utf-8").isalpha():
                langstatus = "en"
            else:
                langstatus = "ko"
            print(langstatus)

            
            # TTS 오디오 파일 생성 (gTTS 예제)
            tts = gTTS(tts_text, lang=langstatus)
            tts_file = "tts/tts.mp3"
            tts.save(tts_file)
            
            # 음성 채널에 봇 연결
            voice_client = message.guild.voice_client

            if voice_client is None or not voice_client.is_connected():
                # 음성 클라이언트가 없거나 연결되어 있지 않으면 새로 연결
                vc = await voice_channel.connect()
            else:
                # 이미 연결되어 있으면 그 연결을 사용
                vc = voice_client

            if message.content.endswith("leave"):
                try:        
                    await vc.disconnect()
                    return
                except Exception as e:
                    await message.channel.send("음성채널에 연결되어 있지 않습니다")
                    return
            # TTS 파일 재생
            try:
                vc.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg',source="tts/tts.mp3"), after=lambda e: print("Done playing!"))
                while vc.is_playing():
                    await asyncio.sleep(1)  # 재생이 끝날 때까지 대기
            except Exception as e:
                print(f"Error playing audio: {e}")
            
            finally:
                # 음성 채널에서 봇 나가기
                if voice_channel.members == 0:
                    await vc.disconnect()
                    await message.channel.send(f"{voice_channel.name} 채널에는 아무도 없습니다. 음성 채널에 누군가 있을 때 다시 시도하세요!")
                    return
                
                if os.path.exists(tts_file):
                    os.remove(tts_file)


        #from here, auto process rank and other commands

        await rankprocess.rank_process(message)
        
    await client.process_commands(message)




@client.command()
async def on_avatar(ctx):
    await ctx.send("test point")
    await ctx.author.getuser()


def on_exit():
    global serverinfo   
    save_data(serverinfo,'userdata.pkl')
    print("program halted!")


async def main():

    atexit.register(on_exit)
    load_dotenv()
    if os.getenv('MGPT2_Enable') == "true":
        MGPT_Load_Flag = True
    bot_task = asyncio.create_task(client.start(os.getenv('DISCORD_TOKEN')))
    uvicorn_config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        loop="asyncio",       # ← 중요 (loop 생성 방지)
        http="auto",
    )
    uvicorn_server = uvicorn.Server(uvicorn_config)

    uvicorn_task = asyncio.create_task(uvicorn_server.serve())
    await asyncio.gather(bot_task, uvicorn_task)


if __name__=="__main__":
    
    asyncio.run(main())







