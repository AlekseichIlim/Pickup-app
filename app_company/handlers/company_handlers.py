from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram import Router
import app_company.keyboards.company_keyboards as company_kb
from aiogram.fsm.context import FSMContext
from app_company.fsm_states import CompanyRegister
from aiogram.types import ReplyKeyboardRemove

# import app.keyboards as kb
company_router = Router()

@company_router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Это бот для работы с приложением "Самовывоз".\n'
                         f'Чтобы начать работу необходимо зарегистрироваться, для этого нажмите на кнопку на клавиатуре'
                         f'\U0001F447', reply_markup=company_kb.menu)


@company_router.message(StateFilter('*'), F.text == 'Назад')
async def back_to_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    previous = None

    for step in CompanyRegister.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Ок,\n{CompanyRegister.text[previous.state]}')
            return
        previous = step

@company_router.message(F.text == 'Регистрация')
async def registration(message: Message, state: FSMContext):
    await state.set_state(CompanyRegister.name)
    await message.answer('Введенные название заведения.\n*Например: "Маленькая Италия"',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(f'*название, адрес и описание будут отображаться пользователям')


@company_router.message(CompanyRegister.name)
async def registration_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.update_data(tg_id=message.from_user.id)
    await state.set_state(CompanyRegister.description)
    await message.answer('Введите описание заведения или его категорию', reply_markup=company_kb.back_button)


@company_router.message(CompanyRegister.description)
async def registration_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CompanyRegister.city)
    await message.answer('Введите название города', reply_markup=company_kb.back_button)


@company_router.message(CompanyRegister.city)
async def registration_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(CompanyRegister.addresses_street)
    await message.answer('Введите название улицы', reply_markup=company_kb.back_button)


@company_router.message(CompanyRegister.addresses_street)
async def registration_addresses_street(message: Message, state: FSMContext):
    await state.update_data(addresses_street=message.text)
    await state.set_state(CompanyRegister.addresses_home)
    await message.answer('Введите номер дома', reply_markup=company_kb.back_button)


@company_router.message(CompanyRegister.addresses_home)
async def registration_addresses_home(message: Message, state: FSMContext):
    await state.update_data(addresses_home=message.text)
    await state.set_state(CompanyRegister.addresses_comment)
    await message.answer('Введите комментарий к адресу', reply_markup=company_kb.back_button)


@company_router.message(CompanyRegister.addresses_comment)
async def registration_addresses_comment(message: Message, state: FSMContext):
    await state.update_data(addresses_comment=message.text)
    await state.set_state(CompanyRegister.phone)
    await message.answer('Введите номер телефона', reply_markup=company_kb.back_button)


@company_router.message(CompanyRegister.phone)
async def registration_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    if len(data['addresses_comment']) > 0:
        await message.answer(
            f'Организация: "{data['name']}", {data['description']}\nАдрес: {data['city']}, улица '
            f'{data['addresses_street']} дом {data['addresses_home']}. Коментарий: {data['addresses_comment']}\nТелефон: '
            f'{data['phone']}'
        )
    else:
        await message.answer(
            f'Организация: "{data['name']}", {data['description']}\nАдрес: {data['city']}, улица '
            f'{data['addresses_street']} дом {data['addresses_home']}.\nТелефон: {data['phone']}'
        )
    await message.answer('Ваша регистрация завершена.')
    await state.clear()