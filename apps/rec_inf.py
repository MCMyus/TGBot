from aiogram import types

rec_inf_markup = types.InlineKeyboardMarkup(resize_keyboard=True)
kvantorium_button = types.InlineKeyboardButton(text='Кванториум', callback_data='Кванториум')
it_cube_button = types.InlineKeyboardButton(text='IT - куб', callback_data='IT-Cube')
rec_inf_markup.add(kvantorium_button, it_cube_button)
