import requests
from aiogram.dispatcher.filters import Text
import logging
from aiogram import Bot, Dispatcher, executor, types
from db import Database
import markups as nav
from config import tg_bot_token, ADMIN_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=tg_token_bot)
dp = Dispatcher(bot)
db = Database('database.db')




@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет, "+message.from_user.first_name + "\nЯ F1-bot", reply_markup= nav.mainMenu)

async def start(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Добро пожаловать')

@dp.message_handler(Text(equals="Главное меню"))
async def with_puree(message: types.Message):
    if message.text == "Главное меню":
        await message.answer("Выбирай", reply_markup=nav.mainMenu)


@dp.message_handler(Text(equals="Результаты 🏎"))
async def with_puree(message:types.Message):
    if message.text == "Результаты 🏎":
        await message.answer("Что хочешь узнать?", reply_markup=nav.otherMenu)

@dp.message_handler(Text(equals="Результаты гонки"))
async def with_puree(message: types.Message):
    r = requests.get(
        f"http://ergast.com/api/f1/current/last/results.json"
        )
    data = r.json()['MRData']['RaceTable']['Races'][0]['Results']

    text = "<b>Пилот - Очки</b>\n\n"
    for driver in data:
        try:
            text += driver['Driver']['familyName'] + " - " + \
                    driver['Points']['points'] + "\n"
        except KeyError:
            try:
                text += driver['Driver']['familyName'] + " - " + \
                        driver['points'] + "\n"
            except Exception:
                pass
    await message.answer(text)

@dp.message_handler(Text(equals="Чемпионат 🏆"))
async def with_puree(message: types.Message):
    r = requests.get(
        f"http://ergast.com/api/f1/current/driverStandings.json"
        )
    data = r.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    text = "<b>Пилот - Очки</b>\n\n"
    for driver in data:
        try:
            text += driver['Driver']['familyName'] + " - " + \
                    driver['Points']['points'] + "\n"
        except KeyError:
            try:
                text += driver['Driver']['familyName'] + " - " + \
                        driver['points'] + "\n"
            except Exception:
                pass
    if message.text == "Чемпионат 🏆":
        await message.answer(text)

@dp.message_handler(Text(equals="Кубок конструкторов"))
async def with_puree(message: types.Message):
    r = requests.get(
        f"http://ergast.com/api/f1/current/constructorStandings.json"
    )
    data = r.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]

    text = "<b>Команда - Очки</b>\n\n"

    for team in data:
        try:
            text += team["Constructor"]["name"] + " - " + \
                    team['Points']['points'] + "\n"
        except KeyError:
            try:
                text += team["Constructor"]["name"] + " - " + \
                        team['points'] + "\n"
            except Exception:
                pass
    if message.text == "Кубок конструкторов":
        await message.answer(text)


@dp.message_handler(Text(equals="Кубок конструкторов"))
async def without_puree(message: types.Message):
    r = requests.get(
        f"http://ergast.com/api/f1/current/next.json"
    )
    data = r.json()['MRData']['RaceTable']['Races'][0]

    text ="<b>\nТрасса: </b>"+data['raceName']+ "<b>\nДата: </b>" + data["date"] + "<b>\nВремя: </b>"+ data["time"].replace("Z","")

    if message.text == "Следующая гонка ➡":
        await message.answer(text)



@dp.message_handler(commands=['admin'])
async def cmd_all(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == ADMIN_TOKEN:
            await message.answer("Админ-панель", reply_markup=nav.menuAdmin)
        else:
            await message.answer("Вы не админ!")

@dp.message_handler(Text(equals="Рассылка"))
async def with_puree(message: types.Message):
    await message.answer("Что отправить?")

    @dp.message_handler()
    async def all(message:types.Message):
        if message.chat.type == 'private':
            if message.from_user.id == ADMIN_TOKEN:
                text = message.text
                users = db.get_users()
                for row in users:
                    await bot.send_message(row[0], text)
            await bot.send_message(message.from_user.id, "Успешная рассылка", reply_markup=nav.menuAdmin)



#Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
