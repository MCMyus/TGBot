from aiogram import types

rasa_markup = types.InlineKeyboardMarkup(resize_keyboard=True)
type_r1 = types.InlineKeyboardButton('❗ Важная информация', callback_data='r1')
type_r2 = types.InlineKeyboardButton('🔥 Реклама', callback_data='r2')
type_r3 = types.InlineKeyboardButton('📢 Информация о наборе', callback_data='r3')
rasa_markup.add(type_r1, type_r2, type_r3)