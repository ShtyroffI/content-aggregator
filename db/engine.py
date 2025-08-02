import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DATABASE_URL')

if not db_url:
    raise ValueError("Переменная окружения DATABASE_URL не установлена!")

engine = create_async_engine(db_url, echo=True)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)