#Attention!
#MGPT2 will be disabled at rc versions.

#imports
import asyncio, discord, uvicorn
import yt_dlp, os, pickle, atexit

from gtts import gTTS
from src import MintyBot, MintyCurrency, etcfunction, channel_init
from dotenv import load_dotenv
from mintyrank import rank, rankprocess
from fastapi import FastAPI
from contextlib import asynccontextmanager

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
##############3

music_count = 1
repeat_Flag = 0

client = MintyBot.client
orient = "./music/"
voiceclient=discord.utils.get(client.voice_clients,guild=client.guilds)

#lists
music_queue = []  # 재생 대기열을 관리할 리스트
title_list =[] #제목 리스트


#music mp3 defines
def sanitize_file_name(file_name):
    # 슬래시를 언더스코어로 대체하고, 특수 문자는 제거
    file_name = file_name.replace("/", "_")
    return file_name

def nstart(ctx):    
    voice =discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    if voice.is_playing():
        ctx.send("이미 재생중입니다.")
    
    else:
        if music_queue:
            voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source="music/"+music_queue[0]),after = lambda f: nstart(voice))
            music_queue.pop(0)
        else:
            voice.stop()
    
def search_files(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            print(f"파일 발견: {os.path.join(root, filename)}")
            return True
        else:
            return False
        
async def on_voice_state_update(member, before, after):
    # 음성 채널에 접속하거나 음성 채널에 변경 사항이 있을 때 호출됩니다.

    # 노래가 끝났을 때 실행되는 함수x
    print("노래가 끝났습니다.")
    # 추가 작업을 여기에 정의할 수 있습니다.
    await member.send("노래가 끝났습니다!")


async def get_youtube_title(url):
    ydl_opts = {
        'quiet': True,  # 출력이 최소화되도록 설정
        'extract_flat': True,  # 실제 비디오를 다운로드하지 않고 메타데이터만 가져옵니다
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)  # 비디오 다운로드 없이 정보만 추출
            video_title = info_dict.get('title', '제목을 가져올 수 없습니다.')
            return video_title
        except Exception as e:
            return f"오류 발생: {e}"


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
    global MGPT_Load_Flag
    print(f"봇이 로그인되었습니다: {client.user.name}")

    #test code
    MGPT_Load_Flag= True
    print(f"[MGPT2] this is Test code for other modules. MGPT2 unloaded")
    
    if MGPT_Load_Flag == False:

        from MintyGPT2 import MGPT2
        await MGPT2.load_full_model()
        MGPT_Load_Flag = True
    else:
        print("[MGPT2] distilGPT2 already loaded")

    #MintyBot-Main DB Connection
    MintyBot.get_db()  #Main DB Connection

    #rank DB Connection
    rank.get_db()   #rank DB Connection

    #MintyCurrency DB Connection
    MintyCurrency.get_db()
    
    # 봇 이름 변경


global profile


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

        rank_profile = rank.RankDB.get_user(message.author)

        if message.content == "$$rank":
            rankmessage=("```"
                    f"level : {rank_profile.level}\n"
                    f"exp : {rank_profile.experience} / {rank_profile.max_experience}\n"
                    f"nickname : {rank_profile.nickname}\n"
                    "```")
            await message.channel.send(rankmessage)

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




@client.event
async def on_avatar(message):
    if message.content == '$$avatar':
        await message.channel.send("test point")
        await message.channel.author.getuser()

@client.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await ctx.send("Still Developing")
        await channel.connect()
    else:
        await ctx.send("Mintybot isn't in Voice Channel")

@client.command()
async def leave(ctx):
	await client.voice_clients[0].disconnect() #Exit from voice channel


@client.command()
async def play(ctx, url):
    global music_count
    global music_filename
    title = sanitize_file_name(await get_youtube_title(url))
    print(f"sanitized name : {title}")
    title.replace(" / ",".")
    title.replace("#",".")
    print(f"replaced name : {title}")

    if title == "No title":
        await ctx.send("URL is not Correct")
        return  #exit if function can't get title

    if search_files('music/',title+".mp3") ==True:
        print("[ Minty Music ] Music File Already Exists")
        music_queue.append("{title}.mp3")

    else:
        music_filename = f"music/{music_count}.{title}"
        print(f"[ Minty Music ] New download : {title}")

        ydl_opts = { # YouTube video download option
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f"music/{title}",
            'ffmpeg_location': '/usr/bin/ffmpeg',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  #Download Music from URL
            music_queue.append(f"{title}.mp3")  #Add Stack
            await ctx.send(f"Music added to Queue�: {url}")

    print(music_queue)

    #Connect to voice channel and play
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        if not ctx.voice_client:  #If bot disconnected to voice channel
            voice = await channel.connect()
        else:
            voice = ctx.voice_client

        if not voice.is_playing():  #If there's no Music Playing
            try:
                source_1=fr"music/{music_queue[0]}"
                if(music_queue[0]!=""):
                    try:
                        voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source=source_1),after=lambda e:nstart(voice) )
                    except Exception as e:
                        await ctx.send(f"error code: {e}")
                print(f"{source_1} \n {music_queue[0]}")
                music_count += 1
                await ctx.send(f"Now Playing : {music_queue[0]}")

            except Exception as e:
                await ctx.send(f"Error occured while Playing: {e}")
        else:
            await ctx.send(f"Music added to Queue : {url}")
    else:
        await ctx.send("Join to Voice Channel first!")

@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

    if music_queue:  #If music exist in Queue면
        print(music_queue.pop(0))   #Pop first Music title from music queue
        source_2 =f"music/{music_queue[0]}"  #file directory setting
        voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source=source_2))
        await ctx.send(f"Now Playing : {music_queue[0]}")

    else:
        await ctx.send("Queue is Empty.")  #notice when queue is empty

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) #voice info보

    if voice.is_playing(): #pause when music is playing
        voice.pause()

    else:
        await ctx.send("Music is not playing")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) #Voice status

    if voice.is_paused(): #resume when music is paused
        voice.resume()
    else:
        await ctx.send("Music is still playing")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) #Voice status
    global music_queue
    music_queue= []
    voice.stop()
    await voice.disconnect()

@client.command()
async def remove(ctx,num):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

    if voice.is_playing():
        if not music_queue:  #check the Queue for music's exist
            await ctx.send("Music is not in Queue")

        else:
            del music_count[num]
            await ctx.send(f"{num} music removed.")
    else:
        await ctx.send("There is no music.")

@client.command()
async def fstart(ctx):
    voice =discord.utils.get(client.voice_clients, guild=ctx.guild)
    global source_1
    print(music_queue[0])
    if voice.is_playing():
        await ctx.send("Music is already playing.")

    else:
        voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source=music_queue[0]))


@client.command()
async def queue(ctx):
    if not music_queue:
        await ctx.send("현재 재생 대기열이 비어 있습니다.")
    else:
        queue_list = "\n".join([f"{idx + 1}. {song}" for idx, song in enumerate(music_queue)])
        await ctx.send(f"```현재 재생 대기열:\n{queue_list}```")


@client.command()
async def image_load(ctx):
    image_path = 'image/image.png'
    print("code runned")
    await ctx.send(file=discord.File(image_path))


#가사, 차트 크롤링
#-------------------------------------------------------------------
#내 정보(!rank, !profile 등등)
#!avatar (프로필 사진 확대 출력)
#__init__ 파일을 통한 파일 분리 실행

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







