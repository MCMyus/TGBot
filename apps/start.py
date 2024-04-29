from aiogram import types

start_markup = types.InlineKeyboardMarkup()
rec_button = types.InlineKeyboardButton(text='Записаться', callback_data='Rec_start')
faq = types.InlineKeyboardButton(text='Частые вопросы', callback_data='faq')
ask = types.InlineKeyboardButton(text='Задать вопрос', callback_data='rep')

