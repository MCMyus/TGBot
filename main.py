from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import os
from apps.repans import rep_ans_markup
from apps.admin import admin_markup
from apps.rec_inf import rec_inf_markup
from apps.start import start_markup, astart_markup
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
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
temp = []


class Helper(StatesGroup):
    rep = State()
    repa = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if str(message.from_user.id) != str(admin):
        await message.answer("Здравствуйте! Я бот, который поможет записать вашего ребенка в IT-Cube/Кванториум",
                             reply_markup=start_markup)
    else:
        await message.answer("Здравствуйте! Я бот, который поможет записать вашего ребенка в IT-Cube/Кванториум",
                             reply_markup=astart_markup)


@dp.callback_query_handler(text='Rec_start')
async def rec_inf(call: types.CallbackQuery):
    await call.message.answer('Выберите учреждение',
                              reply_markup=rec_inf_markup)


@dp.callback_query_handler(text='faq')
async def faq(call: types.CallbackQuery):
    a = description.cursor().execute('SELECT * FROM FAQ').fetchall()
    q = [f'{i + 1}: {a[i][0]}\n  Ответ: {a[i][1]}' for i in range(len(a))]
    await call.message.answer(text='\n'.join(q))


@dp.callback_query_handler(text='rep')
async def rep(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Напишите ваш вопрос")
    await state.update_data(temp=call.from_user.id)
    a = await state.get_data()
    print(a)
    await Helper.rep.set()


@dp.message_handler(state=Helper.rep)
async def rep2(message: types.Message, state: FSMContext):
    await message.answer('Ваш вопрос отправлен администраторам')
    await bot.send_message(admin, f'Поступил вопрос от пользователя {message.from_user.first_name}\n  {message.text}',
                           reply_markup=rep_ans_markup)
    await state.reset_state(with_data=False)


@dp.callback_query_handler(text='ans')
async def ans(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите ответ на вопрос')
    await Helper.repa.set()


@dp.message_handler(state=Helper.repa)
async def ans_text(message: types.Message, state: FSMContext):
    a = await state.get_data()
    print(a)
    await bot.send_message(a['temp'], f'Поступил ответ на ваш вопрос\n  {message.text}')
    await state.finish()


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


@dp.callback_query_handler(text='admin')
async def admin_menu(call: types.CallbackQuery):
    await call.message.answer('Добрый день, Админ', reply_markup=admin_markup)


@dp.message_handler(lambda message: message.text)
async def oth(message):
    await message.answer('Я не понимаю вас')


executor.start_polling(dp)
