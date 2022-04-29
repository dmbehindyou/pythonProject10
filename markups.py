from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnChangeSchool = KeyboardButton('Изменить школу')
btnGetMenu = KeyboardButton('Получить меню')
btnSupport = KeyboardButton('/support')
minorMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnChangeSchool, btnGetMenu, btnSupport)
defaultMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnSupport)

btnGiveMessage = KeyboardButton('/получить_сообщение')
btnAnswer = KeyboardButton('/написать_кому-то')
btnReturn = KeyboardButton('/назад')
btnAddPhoto = KeyboardButton("/добавить_фото")
adminPanelMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnGiveMessage, btnAnswer, btnReturn, btnAddPhoto)
btnReport = KeyboardButton('/сообщить_о_баге')
btnAddSchool = KeyboardButton('/добавить_школу')
reportMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnReport, btnAddSchool, btnReturn)

btn_n_chelny = InlineKeyboardButton(text="г. Набережные Челны", callback_data="btn_n_chelny")
inlineMenu = InlineKeyboardMarkup(row_width=2).insert(btn_n_chelny)

btn_lic_int79 = InlineKeyboardButton(text="Лицей-интернат №79", callback_data="btn_lic_int79")
btn_sch78 = InlineKeyboardButton(text="Лицей №78", callback_data="btn_sch78")
btn_gym26 = InlineKeyboardButton(text="Гимназия №26", callback_data="btn_gym26")
inlineMinorMenu = InlineKeyboardMarkup(row_width=2).add(btn_lic_int79, btn_sch78, btn_gym26)
