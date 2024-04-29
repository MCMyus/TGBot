from aiogram import types

rec_markup = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_rec = types.InlineKeyboardButton(text='Оставить заявку', callback_data='Record')
rec_markup.add(button_rec)
