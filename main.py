from aiogram import Bot, Dispatcher, executor, types
from aiohttp import ClientSession
from utils import JsonFile
import logging
from modules import button
from datetime import datetime
import os

DOB_IN_FORMAT = "%Y-%m-%d"
DOB_OUT_FORMAT = "%d %B %Y"

# LOGGING
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "api_id": "",
    "api_hash": "",
    "bot_token": "1722679318:AAEFLSggjahVJpifH77JZLvf3E8AR82GRXo",
    "api_url": "",
    "api_token": ""
}

ENV = (os.path.dirname(os.path.realpath(__file__)))
config_path = os.path.join(ENV, "config.json")
Config = JsonFile("Config.json", DEFAULT_CONFIG)
client = Bot(token=Config['bot_token'])
dp = Dispatcher(client)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# MAIN MENU
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    welcome_msg = "Hi " + str(
        message.from_user.first_name) + " here is some help: \n\n🔔 My information: Version: 1.00 August 21 Latest addition: BETA-VERSION \n\n  (by Michele Berardi 🐗) \n\n" \
                                        "💬 I already have a lot of capabilities: \n\n" \
                                        "🏁MotoGP -Show Current 🏁 Grand Prix or ⏱️ Qualifying results. \n" \
                                        "🏁Moto2 -Show Current 🏁 Grand Prix or ⏱️ Qualifying results. \n" \
                                        "🏁Moto3 - Show Current 🏁 Grand Prix or ⏱️ Qualifying results. \n" \
                                        "👱🏼RiderMotoGp - Show information about a 👱🏼 driver from the current season. \n " \
                                        "👱🏼RiderMoto2 - Show information about a 👱🏼 driver from the current season. \n " \
                                        "👱🏼RiderMoto3 - Show information about a 👱🏼 driver from the current season.\n " \
                                        "🏆StandingsMotoGp - Show 👱🏼 driver standings for the current season.\n " \
                                        "🏆StandingsMoto2 - Show 👱🏼 driver standings for the current season.\n " \
                                        "🏆StandingsMoto3 - Show 👱🏼 driver standings for the current season.\n "

    buttons = button.button_menu()
    await message.reply(welcome_msg, reply_markup=buttons)


# MOTO GP RESULTS LISTA CIRCUITS
@dp.message_handler(lambda message: "🏁Moto" in message.text)
async def motogp_list_circuit_answer(message: types.Message):
    print(message.text)
    welcome_msg = "Hi " + str(
        message.from_user.first_name) + " select the circuit you want to see the result: \n\n"
    buttons = button.button_list_circuits(message.text)
    await message.reply(welcome_msg, reply_markup=buttons)
    await message.delete()


@dp.callback_query_handler(lambda call: "circuits" in call.data)
#@dp.answerCallbackQuery(lambda call: "circuits" in call.data)
async def motogp_get_sessions_by_circuit(call: types.CallbackQuery):
    print("***************" + str(call.data))
    category = call.data.split("-")[1]
    category = category.replace("🏁", "")
    event_id = call.data.split("-")[3]
    print(category, event_id)
    welcome_msg = "🏁 select the sessions you want to see the results: \n\n"
    buttons = button.button_list_sessions_motogp(category, event_id, "2022")
    await call.message.answer(welcome_msg, reply_markup=buttons)

@dp.callback_query_handler(lambda call: "sessions" in call.data)
async def parse_sessions(call: types.CallbackQuery):
    category = call.data.split("-")[1]
    session_event = call.data.split("-")[2]
    event = call.data.split("-")[3]
    year = call.data.split("-")[4]
    print(category)
    print(session_event)
    print(event)
    print(year)
    async with ClientSession() as session:
        url = f"{Config['api_url']}/motoresultsessionsnew?year={year}&category={category}&event={event}&session={session_event}&token={Config['api_token']}"
        async with session.get(url) as res:
            json = await res.json()
            circuit_name = json[0]['circuit_name']
            if json[0]['championship_id'] == '0':
                error = "❌ No data for this session! If this session only finished recently, please try again in a few minutes"
                await call.message.answer(error)

            else:
                drivers = [(driver['pos'], f"{driver['rider_name']} {driver['rider_surname']} (+{driver['lap_time']})")
                           for driver in json]
                drivers = sorted(drivers, key=lambda x: x[0])
                messages = [f"{year[0]}. {year[1]}" for year in drivers]
                result_msg = f"🏆 The {year} {category} Rider Result {circuit_name}:\n\n" + "\n".join(messages)
                await call.message.answer(result_msg)


