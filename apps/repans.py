from aiogram import types


rep_ans_markup = types.InlineKeyboardMarkup(resize_keyboard=True)
<<<<<<< HEAD
ans = types.InlineKeyboardButton(text='✏️ Ответить', callback_data='ans')
ign = types.InlineKeyboardButton(text='🗑️ Удалить', callback_data='ign')
=======
ans = types.InlineKeyboardButton(text='Ответить', callback_data=f'ans')
ign = types.InlineKeyboardButton(text='Удалить', callback_data='ign')
>>>>>>> origin/master
rep_ans_markup.add(ans, ign)