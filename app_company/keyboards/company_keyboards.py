from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Регистрация')]
                                     ],
                           resize_keyboard=True, input_field_placeholder="Нажмите кнопку 'Регистрация'"
)

menu_2 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад'), KeyboardButton(text='Дальше')]
                                     ],
                           resize_keyboard=True, input_field_placeholder="Нажмите кнопку 'Регистрация'"
)

back_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=f'Назад')]], resize_keyboard=True)
# \U0001F519