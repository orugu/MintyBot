import asyncio
from . import engine
from .model import Base

async def init_db():
    async with engine.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("[MintyCurrency] Database initialized")

