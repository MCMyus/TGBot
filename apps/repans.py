from aiogram import types

rep_ans_markup = types.InlineKeyboardMarkup(resize_keyboard=True)
ans = types.InlineKeyboardButton(text='✏️ Ответить', callback_data='ans')
ign = types.InlineKeyboardButton(text='🗑️ Удалить', callback_data='ign')
rep_ans_markup.add(ans, ign)