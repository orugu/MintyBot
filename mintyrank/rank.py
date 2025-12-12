import mariadb
import sys
from dotenv import load_dotenv
import os
# -----------------------------------
# .env config load
# add to .env
#
# MINTYRANK_HOST="your ip or address"
# MINTYRANK_PORT="your port"
# MINTYRANK_USER="your user"
# MINTYRANK_PASSWORD="your password"
# MINTYRANK_DATABASE="your database"
# -----------------------------------

load_dotenv()

# -----------------------------------
# Connect to MariaDB
# -----------------------------------
def get_db() -> mariadb.Connection:
    try:
        conn = mariadb.connect(
            host= os.getenv("MINTYRANK_HOST", "localhost"),
            user= os.getenv("MINTYRANK_USER", "orugu"),
            password= os.getenv("MINTYRANK_PASSWORD", "jys0713"),
            database= os.getenv("MINTYRANK_DATABASE", "mintyrank"),
            port= int(os.getenv("MINTYRANK_PORT", "53305"))
        )
        return conn

    except mariadb.Error as e:
        print(f"[DB ERROR] Database Connection Failed: {e}")
        sys.exit(1)

#rank test profile 
class MockMember:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name


# -----------------------------------
# 유저 랭크 데이터 오브젝트
#User Rank Profile
# -----------------------------------
class UserRank:
    def __init__(self, user_id, nickname, level=1, exp=0, max_exp=100):
        self.id = user_id
        self.nickname = nickname
        self.level = level
        self.experience = exp
        self.max_experience = max_exp
        self.toggle_levelup_message = False  #레벨업 메시지 토글 기본값은 켜짐

    def add_experience(self, text: str):
        self.experience += len(text)

    def exp_check(self, message):
        if self.experience >= self.max_experience:
            self.experience -= self.max_experience
            self.level += 1 
            self.max_experience = int(self.max_experience * (1.2)**self.level)
            self.toggle_levelup_message = True  #레벨업 메시지 토글 켜기

    async def level_up_message(self, message):
        if self.toggle_levelup_message:
            self.toggle_levelup_message = False  #레벨업 메시지 토글 끄기
            await message.channel.send(f"축하합니다, {self.nickname}님! 레벨 {self.level}로 상승하셨습니다! 🎉")
    
    def remove_experience(self, amount):
        self.experience = max(0, self.experience - amount)

    def __repr__(self):
        return f"<UserRank {self.nickname} | LV:{self.level} EXP:{self.experience}/{self.max_experience}>"


# -----------------------------------
# MariaDB 를 이용한 Rank Manager
# -----------------------------------
class RankDB:

    # 유저 가져오기 (없으면 생성)
    @staticmethod
    def get_user(member):
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT user_id, nickname, level, experience, max_experience FROM user_rank WHERE user_id = ?",
                    (member.id,))

        row = cur.fetchone()

        # 신규 유저인 경우 DB에 추가
        if row is None:
            cur.execute(
                "INSERT INTO user_rank (user_id, nickname) VALUES (?, ?)",
                (member.id, member.name)
            )
            conn.commit()
            conn.close()
            return UserRank(member.id, member.name)

        conn.close()

        return UserRank(
            user_id=row[0],
            nickname=row[1],
            level=row[2],
            exp=row[3],
            max_exp=row[4]
        )

    # 저장 (UPDATE)
    @staticmethod
    def save_user(user: UserRank):
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            UPDATE user_rank
            SET nickname=?, level=?, experience=?, max_experience=?
            WHERE user_id=?
        """, (user.nickname, user.level, user.experience, user.max_experience, user.id))

        conn.commit()
        conn.close()

    # 경험치 추가 처리
    @staticmethod
    def add_exp(member, text):
        user = RankDB.get_user(member)

        user.add_experience(text)
        user.exp_check()

        RankDB.save_user(user)

        return user


# -----------------------------------
# 오류 메시지
# -----------------------------------
class RankErrorHandler:
    @staticmethod
    async def check_data_fail(message):
        await message.channel.send("랭크 데이터 오류 발생 — 관리자에게 문의하세요.")
