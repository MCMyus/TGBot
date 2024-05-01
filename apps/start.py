from aiogram import types

start_markup = types.InlineKeyboardMarkup(resize_keyboard=True)
astart_markup = types.InlineKeyboardMarkup(resize_keyboard=True)
rec_button = types.InlineKeyboardButton(text='📝 Записаться', callback_data='Rec_start')
faq = types.InlineKeyboardButton(text='❔ Частые вопросы', callback_data='faq')
ask = types.InlineKeyboardButton(text='⁉️ Задать вопрос', callback_data='rep')
fmk = types.InlineKeyboardButton(text='ℹ️ О нас(Кваториум)', url="https://kvantorium.stavdeti.ru/")
fmi = types.InlineKeyboardButton(text='ℹ️ О нас(IT-Cube)', url='https://itcube.stavdeti.ru/')
admin = types.InlineKeyboardButton(text='👨‍💻 АДМИН-Панель', callback_data='admin')
start_markup.add(rec_button, faq, ask, fmk, fmi)
astart_markup.add(rec_button, faq, ask, fmk, fmi, admin)
