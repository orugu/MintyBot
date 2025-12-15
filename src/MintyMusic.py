#file name : MintyMusic.py

from src import MintyBot
from src.lib import MintyMusic_lib
import yt_dlp
import discord

client=MintyBot.client
voiceclient=MintyBot.voiceclient
orient = "./music/"

music_count = MintyMusic_lib.music_count
music_filename = ""
music_queue = MintyMusic_lib.music_queue


@client.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await ctx.send("Still Developing")
        await channel.connect()
    else:
        await ctx.send("you're not in Voice Channel")

@client.command()
async def leave(ctx):
	await client.voice_clients[0].disconnect() #Exit from voice channel


@client.command()
async def play(ctx, url):

    title = MintyMusic_lib.sanitize_file_name(await MintyMusic_lib.get_youtube_title(url))
    print(f"sanitized name : {title}")
    title.replace(" / ",".")
    title.replace("#",".")
    print(f"replaced name : {title}")

    if title == "No title":
        await ctx.send("URL is not Correct")
        return  #exit if function can't get title

    if MintyMusic_lib.search_files('music/',title+".mp3") ==True:
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
                        voice.play(discord.FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source=source_1),after=lambda e:MintyMusic_lib.nstart(voice) )
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
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) #voice info

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
