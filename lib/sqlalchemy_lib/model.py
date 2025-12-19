from sqlalchemy import Column, Integer, BigInteger, String, DateTime, func
from .engine import Base

class ServerInfo(Base):
    __tablename__ = "serverinfo"

    user_id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(BigInteger, unique=True, nullable=False)
    user_balance = Column(BigInteger, unique= True, nullable = False)
    last_login = Column(DateTime, server_default=func.now())
    