# RIDER MOTOGP
@dp.message_handler(lambda message: "👱🏼RiderMotoGP" in message.text)
async def motogp_list_circuit_answer(message: types.Message):
    welcome_msg = "Hi " + str(
        message.from_user.first_name) + " select the circuit you want to see the resus: \n\n"
    async with ClientSession() as session:
        url = f"{Config['api_url']}/motogprider?year=2022&token={Config['api_token']}"
        async with session.get(url) as res:
            json = await res.json()
            buttons = button.button_list_rider_motogp(json, category="MotoGP")
            await message.reply(welcome_msg, reply_markup=buttons)
            await message.delete()


@dp.message_handler(lambda message: "👱🏼RiderMoto2" in message.text)
async def motogp_list_circuit_answer(message: types.Message):
    welcome_msg = "Hi " + str(
        message.from_user.first_name) + " select the circuit you want to see the resus: \n\n"
    async with ClientSession() as session:
        url = f"{Config['api_url']}/motogprider?year=2022&token={Config['api_token']}"
        async with session.get(url) as res:
            json = await res.json()
            buttons = button.button_list_rider_motogp(json, category="Moto2")
            await message.reply(welcome_msg, reply_markup=buttons)
            await message.delete()


@dp.message_handler(lambda message: "👱🏼RiderMoto3" in message.text)
async def motogp_list_circuit_answer(message: types.Message):
    welcome_msg = "Hi " + str(
        message.from_user.first_name) + " select the circuit you want to see the resus: \n\n"
    async with ClientSession() as session:
        url = f"{Config['api_url']}/motogprider?year=2022&token={Config['api_token']}"
        async with session.get(url) as res:
            json = await res.json()
            buttons = button.button_list_rider_motogp(json, category="Moto3")
            await message.reply(welcome_msg, reply_markup=buttons)
            await message.delete()


@dp.callback_query_handler(lambda call: "rider_number" in call.data)
async def motogp_get_sessions_by_circuit(call: types.CallbackQuery):
    rider_number = call.data.split("-")[1]
    async with ClientSession() as session:
        url = f"{Config['api_url']}/motogprider?year=2022&token={Config['api_token']}"
        async with session.get(url) as res:
            json = await res.json()
            for rider in json:
                if rider['rider_number'] == rider_number:
                    wanted_driver = rider
            now = datetime.now()
            dob = datetime.strptime(wanted_driver['dob'], DOB_IN_FORMAT)
            message = f"👱🏼 Driver information for {wanted_driver['rider_surname']}:\n\n"
            message += f"📇 Name: {wanted_driver['rider_name']} {wanted_driver['rider_surname']}\n"
            message += f"🌎 Nationality: {wanted_driver['country']}\n"
            message += f"🍼 Age/DOB: {((now - dob).days) // 365}, {dob.strftime(DOB_OUT_FORMAT)}\n"
            message += f"🔢 Number: {wanted_driver['rider_number']}\n"
            message += f"👩‍👩‍👦‍👦 Team: {wanted_driver['team_name']}\n"
            message += f"🏁 Category: {wanted_driver['category']}\n"
            message += f"🔧 Constructor: {wanted_driver['constructor']}\n"
            await call.message.answer(message)


