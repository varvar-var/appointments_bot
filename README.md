# appointments_bot 🤖

Бот для записи на услуги. Пользователь имеет возможность выбрать необходимую дату и время, после чего информация сохраняется в файл. Также есть возможность оставить отзыв.

## 🚀 Функционал
- `/start` — приветствие
- `/make_appointment` — выбор дня для записи
- `/help` - справка
- `/set_name` - ввод имени
- `/add_review` - добавление отзыва

## 🛠 Технологии
- Python 3.12
- pyTelegramBotAPI (telebot)
- threading
- datetime

## 📦 Установка и запуск
1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:varvar-var/appointments_bot.git
   cd appointments_bot
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` в корневой папке и добавьте токен:
   ```
   BOT_TOKEN=ваш_токен_от_BotFather
   ```

4. Запустите бота:
   ```bash
   python bot.py
   ```

## 👨‍💻 Автор
Топоркова Варвара — https://github.com/varvar-var
