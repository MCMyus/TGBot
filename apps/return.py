from aiogram import types

return_markup = types.InlineKeyboardMarkup(resize_keyboard=True)
retbut = types.InlineKeyboardButton('🔙 Назад', callback_data='return')
return_markup.add(retbut)