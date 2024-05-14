from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import os
from base import base
from apps.rtrn import return_markup
from apps.rasa import rasa_markup
from apps.order import order_markup
from apps.repans import rep_ans_markup
from apps.admin import admin_markup
from apps.rec_inf import rec_inf_markup
from apps.start import start_markup, astart_markup
from apps.kvantorium import kvantorium_markup
from apps.it_cub import it_cube_markup
from apps.req_contact import req_markup
from apps.record import rec_markup
from apps.sections import sections
from dotenv import load_dotenv

load_dotenv('.env')
description = base
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
admin = os.getenv("ADMIN")
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
temp = []


class Helper(StatesGroup):
    rep = State()
    repa = State()
    rass = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    with open('users.txt', mode='a', encoding='utf-8') as txt:
        txt.write(f'{message.from_user.id}\n')
    photo = InputFile('files/preview.jpg')
    if str(message.from_user.id) != str(admin):
        await message.answer_photo(photo=photo,
                                   caption="Здравствуйте! Я бот, который поможет записать вашего ребенка в"
                                           " IT-Cube/Кванториум", reply_markup=start_markup)
    else:
        await message.answer_photo(photo=photo,
                                   caption="Здравствуйте! Я бот, который поможет записать вашего ребенка в "
                                           "IT-Cube/Кванториум", reply_markup=astart_markup)


@dp.callback_query_handler(text='Rec_start')
async def rec_inf(call: types.CallbackQuery):
    photo = InputFile('files/VS.jpg')
    await call.message.answer_photo(photo=photo, caption='Выберите учреждение',
                                    reply_markup=rec_inf_markup)


@dp.callback_query_handler(text='faq')
async def faq(call: types.CallbackQuery):
    a = description.cursor().execute('SELECT * FROM FAQ').fetchall()
    q = [f'{i + 1}: {a[i][0]}\n  Ответ: {a[i][1]}' for i in range(len(a))]
    photo = InputFile('files/faq.jpg')
    await call.message.answer_photo(photo=photo, caption='\n'.join(q), reply_markup=return_markup)


@dp.callback_query_handler(text='rep')
async def rep(call: types.CallbackQuery):
    photo = InputFile('files/faq.jpg')
    await call.message.answer_photo(photo=photo, caption="Напишите ваш вопрос")
    await Helper.rep.set()


@dp.message_handler(state=Helper.rep)
async def rep2(message: types.Message, state: FSMContext):
    cur = description.cursor()
    cur.execute(f'INSERT INTO [QST] (ID, QUEST) VALUES ({message.from_user.id}, "{message.text}")')
    description.commit()
    await message.answer('Ваш вопрос отправлен администраторам ✅', reply_markup=return_markup)
    await bot.send_message(admin, f'Поступил вопрос от пользователя {message.from_user.first_name}\n  Вопрос: {message.text}')
    await state.reset_state(with_data=False)


@dp.callback_query_handler(text='ans')
async def ans(call: types.CallbackQuery, state: FSMContext):
    description.cursor().execute(f'DELETE from [QST] where num = {call.message.text.split()[0].replace(":", "")}')
    description.commit()
    await state.update_data(temp=call.message.text.split()[1])
    await call.message.answer(f'Введите ответ на вопрос')
    await Helper.repa.set()


@dp.callback_query_handler(text='ign')
async def ign(call: types.CallbackQuery):
    description.cursor().execute(f'DELETE from [QST] where num = {call.message.text.split()[0].replace(":", "")}')
    description.commit()
    await call.message.delete()
    await call.message.answer('Вопрос успешно удалён ✅')


@dp.callback_query_handler(text='Orders')
async def order(call: types.CallbackQuery):
    cur = description.cursor().execute('SELECT * FROM [ORDER]').fetchall()
    if len(cur) != 0:
        for i in cur:
            a = f'ID заявки: {i[0]}\nФИО: {i[1]}\nСекция: {i[2]}\nНомер: {i[3]}\n'
            await call.message.answer(a, reply_markup=order_markup)
    else:
        await call.message.answer('Заявок нет')


