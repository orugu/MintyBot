from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = f"mysql+pymysql://user:password@localhost:3306/mintybot"

# SQLite 예시:
# DATABASE_URL = "sqlite:///./mintybot.db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,          # SQL 로그 보고 싶으면 True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
