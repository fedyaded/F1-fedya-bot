import requests
from config import tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text


bot = Bot(token=tg_bot_token,parse_mode='HTML')
dp = Dispatcher(bot)

# Команды + Клавиатура
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Результаты 🏎", "Следующая гонка ➡", "Чемпионат 🏆"]
    keyboard.add(*buttons)
    await message.answer("Привет, "+message.from_user.first_name + "\nЯ F1-bot", reply_markup=keyboard)

@dp.message_handler(Text(equals="Результаты 🏎"))
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
    await message.answer(text)



@dp.message_handler(lambda message: message.text == "Следующая гонка ➡")
async def without_puree(message: types.Message):
    r = requests.get(
        f"http://ergast.com/api/f1/current/next.json"
    )
    data = r.json()['MRData']['RaceTable']['Races'][0]

    text ="<b>\nТрасса: </b>"+data['raceName']+ "<b>\nДата: </b>" + data["date"] + "<b>\nВремя: </b>"+ data["time"].replace("Z","")

    await message.answer(text)


#Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp)