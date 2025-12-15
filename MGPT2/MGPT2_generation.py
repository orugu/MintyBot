from transformers import GPT2LMHeadModel
from transformers import GPT2Tokenizer
import discord, asyncio
from transformers import pipeline
import os
from gtts import gTTS
import torch
import transformers
transformers.utils.import_utils._torchvision_available = False
# Discord 봇 상태 관리 클래스
class DiscordGPT2Bot:
    tokenizer_textgen = None
    model_textgen = None
    tts_file = "GPTtts/tts.mp3"  # TTS 파일 저장 경로

        
    def load_gen_model(type):
        """GPT-2 모델과 토크나이저 로드"""
        global tokenizer, model, device
        tokenizer = GPT2Tokenizer.from_pretrained(type, cache_dir="/tmp/hf_cache")
        model = GPT2LMHeadModel.from_pretrained(type, cache_dir="/tmp/hf_cache")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        print("GPT-2 문장생성 모델이 성공적으로 로드되었습니다.")

    async def gen_handle_message(message, text):
        """GPT-2와 TTS 처리"""
        global tokenizer,model,device
        if not tokenizer or not model:
            await message.channel.send("GPT-2가 초기화되지 않았습니다. 관리자에게 문의하세요.")
            return

        # TTS 플래그 설정
        tts_flag = "-voice" in text
        if tts_flag:
            text = text.replace("-voice", "").strip()

        # 텍스트 생성
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0)
        output = pipe(text, max_length=60, truncation=True)
        generated_text = output[0]['generated_text']
        await message.channel.send(generated_text)

        # TTS 처리
        if tts_flag:
            await DiscordGPT2Bot.handle_tts(message, generated_text)

    #tts code
    async def handle_tts(message, text):
        """TTS 처리 및 음성 채널 재생"""
        tts_text = message.content[6:].strip()
        print(f"Received TTS request: {tts_text}")
        if tts_text[0].encode("utf-8").isalpha():
            langstatus = "en"
        else:
            langstatus = "ko"
        print(langstatus)
        tts = gTTS(text, lang= langstatus)
        tts.save(DiscordGPT2Bot.tts_file)

        if not message.author.voice or not message.author.voice.channel:
            await message.channel.send("먼저 음성 채널에 들어가 주세요!")
            return

        voice_channel = message.author.voice.channel
        vc = message.guild.voice_client

        if not vc or not vc.is_connected():
            vc = await voice_channel.connect()

        try:
            vc.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source=DiscordGPT2Bot.tts_file))
            while vc.is_playing():
                await asyncio.sleep(1)
        except Exception as e:
            await message.channel.send(f"오디오 재생 중 오류가 발생했습니다: {e}")
        finally:
            if os.path.exists(DiscordGPT2Bot.tts_file):
                os.remove(DiscordGPT2Bot.tts_file)

            if len(voice_channel.members) == 1:  # 봇만 남아있다면
                await vc.disconnect()
