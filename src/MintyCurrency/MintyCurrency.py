import mariadb, sys
import os, time
from dotenv import load_dotenv


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

# -----------------------------------
# Connect to MariaDB
# -----------------------------------

def get_currency_db():
    try:
        currency_db = mariadb.connect(
            host= os.getenv("MINTYCURRENCY_DB_HOST", "localhost"),
            user= os.getenv("MINTYCURRENCY_DB_USER", "username"),
            password= os.getenv("MINTYCURRENCY_DB_PASSWORD", "password"),
            database= os.getenv("MINTYCURRENCY_DB_DATABASE", "minty_currency_DB"),
            port= int(os.getenv("MINTYCURRENCY_DB_PORT", 53305)))
        return currency_db
    except mariadb.Error as e:
        print(f"[DB ERROR] Database Connection Failed: {e}")
        sys.exit(1)

def get_currency_cursor():
    conn = get_currency_db()
    return conn.cursor()

class UserCurrency:

    def __init__(self, user_id, balance=0, daily_streak=0, last_daily=None):
        self.id = user_id
        self.balance = balance
        self.daily_streak = daily_streak
        self.last_daily = last_daily
    
    def __repr__(self) -> str:
        """유저 화폐 정보 출력
        args: None
        returns: str
        """
        return f"<UserCurrency {self.id} | Balance:{self.balance} DailyStreak:{self.daily_streak}>"

    def daily_check():
        """출석체크: 1. 출석여부 확인 후 출석체크 & 보너스 지급
        args: None
        returns: None
        """
        conn = get_currency_db()
        cursor = conn.cursor()

    def user_balance_check():
        """유저 잔액 확인
        args: None
        returns: balance(int)
        """

    def user_work():
        """유저 일하기: 1. 일하기 명령어 실행 시 일정 금액 지급
        args: None
        returns: earned_amount(int)
        """
    
    def user_crime():
        """유저 범죄하기: 1. 범죄 명령어 실행 시 성공 시 일정 금액 지급, 실패 시 벌금 차감
        args: None
        returns: result(str), amount(int)
        """

    def user_gamble():
        """유저 도박하기: 1. 도박 명령어 실행 시 일정 금액 베팅 후 결과에 따라 잔액 증감
        args: bet_amount(int)
        returns: result(str), amount(int)
        """
    
    def user_transfer():
        """유저 송금하기: 1. 다른 유저에게 일정 금액 송금
        args: recipient_id(int), transfer_amount(int)
        returns: success(bool)
        """

    def user_leaderboard():
        """유저 랭킹 확인: 1. 잔액 기준 상위 유저들 랭킹 조회
        args: None
        returns: leaderboard(list of tuples)
        """
    

