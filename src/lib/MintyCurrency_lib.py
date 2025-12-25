from sqlalchemy import Integer, String, func, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import Column
import sys, os, mariadb
from datetime import date, datetime

#MintyBot library
from src import MintyBot
from lib.sqlalchemy_lib.model import ServerInfo, Base
from lib.sqlalchemy_lib import crud, engine,model
from lib.sqlalchemy_lib.engine import AsyncSessionLocal



client = MintyBot.client



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
    
    @staticmethod
    async def register(ctx):
        """회원가입 요청"""
        print(f"[MintyCurrency] Registration : {ctx.author.id}")
        await ctx.send(f"[MintyCurrency] {ctx.author.name} 의 회원가입 시작점")

        async with AsyncSessionLocal() as db:
            print(f"[MintyCurrency] Registration DB Session Opened : {ctx.author.id}")
            try:
                stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(stmt)
                user = result.scalars().first()
                print(f"[MintyCurrency] Registration User Query Executed : {ctx.author.id}")
            except Exception as e:
                print(f"[MintyCurrency] Registration User Query Failed : {ctx.author.id}, Error: {e}")
                await ctx.send("회원가입 중 오류가 발생했습니다. 다시 시도해주세요.")
                return
            try:
                if user is None:
                    new_user = ServerInfo(
                        user_id=ctx.author.id,
                        channel_id=ctx.channel.id,
                        user_balance=1000,  #가입 보너스
                        last_login = str(date.today()),
                        user_daily_streak=0   
                    )

                    print(f"[MintyCurrency] New user creating : {ctx.author.id}, {ctx.author.name}")
                    db.add(new_user)
                    await db.commit()
                    print(f"[MintyCurrency] New user registered: {ctx.author.id}, {ctx.author.name}")
                    await ctx.send("회원가입 완료")
                    return True
                else:
                    print(f"[MintyCurrency] User already registered: {ctx.author.id}, {ctx.author.name}")
                    await ctx.send("이미 등록된 사용자입니다")
                    return False
            except Exception as e:
                print(f"[MintyCurrency] Registration Failed : {ctx.author.id}, Error: {e}")
                await ctx.send("회원가입 중 오류가 발생했습니다. 다시 시도해주세요.")
                return False    
        print(f"[MintyCurrency] Registration DB Session Closed : {ctx.author.id}")

    
    async def daily_check(ctx):
        """출석체크: 1. 출석여부 확인 후 출석체크 & 보너스 지급
        args: None
        returns: None
        """
        print(f"[MintyCurrency] Daily Check : {ctx.author.id}")
        await ctx.send(f"[MintyCurrency] {ctx.author.name} 의 출석체크 시작점")
        async with AsyncSessionLocal() as db:
            print(f"[MintyCurrency] Daily Check DB Session Opened : {ctx.author.id}")
            stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
            result = await db.execute(stmt)
            print(f"[MintyCurrency] Daily Check User Query Executed : {ctx.author.id}")
            user = result.scalar_one_or_none()
            
            if user is None:
                print(f"[MintyCurrency] User not registered: {ctx.author.id}, {ctx.author.name}")
                await ctx.send("회원가입이 필요합니다. !register 명령어를 사용해주세요.")
                return

            # 출석체크 로직 구현 (예: 마지막 출석일과 비교 등)
            else:
                print(f"[MintyCurrency] User found for Daily Check: {ctx.author.id}, {ctx.author.name}")
                last_login=select(ServerInfo.last_login).where(ServerInfo.user_id == ctx.author.id)
                today = date.today()

                if last_login != today:
                    user.last_login = today
                    user.daily_streak += 1
                    user.user_balance += 1000*user.daily_streak  # 출석 보너스 지급
                    print(f"""[MintyCurrency] User has been daily checked :
                           user id: {user.daily_streak}
                           last login: {user.last_login}
                           daily streak: {user.daily_streak}""")
                    await ctx.send(f"출석체크 완료! 현재 출석일수: {user.daily_streak}")
                else:
                    await ctx.send("이미 오늘 출석체크를 하셨습니다.")
                    return

            await db.commit()

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

    def Currency_process(message):
        """화폐 관련 명령어 처리
        args: message(discord.Message)
        returns: None
        """

        pass



        
