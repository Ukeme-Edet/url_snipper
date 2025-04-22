from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import datetime as dt

from src.utils import generate_url_key

Base = declarative_base()


class Snipper(Base):
    __tablename__ = "snippers"
    id = Column(String, primary_key=True, nullable=False)
    url = Column(String, nullable=False, unique=True, index=True)
    ip = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.now(dt.timezone.utc))
    delete_date = Column(
        DateTime,
        default=lambda: datetime.now(dt.timezone.utc) + timedelta(weeks=8),
    )

    def __init__(self, url: str, ip: str):
        self.id = generate_url_key()
        self.url = url
        self.ip = ip

    def __repr__(self):
        return f"<Snipper(id={self.id!r}, url={self.url!r})>"


engine = create_async_engine("sqlite+aiosqlite:///snippers.db")
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# To create tables asynchronously:
import asyncio


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_models())
