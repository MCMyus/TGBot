from aiogram import types
from apps.sections import sections

it_cube_markup = types.InlineKeyboardMarkup(resize_keyboard=True)
buttons = sections
a = []
for i in range(8):
    a.append(types.InlineKeyboardButton(text=buttons[i], callback_data=str(i)))

it_cube_markup.add(*a)
