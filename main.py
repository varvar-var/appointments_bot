import telebot
import threading
from datetime import date, timedelta
from json_core import add_appointment, read_json, write_json, add_review
from keyboards import time_keyboard, dates_keyboard, service_keyboard
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

reminders = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')

@bot.message_handler(commands=['make_appointment'])
def make_appointment(message):
    bot.send_message(message.chat.id, 'Выберите день для записи', reply_markup=service_keyboard())

@bot.message_handler(commands=['help'])
def handle_help(message): 
    bot.send_message(message.chat.id, '/make_appointment - Записаться на услугу, /add_rewiew - Добавить отзыв, /set_name - Сохранить имя') 

@bot.message_handler(commands=['set_name'])
def handler_set_name(message):
    bot.send_message(message.chat.id, "Введите свое имя")
    bot.register_next_step_handler(message, save_name)

@bot.message_handler(commands=['add_review'])
def add_rewiew(message):
    bot.send_message(message.chat.id, "Введите свой отзыв")
    bot.register_next_step_handler(message, save_reviews) 

def set_timer(client_id, appointment_date):
    try:
        if client_id in reminders:
            reminders[client_id].cancel()
        date_object = date.fromisoformat(appointment_date)
        reminder_date = date_object + timedelta(days=30)
        today = date.today()
        time = reminder_date - today
        delta = time.total_seconds()
        if delta <= 0:
            return
        timer = threading.Timer(delta, send_reminder, [client_id])
        timer.start()
        reminders[client_id] = timer
        print(f"Для пользователя{client_id} установлен таймер на {reminder_date}")
    except Exception as e:
        print(f"Ошибка при установке таймера: {e}")    

def send_reminder(client_id):
    try:
        message = 'С вашего последнего визита прошел месяц!Используйте /make_appointment для повторной записи!'
        bot.send_message(client_id, message)
        print(f"Отправили пользователю {client_id} напоминание.")
        if client_id in reminders:
            reminders[client_id]
    except Exception as e:
        print(f"Ошибка при отправке пользователю: {e}")    
    
def load_reminders():
    try:
        data = read_json()
        appointments = data['appointments'] 
        last_appointments = {}
        for i in appointments:
            client_id = i["client"]
            date = i["date"]
            if client_id not in last_appointments or date > last_appointments[client_id]:
                last_appointments[client_id] =  date
        for client_id, date in last_appointments.items():
            set_timer(client_id, date)
        print('Напоминания загружены')    
    except Exception as e:
        print(f"Ошибка при загрузке напоминаний: {e}")
              
def save_reviews(message):
    add_review(str(message.chat.id), message.text)
    bot.send_message(message.chat.id, "Ваш отзыв сохранен")

def save_name(message):
    user_data = read_json()
    user_data["clients"][str(message.chat.id)] = message.text
    write_json(user_data)
    bot.send_message(message.chat.id, "Ваше имя сохраненно")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data.startswith("service_"):
        service = call.data.split("_")[1]
        bot.send_message(call.message.chat.id, f'Вы выбрали: {service}', reply_markup=dates_keyboard(service))
    if call.data.startswith("day_"):
        _, service, day = call.data.split("_")
        bot.send_message(call.message.chat.id, f'Вы выбрали: {day}', reply_markup=time_keyboard(day, service))
    if call.data.startswith("appointment_"):
        _, service, day, time = call.data.split("_")
        add_appointment(service, day, time, str(call.message.chat.id))
        set_timer(call.message.chat.id, day)
        bot.send_message(call.message.chat.id, f'Вы выбрали: {service}, {day}, {time}')        

@bot.message_handler(func=lambda message: True)  
def handle_all(message):
    bot.send_message(message.chat.id, 'Я вас не понял.')    

if __name__ == '__main__':
    load_reminders()
    bot.polling(none_stop=True)