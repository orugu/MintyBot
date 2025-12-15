import mariadb
import sys
import mintyrank.rank as rank




async def rank_process(message):
    # 봇 메시지 무시
    if message.author.bot:
            return
    
    try:
        # DB에서 유저 가져오기 (없으면 생성)
        user = rank.RankDB.get_user(message.author)

        # 경험치 추가
        user.add_experience(message.content)
        user.exp_check(message)
        # 레벨업 메시지 전송
        await user.level_up_message(message)        

        # DB 저장
        rank.RankDB.save_user(user)

        # 결과 출력 (test)
        print(f"{message.content}, {len(str(message.content))}, {user.nickname}")
        print(f"[RANK] {user.nickname} | LV:{user.level} EXP:{user.experience}/{user.max_experience}")

    except Exception as e:
        print(f"[RANK ERROR] Rank Processing Failed: {e}")


