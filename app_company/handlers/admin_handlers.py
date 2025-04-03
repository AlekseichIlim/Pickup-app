from app_company.filtetrs.admin_filter import IsAdminFilter


from app_company.requests import get_all_objects
from models.models import Company, CategoryProduct
import app_company.keyboards.admin_keyboards as admin_kb
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

import app_company.keyboards.company_keyboards as company_kb
import app_company.requests as rq
from app_company.fsm_states import CompanyRegister, CategoryCreate, ProductCreate, DataCompany

from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

admin_company_router = Router()

admin_company_router.message.filter(IsAdminFilter())


@admin_company_router.message(CommandStart())
async def admin_start(message: Message):

    companies = await get_all_objects(Company)
    if len(companies) != 0:
        await message.answer(
            "Привет, это административная панель.", reply_markup=admin_kb.menu_company
        )
    else:
        await message.answer(
            "Привет, это административная панель. Зарегистрируй первую компанию.",
            reply_markup=admin_kb.create_company
        )


@admin_company_router.message(StateFilter('*'), F.text == 'Назад')
async def back_to_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    previous = None

    for step in CompanyRegister.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Ок,\n{CompanyRegister.text[previous.state]}')
            return
        previous = step

@admin_company_router.message(F.text == 'Создать организацию')
async def registration(message: Message, state: FSMContext):
    await state.set_state(CompanyRegister.name)
    await message.answer('Введенные название заведения.\n*Например: "Маленькая Италия"',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(f'*название, адрес и описание будут отображаться пользователям')


@admin_company_router.message(CompanyRegister.name)
async def registration_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.update_data(tg_id=message.from_user.id)
    await state.set_state(CompanyRegister.description)
    await message.answer('Введите описание заведения или его категорию', reply_markup=company_kb.back_button)


@admin_company_router.message(CompanyRegister.description)
async def registration_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CompanyRegister.city)
    await message.answer('Введите название города', reply_markup=company_kb.back_button)


@admin_company_router.message(CompanyRegister.city)
async def registration_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(CompanyRegister.addresses_street)
    await message.answer('Введите название улицы', reply_markup=company_kb.back_button)


@admin_company_router.message(CompanyRegister.addresses_street)
async def registration_addresses_street(message: Message, state: FSMContext):
    await state.update_data(addresses_street=message.text)
    await state.set_state(CompanyRegister.addresses_home)
    await message.answer('Введите номер дома', reply_markup=company_kb.back_button)


@admin_company_router.message(CompanyRegister.addresses_home)
async def registration_addresses_home(message: Message, state: FSMContext):
    await state.update_data(addresses_home=message.text)
    await state.set_state(CompanyRegister.addresses_comment)
    await message.answer('Введите комментарий к адресу', reply_markup=company_kb.back_button)


@admin_company_router.message(CompanyRegister.addresses_comment)
async def registration_addresses_comment(message: Message, state: FSMContext):
    await state.update_data(addresses_comment=message.text)
    await state.set_state(CompanyRegister.phone)
    await message.answer('Введите номер телефона', reply_markup=company_kb.back_button)


@admin_company_router.message(CompanyRegister.phone)
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
    await message.answer('Регистрация завершена.', reply_markup=admin_kb.menu_company)
    await state.clear()
    await rq.save_data_company(data_company)


@admin_company_router.message(F.text == 'Просмотр организаций')
async def view_all_companies(message: Message):
    await message.answer('Выберите заведение.',
                         reply_markup=await admin_kb.companies())


@admin_company_router.callback_query(F.data.startswith('company_'))
async def view_one_company(callback: CallbackQuery, state: FSMContext):

    company_id = int(callback.data.split('_')[1])
    company = await rq.get_one_object(Company, company_id)
    categories = await rq.get_all_objects_foreignkey(CategoryProduct.company, company_id)
    await state.update_data(company=company)
    await state.set_state(DataCompany.view_data_company)

    if len(categories) != 0:
        await callback.message.answer(f'{company.name}', reply_markup=admin_kb.view_company_and_menu)
    else:
        await callback.message.answer(f'{company.name}', reply_markup=admin_kb.view_company_not_menu)


@admin_company_router.message(DataCompany.view_data_company, F.text == 'Посмотреть данные')
async def view_data_company(message: Message, state: FSMContext):
    data = await state.get_data()
    company = data['company']
    await message.answer(f'Назавние: {company.name}\nОписание:{company.description}\nАдрес: {company.city}, улица '
                         f'{company.addresses_street} дом {company.addresses_home}\nКоментарий:'
                         f'{company.addresses_comment}\nТелефон: {company.phone}')


@admin_company_router.message(F.text == 'Редактировать данные')
async def update_data_company(message: Message, state: FSMContext):
    await state.clear()