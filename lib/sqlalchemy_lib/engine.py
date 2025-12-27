from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from dotenv import load_dotenv
import os 

load_dotenv()

MC_USER=os.getenv("MINTYCURRENCY_DB_USER")
MC_HOST=os.getenv("MINTYCURRENCY_DB_HOST")
MC_PASSWORD=os.getenv("MINTYCURRENCY_DB_PASSWORD")
MC_PORT=os.getenv("MINTYCURRENCY_DB_PORT")
MC_DBNAME=os.getenv("MINTYCURRENCY_DB_DATABASE")

DATABASE_URL = f"mysql+asyncmy://{MC_USER}:{MC_PASSWORD}@{MC_HOST}:{MC_PORT}/{MC_DBNAME}"

# SQLite 예시:
# DATABASE_URL = "sqlite:///./mintybot.db"

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,          # SQL 로그 보고 싶으면 True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


