import requests
from config import tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import markups as nav


bot = Bot(token=tg_bot_token,parse_mode='HTML')
dp = Dispatcher(bot)

# Команды + Клавиатура
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Привет, "+message.from_user.first_name + "\nЯ F1-bot", reply_markup= nav.mainMenu)


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


@dp.message_handler(lambda message: message.text == "Следующая гонка ➡")
async def without_puree(message: types.Message):
    r = requests.get(
        f"http://ergast.com/api/f1/current/next.json"
    )
    data = r.json()['MRData']['RaceTable']['Races'][0]

    text ="<b>\nТрасса: </b>"+data['raceName']+ "<b>\nДата: </b>" + data["date"] + "<b>\nВремя: </b>"+ data["time"].replace("Z","")

    if message.text == "Следующая гонка ➡":
        await message.answer(text)


#Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp)
