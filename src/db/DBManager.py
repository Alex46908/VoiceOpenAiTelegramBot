from sqlalchemy import select, update, insert
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db.models.UserValuesModel import UserValuesModel

class DBManager:
    def __init__(self, user, password, host, port, db):
        self.url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
        self.engine = None
        self.async_session = None

    async def connect(self):
        engine = create_async_engine(self.url, poolclass=AsyncAdaptedQueuePool, echo=True)
        self.engine = engine
        self.async_session = async_sessionmaker(engine, expire_on_commit=False)

    async def find_values(self, telegram_id):
        res = None
        async with self.async_session() as session:
            res = await session.execute(select(UserValuesModel).where(UserValuesModel.telegram_id == telegram_id).limit(1))

        return res.scalars().first()

    async def update_values(self, telegram_id, old_values, new_value):
        values = str(old_values) + "," + new_value
        async with self.async_session() as session:
            await session.execute(update(UserValuesModel).where(UserValuesModel.telegram_id == telegram_id).values(values=values))
            await session.commit()

    async def insert_values(self, telegram_id, values):
        async with self.async_session() as session:
            await session.execute(insert(UserValuesModel).values(telegram_id=telegram_id, values=values))
            await session.commit()