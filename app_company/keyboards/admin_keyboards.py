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
    keyboard.add(InlineKeyboardButton(text='Назад\U00002b05', callback_data='to_back_main_menu'))
    return keyboard.adjust(2).as_markup()


async def data_company():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Название', callback_data='update_company_name'),
                 InlineKeyboardButton(text='Описание', callback_data='update_company_description'),
                 InlineKeyboardButton(text='Город', callback_data='update_company_city'),
                 InlineKeyboardButton(text='Улицу', callback_data='update_company_addresses_street'),
                 InlineKeyboardButton(text='Номер дома', callback_data='update_company_addresses_home'),
                 InlineKeyboardButton(text='Комментарий', callback_data='update_company_addresses_comment'),
                 InlineKeyboardButton(text='Телефон', callback_data='update_company_phone'),
                 InlineKeyboardButton(text='Статус', callback_data='update_company_is_active'),
                 InlineKeyboardButton(text='Назад\U00002b05', callback_data='back'),
                 )
    return keyboard.adjust(3).as_markup()
