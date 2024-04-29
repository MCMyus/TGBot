from aiogram import types
from apps.sections import sections

kvantorium_markup = types.InlineKeyboardMarkup(resize_keyboard=True)
buttons = sections
a = []
for i in range(8, len(buttons)):
    a.append(types.InlineKeyboardButton(text=buttons[i], callback_data=str(i)))

kvantorium_markup.add(*a)
