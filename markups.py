from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnAdmin = KeyboardButton("Панель Администратора")

### ADMIN PANEL ###

btnAll = KeyboardButton("Рассылка")
btnOff = KeyboardButton("Разблокировать")
menuAdmin = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAll,btnOff)

btnMain = KeyboardButton("Главное меню")

### Main menu ###
btnRandom = KeyboardButton("Результаты 🏎")
btnOther = KeyboardButton ("Следующая гонка ➡")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRandom,btnOther)

### Other menu ###

btnInfo = KeyboardButton("Чемпионат 🏆")
btnInfo2 = KeyboardButton ("Кубок конструкторов")
btnInfo3 = KeyboardButton ("Результаты гонки")
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo,btnInfo2,btnInfo3, btnMain)
