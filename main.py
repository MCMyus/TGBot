from aiogram import Bot, Dispatcher, types, executor
import os
from apps.rec_inf import rec_inf_markup
from apps.start import start_markup
from apps.kvantorium import kvantorium_markup
from apps.it_cub import it_cube_markup
from apps.req_contact import req_markup
from apps.record import rec_markup
from apps.sections import sections
import sqlite3
from dotenv import load_dotenv

load_dotenv()
description = sqlite3.connect('Base.sqlite3')
bot = Bot(os.getenv('TOKEN'))
admin = os.getenv("ADMIN")
dp = Dispatcher(bot=bot)
temp = []


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Здравствуйте! Я бот, который поможет записать вашего ребенка в IT-Cube/Кванториум",
                         reply_markup=start_markup)


@dp.callback_query_handler(text = 'Rec_start')
async def rec_inf(call: types.CallbackQuery):
    await call.message.answer('Выберите учреждение',
                              reply_markup=rec_inf_markup)


@dp.callback_query_handler(text='Кванториум')
async def kvantorium(call: types.CallbackQuery):
    await call.message.answer("Выберите направление Кванториума:", reply_markup=kvantorium_markup)


@dp.callback_query_handler(text='IT-Cube')
async def it_cube(call: types.CallbackQuery):
    await call.message.answer("Выберите направление в IT-кубе:", reply_markup=it_cube_markup)


@dp.callback_query_handler(text=list(map(str, range(16))))
async def rec(call: types.CallbackQuery):
    section = sections[int(call.data)]
    cur = description.cursor()
    cur.execute(f'INSERT INTO [ORDER] (name, section) VALUES ("{call.from_user.first_name} {call.from_user.last_name}",'
                f' "{section}")')
    info = cur.execute(f'SELECT INFO, age From DESC WHERE Section = "{section}"').fetchall()
    await call.message.answer(f'*{section}*\n{info[0][0]}\nВозраст: {info[0][1]}', reply_markup=rec_markup,
                              parse_mode='Markdown')


@dp.callback_query_handler(text='Record')
async def request(call: types.CallbackQuery):
    reply_text = f"Прекрасный выбор! Отправьте свой номер телефона, пожалуйста, чтобы администратор с вами связался."
    await call.message.answer(reply_text, reply_markup=req_markup)


@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message):
    phone_number = message.contact.phone_number
    cur = description.cursor()
    cur.execute(f"UPDATE [ORDER] SET phone = '{phone_number}'"
                f" WHERE name = '{message.from_user.first_name} {message.from_user.last_name}'")
    description.commit()
    await message.answer("Ваша заявка принята!")
    await bot.send_message(admin, 'Пришла заявка')


@dp.message_handler(lambda message: message.text == 'ADMIN-Панель')
async def admin_menu(message: types.Message):
    pass


@dp.message_handler(lambda message: message.text)
async def oth(message):
    await message.answer('Я не понимаю вас')


executor.start_polling(dp)
