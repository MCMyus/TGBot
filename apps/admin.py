from aiogram import types

admin = types.InlineKeyboardMarkup()
req = types.InlineKeyboardButton(text='Список заявок', callback_data='Orders')
faq = types.InlineKeyboardButton(text='Частые вопросы', callback_data='faqa')
ras = types.InlineKeyboardButton(text='Создать рассылку', callback_data='rasa')
admin.add(req, faq, ras)