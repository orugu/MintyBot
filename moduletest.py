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
#from MintyGPT2 import MGPT2
import pyglet 
import ctypes,sys
import etcfunction
from dotenv import load_dotenv
from mintyrank import rank, rankprocess
#private variables

music_count = 1
repeat_Flag = 0

client = commands.Bot(command_prefix='$!',intents=discord.Intents.all())
orient = "./music/"
voiceclient=discord.utils.get(client.voice_clients,guild=client.guilds)

#lists
music_queue = []  #music queue will stack like FIFO
title_list =[] 	  #music title will stack like FIFO

#music mp3 defines
def sanitize_file_name(file_name):
    file_name = file_name.replace("/", "_") #replace / to _
    return file_name



def nstart(ctx):
    voice =discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        ctx.send("music player is busy now...")

    else:
        if music_queue:
            voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source="music/"+music_queue[0]),after = lambda f: nstart(voice))
            music_queue.pop(0)
        else:
            voice.stop()
    
def search_files(directory, filename):
    for root, dirs, files in os.walk(directory):

        if filename in files:
            print(f"[ Minty Music ] File Founded: {os.path.join(root, filename)}")
            return True
        else:
            return False

#called when music channel has changed 
async def on_voice_state_update(member, before, after):

    #Finish announcement.
    print("[ Minty Music ] Music ended.")
    await member.send("Music is ended.")


async def get_youtube_title(url):
    ydl_opts = {
        'quiet': True,  #quiet output
        'extract_flat': True,  #download metadata
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)  #video info download
            video_title = info_dict.get('title', 'No Title')
            return video_title
        except Exception as e:
            return f"Error occured : {e}"


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
        print(f"'{filename}' Make file because there are no file")
        default_data = {}
        save_data(filename, default_data)
        return default_data


serverinfo = load_data('userdata.pkl')
#userrankinfo = load_data('userrankdata.pkl')
value =serverinfo["hertime"]



#chat events
@client.event
async def on_ready():
    print(f"[ Minty Bot ] Bot Logined: {client.user.name}")
    rank.get_db()



global profile



@client.event
async def on_message(message):

    randomnumber = random.randrange(1,999)
    if message.author == client.user: #Ignore bot's self message
        return


    #TTS Function
    if message.content.startswith("$$tts "):
        if message.author.voice and message.author.voice.channel:
            voice_channel = message.author.voice.channel
            print(f"User is in channel: {voice_channel}")
        else:
            await message.channel.send("Please join the voice channel first!")
            return
        
        tts_text = message.content[6:].strip()
        print(f"Received TTS request: {tts_text}")
        if tts_text[0].encode("utf-8").isalpha():
            langstatus = "en"
        else:
            langstatus = "ko"
        print(langstatus)



        #Create TTS Audio file
        tts = gTTS(tts_text, lang=langstatus)
        tts_file = "tts/tts.mp3"
        tts.save(tts_file)

        #Connect bot to Voice channel
        voice_client = message.guild.voice_client

        if voice_client is None or not voice_client.is_connected():
            #Connect voice client if there are no voice client�결
            vc = await voice_channel.connect()
        else:
            #if already connected, use that connection
            vc = voice_client

        if message.content.endswith("leave"):
            try:
                await vc.disconnect()
                return
            except Exception as e:
                await message.channel.send("Disconnected from voice channel already")
                return

        try:  #Play TTS voice file
            vc.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg',source="tts/tts.mp3"), after=lambda e: print("Done playing!"))
            while vc.is_playing():
                await asyncio.sleep(1)  #Wait until voice file end기
        except Exception as e:
            print(f"Error playing audio: {e}")

        finally:  #leave from voice channel
            if voice_channel.members == 0:
                await vc.disconnect()
                await message.channel.send(f"Disconnected from {voice_channel.name}")
                return

            if os.path.exists(tts_file):
                os.remove(tts_file)

    #etc functions
    if message.content == '$$hello':
        await message.channel.send('Hello!')

    if message.content == '$$ping!':
        await message.channel.send('Pong!')


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

    rank_profile = rank.RankDB.get_user(message.author)

    if message.content == "$$rank":
        await message.channel.send(f"level : {rank_profile.level} \n ")
        await message.channel.send(f"exp : {rank_profile.experience} / {rank_profile.max_experience} \n")
        await message.channel.send(f"nickname : {rank_profile.nickname} \n ")


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

atexit.register(on_exit)
load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))




