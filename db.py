import asyncio
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_async_engine("sqlite+aiosqlite:///requests.db", future=True, echo=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    cadastre_number = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    response = Column(Boolean)
    create_date = Column(DateTime)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_database():
    await create_tables()


async def main():
    await create_database()

if __name__ == "__main__":
    asyncio.run(main())