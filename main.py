#imports
import asyncio, discord
import random
from discord.ext import commands, tasks
import yt_dlp
import ffmpeg
import os, re
import pickle, atexit
import requests
from gtts import gTTS
from MGPT2 import *
from MintyGPT2 import MGPT2
import pyglet 
import ctypes,sys
import etcfunction

music_count = 1
repeat_Flag = 0


#variables
client = commands.Bot(command_prefix='$$',intents=discord.Intents.all())
level_1_max_experience = 200
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
        
        
#classes
def xp(chat_length):
    return len(chat_length)

class rank_profile:
    def __init__(self,name):
        self.nickname = client.user.name
        self.experience = 0
        self.level = 0
    
    def nickname_call(self):
        return self.nickname
    
    def experience_call(self):
        return self.experience
    
    def level_call(self):
        return self.level
    
    def experience(self,cl):
        self.experience += xp(cl)
    
    def exp_check(self):
        global message
        if self.experience >=level_1_max_experience*self.level:
            self.level+=1
        else:
            return



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
#userrankinfo = load_data('userrankdata.pkl')
value =serverinfo["hertime"]



#chat events
@client.event
async def on_ready():
    print(f"봇이 로그인되었습니다: {client.user.name}")
    await MGPT2.load_full_model()
    # 봇 이름 변경
    


@client.event
async def on_message(message):
    
    randomnumber = random.randrange(1,999)
    if message.author == client.user: # 봇 자신이 보내는 메세지는 무시
        return
    
    
    #guild_id = 1172715799690088488  # 특정 서버 ID
    #if message.guild and message.guild.id == guild_id:
    
    #if message.content == '헐':
       # await message.channel.send("헐 테스트중")
    
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
    
    # 데이터 불러오기
    if message.content == '$$hello':  # 만약 채팅이 '$hello'라면
        
        await message.channel.send('Hello!')  # Hello!라고 보내기
    
    
    if message.content == '$$ping!':
        
        await message.channel.send('Pong!')
    '''
    if message.content == '헐':
        global value, serverinfo
        serverinfo=load_data('userdata.pkl')
        print(value)
        print(serverinfo)
        
        value+=1
        serverinfo["hertime"] = value
        with open('userdata.pkl', 'wb') as file:
            pickle.dump(serverinfo,file)

        print("aftersave")
        print(value)
        print()
        
        await message.channel.send(str(value)+ '번 헐을 외쳤습니다')  # 문자열 형식으로 출력
    '''
    #rank
    if message.content == '$$rank':
        await message.channel.send("테스트중입니다")
        #check_and_create_class(message.author.username)
        await message.channel.send(rank_profile.nickname_call(message.author.username))

    #GPT2 Model

    if message.content == '$$주사위':
        a = random.randrange(1,7)
        b = random.randrange(1,7)
    
        if a > b:
            await message.channel.send("패배")
            await message.channel.send("봇의 숫자: " + str(a) + " 당신의 숫자: " +  str(b))
        elif a == b:
            await message.channel.send("무승부")
            await message.channel.send("봇의 숫자: " + str(a) + " 당신의 숫자: " +  str(b))
        elif a < b:
            await message.channel.send("승리")
            await message.channel.send("봇의 숫자: " + str(a) + " 당신의 숫자: " +  str(b))
        
    if message.content == "$$rank":
        await message.channel.send("레벨: "+rank_profile.level+"\n")
        await message.channel.send("경험치: " +rank_profile.experience +"\n")
 
    
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
        await ctx.send("음악기능 아직 미완성.")
        await channel.connect()
    else:
        await ctx.send("음성채널 없음")

@client.command()
async def leave(ctx):
	await client.voice_clients[0].disconnect() #음성채널 나가기



