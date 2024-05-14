from aiogram import types

admin_markup = types.InlineKeyboardMarkup()
req = types.InlineKeyboardButton(text='📒 Список заявок', callback_data='Orders')
faq = types.InlineKeyboardButton(text='❔📒 Список вопросов', callback_data='faqa')
ras = types.InlineKeyboardButton(text='🔥 Создать рассылку', callback_data='rasa')
ret = types.InlineKeyboardButton(text='🔙 Вернуться в меню', callback_data='return')
admin_markup.add(req, faq, ras).add(ret)