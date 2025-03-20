from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class CompanyRegister(StatesGroup):
    tg_id = State()
    name = State()
    description = State()
    city = State()
    addresses_street = State()
    addresses_home = State()
    addresses_comment = State()
    phone = State()

    text = {
        'CompanyRegister:name': 'Введите название заново:',
        'CompanyRegister:description': 'Введите описание заново:',
        'CompanyRegister:city': 'Введите название города заново:',
        'CompanyRegister:addresses_street': 'Введите название улицы заново:',
        'CompanyRegister:addresses_home': 'Введите номер дома заново:',
        'CompanyRegister:addresses_comment': 'Введите комментарий к адресу заново:',
        'CompanyRegister:phone': 'Введите номер телефона заново:',

    }

class MenuCreate(StatesGroup):
    pass