@dp.callback_query_handler(text='del')
async def deleter(call: types.CallbackQuery):
    cur = description.cursor()
    inf = call.message.text.split()[2]
    cur.execute(f'DELETE from [ORDER] where id = {inf}')
    description.commit()
    await call.message.delete()
    await call.message.answer('Заявка успешно удалена')


@dp.callback_query_handler(text='rasa')
async def rasa(call: types.CallbackQuery):
    await call.message.answer('Выберите тип рассылки', reply_markup=rasa_markup)


@dp.callback_query_handler(text='r1')
async def r1(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(type='❗ Важная информация')
    await call.message.answer('Введите текст рассылки')
    await Helper.rass.set()


@dp.callback_query_handler(text='r2')
async def r2(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(type='🔥 Реклама')
    await call.message.answer('Введите текст рассылки')
    await Helper.rass.set()


@dp.callback_query_handler(text='r3')
async def r3(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(type='📢 Информация о наборе')
    await call.message.answer('Введите текст рассылки')
    await Helper.rass.set()


@dp.message_handler(state=Helper.rass)
async def rass(msg: types.Message, state: FSMContext):
    b = await state.get_data()
    with open('users.txt', mode='r', encoding='utf-8') as txt:
        a = list(set(txt.read().split()))
        for i in a:
            await bot.send_message(i, f'{b["type"]}\n{msg.text}')
    await state.reset_state(with_data=False)


@dp.callback_query_handler(text='faqa')
async def faqa(call: types.CallbackQuery):
    cur = description.cursor().execute('SELECT * FROM QST').fetchall()
    if len(cur) != 0:
        for i in cur:
            await call.message.answer(f'{i[0]}: {i[1]}: {i[2]}', reply_markup=rep_ans_markup)
    else:
        await call.message.answer('Контейнер с вопросами пуст')


@dp.message_handler(state=Helper.repa)
async def ans_text(message: types.Message, state: FSMContext):
    a = await state.get_data()
    await bot.send_message(a['temp'], f'Поступил ответ на ваш вопрос\n  {message.text}')
    await state.finish()


@dp.callback_query_handler(text='Кванториум')
async def kvantorium(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Выберите направление Кванториума:", reply_markup=kvantorium_markup)


@dp.callback_query_handler(text='IT-Cube')
async def it_cube(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Выберите направление в IT-кубе:", reply_markup=it_cube_markup)


@dp.callback_query_handler(text=list(map(str, range(16))))
async def rec(call: types.CallbackQuery):
    await call.message.delete()
    section = sections[int(call.data)]
    cur = description.cursor()
    cur.execute(f'INSERT INTO [ORDER] (name, section) VALUES ("{call.from_user.first_name} {call.from_user.last_name}",'
                f' "{section}")')
    info = cur.execute(f'SELECT INFO, age From DESC WHERE Section = "{section}"').fetchall()
    await call.message.answer(f'*{section}*\n{info[0][0]}\nВозраст: {info[0][1]}', reply_markup=rec_markup,
                              parse_mode='Markdown')


@dp.callback_query_handler(text='Record')
async def request(call: types.CallbackQuery):
    await call.message.delete()
    reply_text = f"Прекрасный выбор! Отправьте свой номер телефона, пожалуйста, чтобы администратор с вами связался."
    await call.message.answer(reply_text, reply_markup=req_markup)


@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message):
    phone_number = message.contact.phone_number
    cur = description.cursor()
    cur.execute(f"UPDATE [ORDER] SET phone = '{phone_number}'"
                f" WHERE name = '{message.from_user.first_name} {message.from_user.last_name}'")
    description.commit()
    await message.delete()
    await message.answer("Ваша заявка принята! ✅", reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(admin, 'Пришла заявка')


@dp.callback_query_handler(text='admin')
async def admin_menu(call: types.CallbackQuery):
    photo = InputFile('files/admin.jpg')
    await call.message.answer_photo(photo=photo, caption='Добрый день, Админ', reply_markup=admin_markup)


@dp.callback_query_handler(text='return')
async def rtrn(call: types.CallbackQuery):
    await start(call.message)


@dp.message_handler(lambda message: message.text)
async def oth(message):
    await message.answer('Я не понимаю вас')


executor.start_polling(dp)
