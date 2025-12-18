from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, session
from sqlalchemy.schema import Column
import sys, os, mariadb, MintyBot

Base = declarative_base()
async_session = None
engine = None
client = MintyBot.client


class SessionContext:
    
    session = None

    def __enter__(self):
        self.session=Session()
        return self.session

    def __exit__(self):
        self.session.close()


# ----------------------------------------
# User Table 생성
# ----------------------------------------

class UserTable(Base):  
    __tablename__ = 'minty_server_DB'
    user_id = Column(Integer, primary_key = True, nullable=False)
    user_currency = Column(Integer)
    check_server_id = Column(String[50])
    check_channel_id = Column(String[50])



                
class MintyCurrency_CRUD():
    def MC_Create_user_profile(client):

                        
        return
    
    def MC_Read_user_profile(client):


        return
    
    def MC_Update_user_profile(client):
  

        return
    
    def MC_Delete_user_profile(client):


        return
    
    

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

#with SessionContext() as session:
#    print("[MintyCurrency] Session Context activated")
    



def Currency_initialize():
    global async_session            #for async_session load
    global engine                   #for engine load
    print("[MintyCurrency] Currency DB Connection Started")
    try:
        engine = create_async_engine(f"""mariadb+asyncmy://
                                    {os.getenv('MINTYCURRENCY_DB_USER', 'root')}:
                                    {os.getenv('MINTYCURRENCY_DB_PASSWORD', 'password')}@
                                    {os.getenv('MINTYCURRENCY_DB_HOST', 'localhost')}:
                                    {os.getenv('MINTYCURRENCY_DB_PORT','3306')}/
                                    {os.getenv('MINTYCURRENCY_DB_DATABASE','mintycurrency_db')}""")
        print("[MintyCurrency] Currency DB Connection Completed")
    
    except Exception as e:
        print(f"Currency initialization failed: {e}")
        sys.exit(1)
    
    async_session = sessionmaker(
        autocommit = True,
        autoflush = True,
        expire_on_commit=False,
        bind=engine,
        class_=AsyncSession,
        )
    
    relationship('asyncmy')


        
