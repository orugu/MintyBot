import yt_dlp, os
import discord
from src import MintyBot
#music mp3 defines
client = MintyBot.client

music_queue = []  # 재생 대기열을 관리할 리스트
title_list =[] #제목 리스트

music_count = 1
repeat_Flag = 0

def sanitize_file_name(file_name):
    # 슬래시를 언더스코어로 대체하고, 특수 문자는 제거
    file_name = file_name.replace("/", "_")
    return file_name

def search_files(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            print(f"파일 발견: {os.path.join(root, filename)}")
            return True
        else:
            return False
        
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


async def on_voice_state_update(member, before, after):
    # 음성 채널에 접속하거나 음성 채널에 변경 사항이 있을 때 호출됩니다.

    # 노래가 끝났을 때 실행되는 함수x
    print("노래가 끝났습니다.")
    # 추가 작업을 여기에 정의할 수 있습니다.
    await member.send("노래가 끝났습니다!")