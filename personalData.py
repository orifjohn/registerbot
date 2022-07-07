from aiogram.dispatcher.filters.state import State, StatesGroup


class PersonalData(StatesGroup):
    email = State()
    password = State()
    confirm_password = State()
    fullname = State()
    phone = State()
