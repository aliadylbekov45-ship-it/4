import telebot
from telebot import types
import random

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

# /start командасы
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('Привет')
    b2 = types.KeyboardButton('инфа')
    b3 = types.KeyboardButton('анекдот')
    b4 = types.KeyboardButton('переводчик')
    keyboard.add(b1, b2, b3, b4)

    bot.send_message(
        message.chat.id,
        "Привет! Я хакер 🤖\nВыбери действие:",
        reply_markup=keyboard
    )

# Основная логика
@bot.message_handler(func=lambda message: True)
def reply(message):
    text = message.text.lower()

    if 'привет' in text:
        bot.send_message(message.chat.id, 'Привет! Я хакер, чем могу помочь? 💻')

    elif 'инфа' in text:
        bot.send_message(message.chat.id, 'Ты крутой 😎')

    elif 'пока' in text:
        bot.send_message(message.chat.id, 'До встречи! 👋')

    elif 'как дела' in text or 'как ты' in text:
        bot.send_message(message.chat.id, 'Отлично! А у тебя как? 😎')

    elif 'кто ты' in text:
        bot.send_message(message.chat.id, 'Я бот-хакер, созданный для помощи тебе 🤖')

    elif 'что умеешь' in text:
        bot.send_message(message.chat.id, 'Я умею отвечать на сообщения и показывать кнопки 💡')

    elif 'анекдот' in text:
        bot.send_message(message.chat.id, '2+2=4 болот экен 😂')

    elif 'время' in text:
        from datetime import datetime
        now = datetime.now().strftime('%H:%M:%S')
        bot.send_message(message.chat.id, f'Сейчас {now} ⏰')

    elif 'дата' in text:
        from datetime import datetime
        today = datetime.now().strftime('%d.%m.%Y')
        bot.send_message(message.chat.id, f'Сегодня {today} 📅')

    # ---------------- ПЕРЕВОДЧИК ----------------
    elif 'переводчик' in text:
        bot.send_message(message.chat.id,
                         "Напиши текст, я переведу автоматически 🇰🇬 ↔ 🇷🇺")

    else:
        # Автоматический перевод
        try:
            translated = message.translate(message.text, dest='ru').text

            # Если текст на русском → переводим в кыргызча
            if message.text == message.translate(message.text, dest='ky').text:
                translated = message.translate(message.text, dest='ky').text
            else:
                translated = message.translate(message.text, dest='ru').text

            bot.send_message(message.chat.id, f"Перевод: {translated}")
        except:
            bot.send_message(message.chat.id, 'Не смог перевести 🤔 Попробуй другой текст.')

bot.polling(none_stop=True)
