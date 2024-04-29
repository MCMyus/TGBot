from aiogram import types

start_markup = types.InlineKeyboardMarkup()
rec_button = types.InlineKeyboardButton(text='Записаться', callback_data='Rec_start')
faq = types.InlineKeyboardButton(text='Частые вопросы', callback_data='faq')
ask = types.InlineKeyboardButton(text='Задать вопрос', callback_data='rep')
fm = types.InlineKeyboardButton(text='О нас', callback_data='fm')
start_markup.add(rec_button, faq, ask, fm)
