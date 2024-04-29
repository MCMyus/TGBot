from aiogram import types

req_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_phone = types.KeyboardButton('Отправить номер телефона', request_contact=True)
req_markup.add(button_phone)