# StandingsMotoG
#@dp.callback_query_answer_handler(lambda call: "standings" in call.data)
@dp.callback_query_handler(lambda call: "standing-MotoGP" in call.data)
async def motogp_standing(call: types.CallbackQuery):
    category = call.data.split("-")[1]
    async with ClientSession() as session:
        url = f"{Config['api_url']}/motoriderstanding?year=2022&category=motogp&token={Config['api_token']}"
        async with session.get(url) as res:
            json = await res.json()
            if json[0]['category'] == '0':
                error = "❌ No data for this session! If this session only finished recently, please try again in a few minutes"
                await call.message.answer(error)
            else:

                drivers = [(int(driver['position']),
                            f"{driver['first_name']} {driver['last_name']} ({driver['points']}) ({driver['team_name']})")
                           for driver in json]
                drivers = sorted(drivers, key=lambda x: x[0])
                messages = [f"🏅 {position[0]}. {position[1]}" for position in drivers]
                result_msg = f"🏆 The 2022 MOTOGP driver standings : :\n\n" + "\n".join(messages)
                await call.message.answer(result_msg)


@dp.callback_query_handler(lambda call: "standing-Moto3" in call.data)
async def moto3_standing(call: types.CallbackQuery):
    category = call.data.split("-")[1]
    async with ClientSession() as session:
        url = f"{Config['api_url']}/motoriderstanding?year=2022&category=moto3&token={Config['api_token']}"
        async with session.get(url) as res:
            json = await res.json()
            if json[0]['category'] == '0':
                error = "❌ No data for this session! If this session only finished recently, please try again in a few minutes"
                await call.message.answer(error)
            else:

                drivers = [(int(driver['position']),
                            f"{driver['first_name']} {driver['last_name']} ({driver['points']}) ({driver['team_name']})")
                           for driver in json]
                drivers = sorted(drivers, key=lambda x: x[0])
                messages = [f"🏅 {position[0]}. {position[1]}" for position in drivers]
                result_msg = f"🏆 The 2022 MOTO3 driver standings : :\n\n" + "\n".join(messages)
                await call.message.answer(result_msg)


@dp.callback_query_handler(lambda call: "standing-Moto2" in call.data)
async def moto2_standing(call: types.CallbackQuery):
    category = call.data.split("-")[1]
    async with ClientSession() as session:
        url = f"{Config['api_url']}/motoriderstanding?year=2022&category=moto2&token={Config['api_token']}"
        async with session.get(url) as res:
            json = await res.json()
            if json[0]['category'] == '0':
                error = "❌ No data for this session! If this session only finished recently, please try again in a few minutes"
                await call.message.answer(error)
            else:

                drivers = [(int(driver['position']),
                            f"{driver['first_name']} {driver['last_name']} ({driver['points']}) ({driver['team_name']})")
                           for driver in json]
                drivers = sorted(drivers, key=lambda x: x[0])
                messages = [f"🏅 {position[0]}. {position[1]}" for position in drivers]
                result_msg = f"🏆 The 2022 MOTO2 driver standings : :\n\n" + "\n".join(messages)
                await call.message.answer(result_msg)


@dp.message_handler(lambda message: "🏆StandingsMotoGP" in message.text)
async def motogp_list_season_year(message: types.Message):
    category = "MotoGP"
    welcome_msg = "Hi " + str(
        message.from_user.first_name) + " select the season year : \n\n"
    buttons = button.button_list_year(category)
    await message.reply(welcome_msg, reply_markup=buttons)
    await message.delete()


@dp.message_handler(lambda message: "🏆StandingsMoto2" in message.text)
async def motogp_list_season_year(message: types.Message):
    category = "Moto2"
    welcome_msg = "Hi " + str(
        message.from_user.first_name) + " select the season year : \n\n"
    buttons = button.button_list_year(category)
    await message.reply(welcome_msg, reply_markup=buttons)
    await message.delete()


@dp.message_handler(lambda message: "🏆StandingsMoto3" in message.text)
async def motogp_list_season_year(message: types.Message):
    category = "Moto3"
    welcome_msg = "Hi " + str(
        message.from_user.first_name) + " select the season year : \n\n"
    buttons = button.button_list_year(category)
    await message.reply(welcome_msg, reply_markup=buttons)
    await message.delete()


executor.start_polling(dp)
