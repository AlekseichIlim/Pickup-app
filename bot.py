from config import PICKUP_BOT_TOKEN, DEBUG
import logging
from aiogram import Bot, Dispatcher
import asyncio

from app_company.handlers.company_handlers import company_router


async def main():
    dp = Dispatcher()
    bot = Bot(token=PICKUP_BOT_TOKEN)

    # dp.include_router(admin_router)
    dp.include_router(company_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    if DEBUG:
        logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
