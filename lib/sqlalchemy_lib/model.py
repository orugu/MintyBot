from sqlalchemy import Column, Integer, BigInteger, String, DateTime, func
from .engine import Base

class ServerInfo(Base):
    __tablename__ = "serverinfo"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(BigInteger, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
