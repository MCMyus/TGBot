from aiogram import types

order_markup = types.InlineKeyboardMarkup(resize_keyboard=True)
dell = types.InlineKeyboardButton('🗑️Удалить', callback_data='del')

order_markup.add(dell)
