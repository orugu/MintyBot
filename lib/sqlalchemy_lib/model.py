from sqlalchemy import Column, Integer, BigInteger, String, DateTime, func
from sqlalchemy.orm import declarative_base
from datetime import date

Base = declarative_base()

class ServerInfo(Base):
    """
    user_id = Integer
    channel_id = BigInteger
    user_balance= BigInteger
    last_login = DateTime
    """
    __tablename__ = "serverinfo"

    user_id = Column(BigInteger, unique=True, primary_key=True, index=True)
    channel_id = Column(BigInteger, unique=True, nullable=False)
    user_balance = Column(BigInteger, unique= False, nullable = False)
    last_login = Column(String, server_default=str(date.today()))
    user_daily_streak = Column(Integer, default=0)
