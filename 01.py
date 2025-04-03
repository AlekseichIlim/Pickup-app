from io import BytesIO

from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from storage import ObjectStorage

from config import PICKUP_BOT_TOKEN, DEBUG, engine, AsyncSessionLocal
import logging, uuid
from aiogram import Bot, Dispatcher, F, Router
import asyncio
from app_company.handlers.company_handlers import company_reg_router, menu_router
import app_company.keyboards.company_keyboards as company_kb
from models.models import create_all_tables, Image

router = Router()
bot = Bot(token='7056943338:AAEyq5m3NcEs7BZiodjyPTvMOQ5GfrYd700')

load_dotenv()

storage = ObjectStorage()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Отправь фото')


@router.message(F.photo)
async def get_photo(message: Message):
    file = await bot.get_file(message.photo[-1].file_id)
    file_data = BytesIO()
    await bot.download_file(file.file_path, file_data)

    file_name = f'images/{uuid.uuid4()}.jpg'

    image_url = await storage.upload_file(file_data, file_name)

    async with AsyncSessionLocal() as session:
        session.add(Image(name=file_name, url=image_url))
        await session.commit()
    await message.answer(f'Изображение сохранено! {image_url.split('/')[-1].split('.')[0]}')



async def main():
    await create_all_tables(engine)
    await storage.test_connection()
    dp = Dispatcher()
    bot = Bot(token='7056943338:AAEyq5m3NcEs7BZiodjyPTvMOQ5GfrYd700')

    # dp.include_router(admin_router)
    dp.include_router(router)
    dp.include_router(menu_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    if DEBUG:
        logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
