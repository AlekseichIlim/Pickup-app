from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Регистрация')]
                                     ],
                           resize_keyboard=True, input_field_placeholder="Нажмите кнопку 'Регистрация'"
)

create_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Создать меню')]
                                     ],
                           resize_keyboard=True, input_field_placeholder="Нажмите кнопку 'Создать меню'"
)

back_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=f'Назад')]], resize_keyboard=True)
# \U0001F519