@client.command()
async def play(ctx, url):
    global music_count
    global music_filename
    title = await get_youtube_title(url) # 비동기 함수 호출로 제목 가져오기
    print(title)
    title = sanitize_file_name(title)
    print(title)
    title.replace(" / ",".")
    title.replace("#",".")
    print(title)
    if title == "제목을 가져올 수 없습니다.":
        await ctx.send("유효하지 않은 URL입니다.")
        return  # 제목을 가져오지 못했다면 함수 종료
    if search_files('music/',title+".mp3") ==True:
        print("이미 있음")
        music_queue.append(title+".mp3")
        
    else:
        print("새로 다운")
        music_filename = f"music/{music_count}.{title}"

        ydl_opts = { # YouTube 동영상 다운로드 옵션
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
            ydl.download([url])  # URL에서 음악 다운로드
            
            music_queue.append(f"{title}.mp3")  # 대기열에 추가
            await ctx.send(f"노래가 대기열에 추가되었습니다: {url}")

    print(music_queue)
    # 음성 채널 연결 및 재생
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        if not ctx.voice_client:  # 봇이 음성 채널에 연결되지 않은 경우
            voice = await channel.connect()
        else:
            voice = ctx.voice_client

        if not voice.is_playing():  # 재생 중인 노래가 없을 때
            try:
                song_to_play = music_queue[0]
                source_1="music/"+fr"{song_to_play}"
                if(music_queue[0]!=""):
                    try:
                        voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source=source_1),after=lambda e:nstart(voice) )
                    except Exception as e:
                        await ctx.send(f"error code: {e}")
                print(source_1)
                print("\n"+song_to_play)
                music_count += 1
                
                await ctx.send(f"현재 재생 중: {song_to_play}")
            except Exception as e:
                await ctx.send(f"재생 중 오류 발생: {e}")
        else:
            await ctx.send("이미 노래가 재생 중입니다. 대기열에 추가했습니다.")
    else:
        await ctx.send("먼저 음성 채널에 접속해 주세요.")

@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    print(music_queue[0])
    
    voice.stop()
    
    if music_queue:  # 대기열에 곡이 남아 있으면
        music_queue.pop(0)
        next_song = music_queue[0]  # 대기열에서 첫 번째 곡을 꺼냄

        source_2 ="music/"+f"{next_song}"  # 파일 경로 설정
        
        
        voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source=source_2))
        await ctx.send(f"현재 재생 중: {next_song}")
        #await ctx.send(f"재생 시작: {next_song}")
    else:
        await ctx.send("대기열이 비어 있습니다.")  # 대기열이 비었을 경우 알림


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) # 봇의 음성 관련 정보

    if voice.is_playing(): # 노래가 재생중이면
        voice.pause() # 일시정지
        
    else:
        await ctx.send("재생중인 곡 없음") # 오류 메시지

# 다시 재생
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) # 봇의 음성 관련 정보

    if voice.is_paused(): # 일시정지 상태이면
        voice.resume()
    else:
        await ctx.send("일시정지 아님") # 오류 메시지
        
#정지
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) # 봇의 음성 관련 정
    global music_queue
    music_queue= []
    voice.stop()
    await voice.disconnect()

#노래만 끄기

@client.command()
async def remove(ctx,num):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    
    if voice.is_playing():
        # 대기열에 음악이 있는지 확인
        if not music_queue:
            await ctx.send("현재 재생 대기열에 음악이 없습니다.")  

            return
        else:
            del music_count[num]
            await ctx.send("현재 재생 중인 곡이 중지되었습니다.")
    else:
        await ctx.send("재생 중인 곡이 없습니다.")


@client.command()
async def fstart(ctx):
    
    voice =discord.utils.get(client.voice_clients, guild=ctx.guild)
    global source_1
    print(music_queue[0])
    if voice.is_playing():
        await ctx.send("이미 재생중입니다.")
    
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
async def 그림생성(ctx):
    image_path = 'image/image.png'
    print("code runned")
    # discord.File 객체를 만들어서 이미지 전송
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

atexit.register(on_exit)

client.run(os.getenv("DISCORD_TOKEN"))





