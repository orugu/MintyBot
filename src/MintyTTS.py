import MintyBot
from src.lib import MintyTTS_lib    
from gtts import gTTS
import discord,asyncio
#Todo: TTS Function must be loaded with @client.command()
#Todo: There is a bug in TTS function. Must be fixed

async def tts(message):
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