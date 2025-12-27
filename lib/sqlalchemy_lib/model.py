from sqlalchemy import Column, Integer, BigInteger, String, DateTime, func, Date
from sqlalchemy.orm import declarative_base
from datetime import date, datetime

Base = declarative_base()

class ServerInfo(Base):
    """
    user_id = Integer
    channel_id = BigInteger
    user_balance= BigInteger
    last_login = DateTime
    user_daily_streak = Integer
    last_work = DateTime
    last_crime = DateTime
    """
    __tablename__ = "serverinfo"

    user_id = Column(BigInteger, unique=True, primary_key=True, index=True)
    #channel_id = Column(BigInteger, unique=False, nullable=False)
    user_balance = Column(BigInteger, unique= False, nullable = False)
    last_login = Column(Date, default=date.today)
    user_daily_streak = Column(Integer, default=0)
    last_work = Column(DateTime, default=datetime.now)
    last_crime = Column(DateTime, default=datetime.now)
    user_name = Column(String, unique=False, nullable=False)

class ServerShopInfo(Base):
    """
    item_id = Integer
    item_name = String
    item_price = BigInteger
    item_description = String
    """
    __tablename__ = "servershopinfo"

    item_id = Column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    item_name = Column(String, unique=False, nullable=False)
    item_price = Column(BigInteger, unique=False, nullable=False)
    item_description = Column(String, unique=False, nullable=False)