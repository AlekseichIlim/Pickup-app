from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app_company.requests as rq
from models.models import Company

create_company = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Создать организацию')]
                                               ], resize_keyboard=True)

menu_company = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Создать организацию')],
                                             [KeyboardButton(text='Просмотр организаций')]
                                             ], resize_keyboard=True)

view_company_and_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Посмотреть данные'),
                                                       KeyboardButton(text='Редактировать данные')
                                                       ],
                                                      [KeyboardButton(text='Посмотреть меню'),
                                                       KeyboardButton(text='Редактировать меню')
                                                       ],
                                                      [KeyboardButton(text='К списку заведений')]
                                                      ], resize_keyboard=True)

view_company_not_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Посмотреть данные'),
                                                       KeyboardButton(text='Редактировать данные')
                                                       ],
                                                      [KeyboardButton(text='Создать меню')
                                                       ],
                                                      [KeyboardButton(text='К списку заведений')]
                                                      ], resize_keyboard=True)


async def companies():
    all_companies = await rq.get_all_objects(Company)
    keyboard = InlineKeyboardBuilder()
    for company in all_companies:
        keyboard.add(InlineKeyboardButton(text=company.name, callback_data=f'company_{company.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_back_main_menu'))
    return keyboard.adjust(2).as_markup()
