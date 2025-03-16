from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class UserRegister(StatesGroup):
    name = State()
    age = State()
    phone = State()
