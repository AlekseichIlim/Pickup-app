import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

ADMINS = [1892638646, ]

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
PICKUP_BOT_TOKEN = os.getenv("PICKUP_BOT_TOKEN")

DEBUG = True

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
