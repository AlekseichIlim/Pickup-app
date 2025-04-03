
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

import app_company.keyboards.company_keyboards as company_kb
import app_company.requests as rq
from app_company.fsm_states import CompanyRegister, CategoryCreate, ProductCreate

from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

company_reg_router = Router()
category_router = Router()
product_router = Router()

data_company = []

@company_reg_router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Это бот для работы с приложением "Самовывоз".\n'
                         f'Чтобы начать работу необходимо зарегистрироваться, для этого нажмите на кнопку на клавиатуре'
                         f'\U0001F447', reply_markup=company_kb.menu)


@company_reg_router.message(StateFilter('*'), F.text == 'Назад')
async def back_to_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    previous = None

    for step in CompanyRegister.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Ок,\n{CompanyRegister.text[previous.state]}')
            return
        previous = step


@category_router.message(StateFilter('*'), F.text == 'Назад')
async def back_to_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    previous = None

    for step in CategoryCreate.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Ок,\n{CategoryCreate.text[previous.state]}')
            return
        previous = step

@product_router.message(StateFilter('*'), F.text == 'Назад')
async def back_to_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    previous = None

    for step in ProductCreate.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Ок,\n{ProductCreate.text[previous.state]}')
            return
        previous = step

@company_reg_router.message(F.text == 'Регистрация')
async def registration(message: Message, state: FSMContext):
    await state.set_state(CompanyRegister.name)
    await message.answer('Введенные название заведения.\n*Например: "Маленькая Италия"',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(f'*название, адрес и описание будут отображаться пользователям')


@company_reg_router.message(CompanyRegister.name)
async def registration_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.update_data(tg_id=message.from_user.id)
    await state.set_state(CompanyRegister.description)
    await message.answer('Введите описание заведения или его категорию', reply_markup=company_kb.back_button)


@company_reg_router.message(CompanyRegister.description)
async def registration_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CompanyRegister.city)
    await message.answer('Введите название города', reply_markup=company_kb.back_button)


@company_reg_router.message(CompanyRegister.city)
async def registration_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(CompanyRegister.addresses_street)
    await message.answer('Введите название улицы', reply_markup=company_kb.back_button)


@company_reg_router.message(CompanyRegister.addresses_street)
async def registration_addresses_street(message: Message, state: FSMContext):
    await state.update_data(addresses_street=message.text)
    await state.set_state(CompanyRegister.addresses_home)
    await message.answer('Введите номер дома', reply_markup=company_kb.back_button)


@company_reg_router.message(CompanyRegister.addresses_home)
async def registration_addresses_home(message: Message, state: FSMContext):
    await state.update_data(addresses_home=message.text)
    await state.set_state(CompanyRegister.addresses_comment)
    await message.answer('Введите комментарий к адресу', reply_markup=company_kb.back_button)


@company_reg_router.message(CompanyRegister.addresses_comment)
async def registration_addresses_comment(message: Message, state: FSMContext):
    await state.update_data(addresses_comment=message.text)
    await state.set_state(CompanyRegister.phone)
    await message.answer('Введите номер телефона', reply_markup=company_kb.back_button)


@company_reg_router.message(CompanyRegister.phone)
async def registration_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data_company = await state.get_data()
    if len(data_company['addresses_comment']) > 0:
        await message.answer(
            f'Организация: "{data_company['name']}", {data_company['description']}\nАдрес: {data_company['city']}, улица '
            f'{data_company['addresses_street']} дом {data_company['addresses_home']}. Коментарий: {data_company['addresses_comment']}\nТелефон: '
            f'{data_company['phone']}'
        )
    else:
        await message.answer(
            f'Организация: "{data_company['name']}", {data_company['description']}\nАдрес: {data_company['city']}, улица '
            f'{data_company['addresses_street']} дом {data_company['addresses_home']}.\nТелефон: {data_company['phone']}'
        )
    await message.answer('Ваша регистрация завершена.')
    await state.clear()
    await rq.save_data_company(data_company)
    await message.answer('Теперь вам необходимо создать меню', reply_markup=company_kb.create_menu)

# #####################################
# @menu_router.message(F.text == 'Создать меню')
@product_router.message(Command('test'))
async def create_menu(message: Message, state: FSMContext):
    await state.set_state(CategoryCreate.name_category)
    category_list = rq.get_categories(data_company)
    if category_list is not None:
        await message.answer('Выберите категорию или создайте новую')
    else:
        await message.answer('Введите название категории',
                                reply_markup=ReplyKeyboardRemove())


@product_router.message(CategoryCreate.name_category)
async def create_category_product(message: Message, state: FSMContext):
    await state.update_data(name_category=message.text)
    data_category = await state.get_data()
    await message.answer(f'Категория {data_category['name_category']} создана!', reply_markup=company_kb.back_button)

    await state.clear()
    await rq.save_data_category(data_category, data_company)
    # await message.answer('Введите название блюда', reply_markup=company_kb.back_button)


@product_router.message(ProductCreate.name_product)
async def create_name_product(message: Message, state: FSMContext):
    await state.update_data(name_product=message.text)
    await state.set_state(ProductCreate.photo_product)
    await message.answer('Загрузите фото блюда', reply_markup=company_kb.back_button)


# @product_router.message(ProductCreate.photo_product)
# async def create_name_product(message: Message, state: FSMContext):
#
#     file = await message.bot.get_file(message.photo[-1].file_id)
#     file_data = BytesIO()
#     await message.bot.download_file(file.file_path, file_data)
#
#     data = await state.get_data()
#     file_name = f'{data_company['name']}/{data['name_category']}/{data['name_product']}.jpg'
#     file_data.seek(0)
#     image_url = await storage.upload_file(file_data, file_name)
#
#     async with AsyncSessionLocal() as session:
#         session.add(Image(name=file_name, url=image_url))
#         await session.commit()
#     await message.answer(f'Изображение сохранено!')
#
#
#     await state.set_state(ProductCreate.price)
#     await message.answer('Введите цену', reply_markup=company_kb.back_button)
#
#
# @menu_router.message(MenuCreate.price)
# async def create_name_product(message: Message, state: FSMContext):
#     await state.update_data(price=message.text)
#     data = await state.get_data()