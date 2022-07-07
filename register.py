import sqlite3
from os import fsdecode, stat
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.storage import FSMContext
# from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.personalData import PersonalData


@dp.message_handler(Command('register'))
async def enter_registration(message: types.Message):
    await message.answer("Assalomu alaykum, Email manzilingizni kiriting:")
    await PersonalData.email.set()


@dp.message_handler(state=PersonalData.email)
async def answer_fullname(message: types.Message, state: FSMContext):
    email = message.text

    await state.update_data(
        {
            "email": email
        }
    )

    await message.answer("Parol kiriting:")

    # await PersonalData.next()
    await PersonalData.password.set()


@dp.message_handler(state=PersonalData.password)
async def answer_fullname(message: types.Message, state: FSMContext):
    password = message.text

    await state.update_data(
        {
            "password": password
        }
    )

    await message.answer("Parolni tasdiqlang:")

    # await PersonalData.next()
    await PersonalData.confirm_password.set()


@dp.message_handler(state=PersonalData.confirm_password)
async def answer_email(message: types.Message, state: FSMContext):
    confirm_password = message.text

    await state.update_data(
        {
            "confirm_password": confirm_password
        }
    )

    data = await state.get_data()
    password = data.get('password')

    if password != confirm_password:
        await message.answer("Parol mos kelmadi. Qaytadan kiriting!")
        await PersonalData.password.set()
    else:
        await message.answer("To'liq ism familyangizni kiriting:")
        await PersonalData.next()


@dp.message_handler(state=PersonalData.fullname)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text

    await state.update_data(
        {
            "fullname": fullname
        }
    )

    await message.answer("Telefon raqamingizni kiriting:")

    # await PersonalData.next()
    await PersonalData.phone.set()


@dp.message_handler(state=PersonalData.phone)
async def answer_phone(message: types.Message, state: FSMContext):
    phone = message.text

    await state.update_data(
        {
            "phone": phone
        }
    )

    data = await state.get_data()
    email = data.get('email')
    confirm_password = data.get('confirm_password')
    fullname = data.get('fullname')
    phone = data.get('phone')

    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    user_info = [email, fullname, phone, confirm_password]
    cur.execute('INSERT INTO user (email, fullname, phone, password) VALUES (?,?,?,?)', user_info)


    conn.commit()
    conn.close()

    msg = "Quyidagi ma'lumotlar qabul qilindi:\n"
    msg += f"Email manzilingiz - {email}\n"
    msg += f"Ism Familyangiz - {fullname}\n"
    msg += f"Telefon raqamingiz - {phone}\n"

    await message.answer(msg)
    await message.answer("Tizimga kirish uchun 👉 /login bosing")

    # await state.finish()
    await state.reset_state(with_data=False)
