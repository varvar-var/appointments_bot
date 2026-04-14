from datetime import date, timedelta
from json_core import read_json
from telebot import types


def service_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    service = ["Диагностика", "Лечение", "Реабилитация", "Паллиативная помощь", "Медицинская помощь"]
    for i in service:
        button = types.InlineKeyboardButton(text=i, callback_data=f"service_{i}")    
        keyboard.add(button)
    return keyboard

def time_keyboard(day, service):
    keyboard = types.InlineKeyboardMarkup()
    time = ["10:00", "12:00", "15:00", "17:00"]
    data = read_json()
    for app in data["appointments"]:
        if day == app['date']:
            time.remove(app["time"])
    for i in time:
        button = types.InlineKeyboardButton(text=i, callback_data=f"appointment_{service}_{day}_{i}")    
        keyboard.add(button)
    return keyboard

def dates_keyboard(service):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(7):
        day = str(date.today() + timedelta(days=3 + i))
        button = types.InlineKeyboardButton(text=day, callback_data=f"day_{service}_{day}")
        keyboard.add(button)
    return keyboard    