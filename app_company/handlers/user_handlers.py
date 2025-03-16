from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram import Router
import app_company.keyboards.user_keyboards as user_kb
from aiogram.fsm.context import FSMContext
from app_company.fsm_states import UserRegister
from aiogram.types import ReplyKeyboardRemove

# import app.keyboards as kb
user_router = Router()

@user_router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Это бот для работы с приложением "Самовывоз".\n'
                         f'Чтобы начать работу необходимо зарегистрироваться, для этого нажмите на кнопку на клавиатуре'
                         f'\U0001F447', reply_markup=user_kb.menu)

@user_router.message(F.text == 'Регистрация')
async def registration(message: Message, state: FSMContext):
    await state.set_state(UserRegister.name)
    await message.answer('Введенные название заведения.\n*Например: Пиццерия "Маленькая Италия"',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(f'*название, адрес и описание будут отображаться пользователям')


@user_router.message(UserRegister.name)
async def registration_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserRegister.age)
    await message.answer('Введите ваш возраст.')


@user_router.message(UserRegister.age)
async def registration_name(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(UserRegister.phone)
    await message.answer('Введите ваш телефон.')


@user_router.message(UserRegister.phone)
async def registration_name(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    await message.answer(f'Имя: {data['name']}\nВозраст: {data['age']}\nТелефон: {data['phone']}')
    await message.answer('Ваша регистрация завершена.')