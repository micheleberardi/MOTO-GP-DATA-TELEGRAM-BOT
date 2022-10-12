from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def button_menu():
    keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add("🏁MotoGP", "🏁Moto2", "🏁Moto3",
                                                                                       "👱🏼RiderMotoGP",
                                                                                       "👱🏼RiderMoto2",
                                                                                       "👱🏼RiderMoto3",
                                                                                       "🏆StandingsMotoGP",
                                                                                       "🏆StandingsMoto2",
                                                                                       "🏆StandingsMoto3")
    return keyboard1


def button_list_circuits(category):
    button1 = InlineKeyboardButton(text="🇦🇹Red Bull Ring", callback_data="circuits-" + str(category) + "-austria-13")
    button2 = InlineKeyboardButton(text="🇬🇧Silverstone", callback_data="circuits-" + str(category) + "-uk-12")
    button3 = InlineKeyboardButton(text="🇸🇲SanMarino", callback_data="circuits-" + str(category) + "-it-14")
    button4 = InlineKeyboardButton(text="🇪🇸Aragon", callback_data="circuits-" + str(category) + "-es-15")
    button5 = InlineKeyboardButton(text="🇯🇵Motul ", callback_data="circuits-" + str(category) + "-jp-16")
    button6 = InlineKeyboardButton(text="🇹🇭Thailand ", callback_data="circuits-" + str(category) + "-th-17")
    button7 = InlineKeyboardButton(text="🇦🇺Australia ", callback_data="circuits-" + str(category) + "-au-18")
    button8 = InlineKeyboardButton(text="🇲🇾Malaysia ", callback_data="circuits-" + str(category) + "-ma-19")
    button9 = InlineKeyboardButton(text="🇪🇸Valencia ", callback_data="circuits-" + str(category) + "-va-20")
    keyboard_inline = InlineKeyboardMarkup(resize_keyboard=True).add(button1, button2,button3,button4,button5,button6,button7,button8,button9)
    return keyboard_inline


def button_list_sessions_motogp(category, event, year):
    button14 = InlineKeyboardButton(text="🏁FP1",
                                    callback_data="sessions-" + str(category) + str("-FreePracticeNr1-") + str(
                                        event) + str("-") + str(year))
    button15 = InlineKeyboardButton(text="🏁FP2",
                                    callback_data="sessions-" + str(category) + str("-FreePracticeNr2-") + str(
                                        event) + str("-") + str(year))
    button16 = InlineKeyboardButton(text="🏁FP3",
                                    callback_data="sessions-" + str(category) + str("-FreePracticeNr3-") + str(
                                        event) + str("-") + str(year))
    button17 = InlineKeyboardButton(text="🏁FP4",
                                    callback_data="sessions-" + str(category) + str("-FreePracticeNr4-") + str(
                                        event) + str("-") + str(year))
    button18 = InlineKeyboardButton(text="🏁Q1",
                                    callback_data="sessions-" + str(category) + str("-QualifyingNr1-") + str(
                                        event) + str("-") + str(year))
    button19 = InlineKeyboardButton(text="🏁Q2",
                                    callback_data="sessions-" + str(category) + str("-QualifyingNr2-") + str(
                                        event) + str("-") + str(year))
    button20 = InlineKeyboardButton(text="🏁RACE",
                                    callback_data="sessions-" + str(category) + str("-Race-") + str(event) + str(
                                        "-") + str(year))
    keyboard_inline = InlineKeyboardMarkup(resize_keyboard=True).add(button14, button15, button16, button17, button18,
                                                                     button19, button20)
    return keyboard_inline


def button_list_rider_motogp(drivers, category):
    button_list = []
    for json in drivers:
        if json['category'] == category:
            rider_name = json['rider_name']
            rider_surname = json['rider_surname']
            r = rider_name + " " + rider_surname
            rider_number = json['rider_number']
            button = InlineKeyboardButton(text=r, callback_data="rider_number-" + str(rider_number))
            button_list.append(button)
    print(button_list)
    keyboard_inline = InlineKeyboardMarkup(resize_keyboard=True).add(*button_list)
    return keyboard_inline


def button_list_year(category):
    button1 = InlineKeyboardButton(text="2022", callback_data="standing-"+str(category)+"-2022")
    keyboard_inline = InlineKeyboardMarkup(resize_keyboard=True).add(button1)
    return keyboard_inline
