from config import PICKUP_BOT_TOKEN, DEBUG
import logging
from aiogram import Bot, Dispatcher
import asyncio
from config import engine
from models.models import create_all_tables
from app_company.handlers.company_handlers import company_reg_router, category_router, product_router
from app_company.handlers.admin_handlers import admin_company_router


async def main():
    await create_all_tables(engine)
    dp = Dispatcher()
    bot = Bot(token=PICKUP_BOT_TOKEN)

    dp.include_router(admin_company_router)
    dp.include_router(company_reg_router)
    dp.include_router(category_router)
    dp.include_router(product_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    if DEBUG:
        logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
