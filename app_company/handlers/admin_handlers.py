from aiogram.filters import CommandStart
from aiogram.types import Message
from app_company.filtetrs.admin_filter import IsAdminFilter
from aiogram import Router

admin_router = Router()

admin_router.message.filter(IsAdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.answer(
        "Привет, это административная панель."
    )
