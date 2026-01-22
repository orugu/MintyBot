import MGPT2.MGPT2_generation as gen
import MGPT2.MGPT2_question as quest




class MGPT2:
    async def load_full_model():                  #모듈 전체 로딩
        gen.DiscordGPT2Bot.load_gen_model("distilgpt2")
        quest.load_quest_model()

    async def MGPT_generation(message,text):     #문장 생성 함수
        try:
            await gen.DiscordGPT2Bot.gen_handle_message(message,text)
        except Exception as e:
            await message.channel.send(f'문장생성 에러 발생: {str(e)}')
            
    async def MGPT_question(message,text):
        try:
            await quest.quest_handle_message(message,text)
        except Exception as e:
            await message.channel.send(f'질의응답 에러 발생: {str(e)}')

