import sys, mariadb
import os, discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from src.MintyHelp import HelpCommands
from gtts import gTTS
import asyncio
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

client = commands.Bot(command_prefix=os.getenv("COMMAND_PREFIX"),intents=discord.Intents.all(), help_command=HelpCommands())
voiceclient=discord.utils.get(client.voice_clients,guild=client.guilds)

# -----------------------------------
# Connect to MariaDB
# -----------------------------------

_MintyBot_conn = None

def get_db():
    """
    Docstring for get_db

    :return: Description
    :rtype: mariadb.Connection  
    """
    global _MintyBot_conn

    if _MintyBot_conn is None:
        print("[MintyBot] Main DB Connection started")
        _MintyBot_conn = mariadb.connect(
            host=os.getenv("MINTYBOT_DB_HOST", "localhost"),
            user=os.getenv("MINTYBOT_DB_USER", "username"),
            password=os.getenv("MINTYBOT_DB_PASSWORD", "password"),
            database=os.getenv("MINTYBOT_DB_DATABASE", "mintybot"),
            port=int(os.getenv("MINTYBOT_DB_PORT", 53305)),
            autocommit=False
        )
        print("[MintyBot] Main DB Connection Completed")

    return _MintyBot_conn


def get_cursor():
    """
    Return a cursor object connected to the main database.

    :return: A cursor object for the main database
    :rtype: mariadb.Cursor
    """
    return get_db().cursor()

def is_channel_enabled(channel_id: int) -> bool:
    """
    Docstring for is_channel_enabled
    
    :param channel_id: Description
    :type channel_id: int
    :return: Description
    :rtype: bool
    """
    cur = get_cursor()
    try:
        cur.execute(
            "SELECT EXISTS(SELECT 1 FROM serverinfo WHERE channel_id = ?)",
            (channel_id,)
        )
        return cur.fetchone()[0] == 1
    finally:
        cur.close()

def is_admin_permisson(ctx) -> bool:
    """
    Docstring for is_admin_permisson

    :param ctx: Description
    :return: Description
    :rtype: bool
    """
    result = ctx.channel.permissions_for(ctx.author).administrator if ctx.guild else 'Direct Message'
    return result



@client.command()
async def tts(ctx, *, text: str):
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        print(f"User is in channel: {voice_channel}")
    else:
        await ctx.send("먼저 음성 채널에 들어가 주세요!")
        return
    
    tts_text = ctx.content[6:].strip()
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
    voice_client = ctx.guild.voice_client

    if voice_client is None or not voice_client.is_connected():
        # 음성 클라이언트가 없거나 연결되어 있지 않으면 새로 연결
        vc = await voice_channel.connect()
    else:
        # 이미 연결되어 있으면 그 연결을 사용
        vc = voice_client

    if ctx.content.endswith("leave"):
        try:        
            await vc.disconnect()
            return
        except Exception as e:
            await ctx.channel.send("음성채널에 연결되어 있지 않습니다")
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
            await ctx.channel.send(f"{voice_channel.name} 채널에는 아무도 없습니다. 음성 채널에 누군가 있을 때 다시 시도하세요!")
            return
        
        if os.path.exists(tts_file):
            os.remove(tts_file)
