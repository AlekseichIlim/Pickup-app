from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Регистрация')]
                                     ],
                           resize_keyboard=True, input_field_placeholder="Нажмите кнопку 'Регистрация'"
)

# back_button = KeyboardButton('Назад')