from sqlalchemy import Integer, String, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import Column
import sys, os, mariadb

#MintyBot library
from src import MintyBot
from lib.sqlalchemy_lib.model import ServerInfo
from lib.sqlalchemy_lib import crud, engine

Base = declarative_base()
async_session = None
engine = None
client = MintyBot.client





# ----------------------------------------
# User Table 생성
# ----------------------------------------

class UserTable(Base):  
    __tablename__ = 'minty_server_DB'
    user_id = Column(Integer, primary_key = True, nullable=False)
    user_currency = Column(Integer)
    check_server_id = Column(String[50])
    check_channel_id = Column(String[50])

    

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
    
    async def register(ctx):
        """회원가입 요청"""
        print(f"[MintyCurrency] Registration : {ctx.author.id}")
        await ctx.send(f"[MintyCurrency] {ctx.author.name} 의 회원가입 시작점")

        async with engine.AsyncSessionLocal() as db:
            print("Debug point 1")
            try:
                stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(stmt)
                existance = result.scalar_one_or_none()
                print("Debug point 2")
                if existance is None:
                    await crud.add_user_info(
                        db=db,
                        user_id=ctx.author.id,
                        channel_id=ctx.channel.id,
                        user_balance=100
                    )
                    await ctx.send("회원가입 완료")
                else:
                    await ctx.send("이미 등록된 사용자입니다")

            except Exception as e:
                await db.rollback()
                print(f"[MintyCurrency] Registration failed: {e}")



        

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
    



#def Currency_initialize():
#    global async_session            #for async_session load
#    global engine                   #for engine load
#    print("[MintyCurrency] Currency DB Connection Started")
#    try:
#        engine = create_async_engine(f"""mariadb+asyncmy://
#                                    {os.getenv('MINTYCURRENCY_DB_USER', 'root')}:
#                                    {os.getenv('MINTYCURRENCY_DB_PASSWORD', 'password')}@
#                                    {os.getenv('MINTYCURRENCY_DB_HOST', 'localhost')}:
#                                    {os.getenv('MINTYCURRENCY_DB_PORT','3306')}/
#                                    {os.getenv('MINTYCURRENCY_DB_DATABASE','mintycurrency_db')}""")
#        print("[MintyCurrency] Currency DB Connection Completed")
#    
#    except Exception as e:
#        print(f"Currency initialization failed: {e}")
#        sys.exit(1)
#    
#    async_session = sessionmaker(
#        autocommit = True,
#        autoflush = True,
#        expire_on_commit=False,
#        bind=engine,
#        class_=AsyncSession,
#        )
#    
#    relationship('asyncmy')


        
