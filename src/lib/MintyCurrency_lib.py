from sqlalchemy import func, select
import random
from datetime import date, datetime, timedelta

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
        print(f"[MintyCurrency] Registration Started : {ctx.author.id}")

        async with AsyncSessionLocal() as db:
            print(f"[MintyCurrency] Registration DB Session Opened : {ctx.author.id}")
            try:
                stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(stmt)
                user = result.scalars().first()
                print(f"[MintyCurrency] Registration User Query Executed : {ctx.author.id}")
            except Exception as e:
                print(f"[MintyCurrency] Registration User Query Failed : {ctx.author.id}, Error: {e}")
                await ctx.send("[MintyCurrency] 회원가입 중 오류가 발생했습니다. 관리자에게 문의해주세요.")
                return
            try:
                if user is None:
                    new_user = ServerInfo(
                        user_id=ctx.author.id,
                        user_name=ctx.author.name,
                        user_balance=1000  
                    )

                    print(f"[MintyCurrency] New user creating : {ctx.author.id}, {ctx.author.name}")
                    db.add(new_user)
                    await db.commit()
                    print(f"[MintyCurrency] New user registered: {ctx.author.id}, {ctx.author.name}")
                    await ctx.send("[MintyCurrency] 회원가입 완료")
                    return True
                else:
                    print(f"[MintyCurrency] User already registered: {ctx.author.id}, {ctx.author.name}")
                    await ctx.send("[MintyCurrency] 이미 등록된 사용자입니다")
                    return False
            except Exception as e:
                print(f"[MintyCurrency] Registration Failed : {ctx.author.id}, Error: {e}")
                await ctx.send("[MintyCurrency] 회원가입 중 오류가 발생했습니다. 관리자에게 문의해주세요.")
                return False    
        print(f"[MintyCurrency] Registration DB Session Closed : {ctx.author.id}")

    
    async def daily_check(ctx):
        """출석체크: 1. 출석여부 확인 후 출석체크 & 보너스 지급
        args: ctx(discord.Context)
        returns: None
        """
        print(f"[MintyCurrency] Daily Check : {ctx.author.id}")
        async with AsyncSessionLocal() as db:
            print(f"[MintyCurrency] Daily Check DB Session Opened : {ctx.author.id}")
            try:
                stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(stmt)
                user = result.scalars().first()
                
            except Exception as e:
                print(f"[MintyCurrency] Daily Check User Query Failed : {ctx.author.id}, Error: {e}")
                await ctx.send("[MintyCurrency] 출석체크 중 오류가 발생했습니다. 관리자에게 문의해주세요.")
                return
            
            if user is None:
                print(f"[MintyCurrency] User not registered: {ctx.author.id}, {ctx.author.name}")
                await ctx.send("[MintyCurrency] 회원가입이 필요합니다. !register 명령어를 사용해주세요.")
                return

            # 출석체크 로직 구현 (예: 마지막 출석일과 비교 등)
            else:
                print(f"[MintyCurrency] User found for Daily Check: {ctx.author.id}, {ctx.author.name}")
                today = date.today()
                
                last_login=select(ServerInfo.last_login).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(last_login)
                last_login_date = result.scalars().first()
                print(f"[MintyCurrency] Last login date: {last_login_date}, Today: {today}")

                if last_login_date != today:
                    try:
                        user.last_login = today
                        user.user_daily_streak += 1
                        user.user_balance += 1000*user.user_daily_streak  # 출석 보너스 지급
                        print(f"""[MintyCurrency] User has been daily checked :
                            user id: {user.user_id}
                            last login: {user.last_login}
                            daily streak: {user.user_daily_streak}""")
                        await db.commit()
                        await ctx.send(f"출석체크 완료! 현재 출석일수: {user.user_daily_streak}")
                    except Exception as e:
                        print(f"[MintyCurrency] Daily Check Update Failed : {ctx.author.id}, Error: {e}")
                        await ctx.send("[MintyCurrency] 출석체크 중 오류가 발생했습니다. 관리자에게 문의해주세요.")
                        return

                else:
                    await ctx.send("이미 오늘 출석체크를 하셨습니다.")
                    return

            

    async def user_balance_check(ctx):
        """유저 잔액 확인
        args: ctx(discord.Context)
        returns: balance(int)
        """
        print(f"[MintyCurrency] Money Check : {ctx.author.id}")
        async with AsyncSessionLocal() as db:
            print(f"[MintyCurrency] Money Check DB Session Opened : {ctx.author.id}")
            try:
                stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(stmt)
                user = result.scalars().first()
                
            except Exception as e:
                print(f"[MintyCurrency] Daily Check User Query Failed : {ctx.author.id}, Error: {e}")
                await ctx.send("[MintyCurrency] 오류가 발생했습니다. 관리자에게 문의해주세요.")
                return
            
            if user is None:
                print(f"[MintyCurrency] User not registered: {ctx.author.id}, {ctx.author.name}")
                await ctx.send("[MintyCurrency] 회원가입이 필요합니다. !register 명령어를 사용해주세요.")
                return

            # 돈 체크 로직 구현 (예: 마지막 출석일과 비교 등)
            else:
                print(f"[MintyCurrency] User found for Money Check: {ctx.author.id}, {ctx.author.name}")
                
                money=select(ServerInfo.user_balance).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(money)
                user_balance = result.scalars().first()
                print(f"[MintyCurrency] User balance: {user_balance}")

                if user_balance is not None:
                    await ctx.send(f"현재 잔액: {user_balance}")
                    print(f"""[MintyCurrency] User has been money checked :
                    user id: {user.user_id}
                    balance: {user.user_balance}""")
                else:
                    await ctx.send("잔액을 불러오는 중 오류가 발생했습니다.")
                    return


    async def user_work(ctx):
        """유저 일하기: 1. 일하기 명령어 실행 시 일정 금액 지급
        2. 일정 시간 간격으로만 실행 가능 #todo
        args: ctx(discord.Context)
        returns: earned_amount(int)
        """
        async with AsyncSessionLocal() as db:
            print(f"[MintyCurrency] Money Check DB Session Opened : {ctx.author.id}")
            try:
                stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(stmt)
                user = result.scalars().first()
                
            except Exception as e:
                print(f"[MintyCurrency] Daily Check User Query Failed : {ctx.author.id}, Error: {e}")
                await ctx.send("[MintyCurrency] 오류가 발생했습니다. 관리자에게 문의해주세요.")
                return
            
            if user is None:
                print(f"[MintyCurrency] User not registered: {ctx.author.id}, {ctx.author.name}")
                await ctx.send("[MintyCurrency] 회원가입이 필요합니다. !register 명령어를 사용해주세요.")
                return
            # 일하기 로직 구현
            else:
                print(f"[MintyCurrency] User found for Work: {ctx.author.id}, {ctx.author.name}")
                try:
                    stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                    result = await db.execute(stmt)
                    user = result.scalars().first()
                    
                    if user.last_work is not None:
                        elapsed = datetime.now() - user.last_work
                        if elapsed < timedelta(minutes=5):  # 5분이 지나지 않았으면
                            await ctx.send("[MintyCurrency] 이미 돈을 받은 적이 있습니다. 5분 후에 다시 시도해주세요.")
                            return
                        else:
                            earned_amount = random.randint(100, 500)
                            user.user_balance += earned_amount   # ORM 객체 필드 수정
                            user.last_work = datetime.now()
                            await db.commit()
                            await ctx.send(f"[MintyCurrency] {ctx.author.name}님이 {earned_amount}Minty를 받았습니다.")
                    else:
                        earned_amount = random.randint(1000, 5000)
                        user.user_balance += earned_amount   # ORM 객체 필드 수정
                        user.last_work = datetime.now()
                        await db.commit()
                        await ctx.send(f"[MintyCurrency] {ctx.author.name}님이 처음으로 {earned_amount}Minty를 받았습니다!")

                except Exception as e:
                    print(f"[MintyCurrency] User Work Failed : {ctx.author.id}, Error: {e}")
                    await ctx.send("[MintyCurrency] 돈 받기 중 오류가 발생했습니다. 관리자에게 문의해주세요.")
                    return

    async def user_crime(ctx):
        """유저 범죄하기: 1. 범죄 명령어 실행 시 성공 시 일정 금액 지급, 실패 시 벌금 차감
        args: ctx(discord.Context)
        returns: result(str), amount(int)
        """
        async with AsyncSessionLocal() as db:
            print(f"[MintyCurrency] Crime check DB Session Opened : {ctx.author.id}")
            try:
                stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(stmt)
                user = result.scalars().first()
                
            except Exception as e:
                print(f"[MintyCurrency] Crime Check User Query Failed : {ctx.author.id}, Error: {e}")
                await ctx.send("[MintyCurrency] 오류가 발생했습니다. 관리자에게 문의해주세요.")
                return
            
            if user is None:
                print(f"[MintyCurrency] User not registered: {ctx.author.id}, {ctx.author.name}")
                await ctx.send("[MintyCurrency] 회원가입이 필요합니다. !register 명령어를 사용해주세요.")
                return
            # 범죄하기 로직 구현
            else:
                print(f"[MintyCurrency] User found for Crime: {ctx.author.id}, {ctx.author.name}")
                try:
                    stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                    result = await db.execute(stmt)
                    user = result.scalars().first()
                    
                    if user.last_crime is not None:
                        elapsed = datetime.now() - user.last_crime
                        if elapsed < timedelta(minutes=5):  # 5분이 지나지 않았으면
                            await ctx.send("[MintyCurrency] 이미 강탈한 적이 있습니다. 5분 후에 다시 시도해주세요.")
                            return
                        else:
                            win_chance = random.random()
                            if win_chance < 0.3:  # 30% 확률로 실패
                                fine_amount = random.randint(100, 300)
                                user.user_balance -= fine_amount   # ORM 객체 필드 수정
                                user.last_crime = datetime.now()
                                await db.commit()
                                await ctx.send(f"[MintyCurrency] {ctx.author.name}님이 강탈에 실패하여 {fine_amount}원의 벌금을 냈습니다.")
                                return
                            else:
                                earned_amount = random.randint(100, 500)
                                user.user_balance += earned_amount   # ORM 객체 필드 수정
                                user.last_crime = datetime.now()
                                await db.commit()
                                await ctx.send(f"[MintyCurrency] {ctx.author.name}님이 강탈을 저질러 {earned_amount}원을 벌었습니다.")
                    else:
                        earned_amount = random.randint(1000, 5000)
                        user.user_balance += earned_amount   # ORM 객체 필드 수정
                        user.last_crime = datetime.now()
                        await db.commit()
                        await ctx.send(f"[MintyCurrency] {ctx.author.name}님이 처음으로 강탈을 저질러 {earned_amount}원을 벌었습니다!")

                except Exception as e:
                    print(f"[MintyCurrency] User Work Failed : {ctx.author.id}, Error: {e}")
                    await ctx.send("[MintyCurrency] 강탈을 저지르던 중 오류가 발생했습니다. 관리자에게 문의해주세요.")
                    return
                
    def user_gamble():
        """유저 도박하기: 1. 도박 명령어 실행 시 일정 금액 베팅 후 결과에 따라 잔액 증감
        args: bet_amount(int)
        returns: result(str), amount(int)
        """


    async def user_transfer(ctx):
        """유저 송금하기: 1. 다른 유저에게 일정 금액 송금
        args: recipient_id(int), transfer_amount(int)
        returns: success(bool)
        """
        async with AsyncSessionLocal() as db:
            print(f"[MintyCurrency] Crime check DB Session Opened : {ctx.author.id}")
            try:
                stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(stmt)
                user = result.scalars().first()
                
            except Exception as e:
                print(f"[MintyCurrency] Crime Check User Query Failed : {ctx.author.id}, Error: {e}")
                await ctx.send("[MintyCurrency] 오류가 발생했습니다. 관리자에게 문의해주세요.")
                return
            
            if user is None:
                print(f"[MintyCurrency] User not registered: {ctx.author.id}, {ctx.author.name}")
                await ctx.send("[MintyCurrency] 회원가입이 필요합니다. !register 명령어를 사용해주세요.")
                return
            
            else:
                print(f"[MintyCurrency] User found for Transfer: {ctx.author.id}, {ctx.author.name}")
                # 송금 로직 구현
                if len(ctx.message.mentions) == 0:
                    await ctx.send("[MintyCurrency] 송금할 유저를 멘션해주세요.")
                    return
                else:
                    recipient = ctx.message.mentions[0]
                    try:
                        transfer_amount = int(ctx.message.content.split()[2])
                    except (IndexError, ValueError):
                        await ctx.send("[MintyCurrency] 올바른 금액을 입력해주세요.")
                        return

                    if transfer_amount <= 0:
                        await ctx.send("[MintyCurrency] 송금 금액은 0보다 커야 합니다.")
                        return

                    if user.user_balance < transfer_amount:
                        await ctx.send("[MintyCurrency] 잔액이 부족합니다.")
                        return

                    try:
                        stmt = select(ServerInfo).where(ServerInfo.user_id == recipient.id)
                        result = await db.execute(stmt)
                        recipient_user = result.scalars().first()

                        if recipient_user is None:
                            await ctx.send("[MintyCurrency] 수신자가 회원가입되어 있지 않습니다.")
                            return

                        user.user_balance -= transfer_amount
                        recipient_user.user_balance += transfer_amount
                        await db.commit()
                        await ctx.send(f"[MintyCurrency] {ctx.author.name}님이 {recipient.name}님에게 {transfer_amount}원을 송금했습니다.")

                    except Exception as e:
                        print(f"[MintyCurrency] User Transfer Failed : {ctx.author.id}, Error: {e}")
                        await ctx.send("[MintyCurrency] 송금 중 오류가 발생했습니다. 관리자에게 문의해주세요.")
                        return
        

    async def user_leaderboard(ctx):
        """유저 랭킹 확인: 1. 잔액 기준 상위 유저들 랭킹 조회
        args: None
        returns: leaderboard(list of tuples)
        """
        async with AsyncSessionLocal() as db:
            print(f"[MintyCurrency] Crime check DB Session Opened : {ctx.author.id}")
            try:
                stmt = select(ServerInfo).where(ServerInfo.user_id == ctx.author.id)
                result = await db.execute(stmt)
                user = result.scalars().first()
                
            except Exception as e:
                print(f"[MintyCurrency] Crime Check User Query Failed : {ctx.author.id}, Error: {e}")
                await ctx.send("[MintyCurrency] 오류가 발생했습니다. 관리자에게 문의해주세요.")
                return
            
            if user is None:
                print(f"[MintyCurrency] User not registered: {ctx.author.id}, {ctx.author.name}")
                await ctx.send("[MintyCurrency] 회원가입이 필요합니다. !register 명령어를 사용해주세요.")
                return
            else:
                print(f"[MintyCurrency] User found for Leaderboard: {ctx.author.id}, {ctx.author.name}")
                try:
                    stmt = select(ServerInfo).order_by(ServerInfo.user_balance.desc()).limit(10)
                    result = await db.execute(stmt)
                    top_users = result.scalars().all()

                    leaderboard_message = "[MintyCurrency] 잔액 기준 상위 10명 랭킹:\n"
                    for rank, usr in enumerate(top_users, start=1):
                        leaderboard_message += f"{rank}. User ID: {usr.user_name}, Balance: {usr.user_balance}\n"

                    await ctx.send(leaderboard_message)

                except Exception as e:
                    print(f"[MintyCurrency] User Leaderboard Failed : {ctx.author.id}, Error: {e}")
                    await ctx.send("[MintyCurrency] 랭킹 조회 중 오류가 발생했습니다. 관리자에게 문의해주세요.")
                    return

    async def Currency_process(message):
        """화폐 관련 명령어 처리
        args: message(discord.Message)
        returns: None
        """

        pass



        
