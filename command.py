from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from config import DATABASE_URL, AsyncSessionLocal
from models.models import Base, Company


async def delete_tables():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()



async def delete_obj(model, obj_id):
    async with AsyncSessionLocal() as session:
        obj = await session.get(model, obj_id)
        await session.delete(obj)
        await session.commit()

asyncio.run(delete_obj(Company, 1))