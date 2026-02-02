import telebot
from telebot import types
import random

TOKEN = '8471977033:AAHxDbmW8p1KPqkvXH6ki5CKNaS_T4XQDxY'
bot = telebot.TeleBot(TOKEN)


CARS = {
    'Тойота Камри': 'тойота/камру.jpeg',
    'BMW 3 Series': 'бмв/bmw-m3.jpg',
    'Mercedes S-Class': 'мерседес/мерседес.jpeg',
    'Audi A6': 'ауди/а6.jpg',
    'Lexus RX': 'лехсус/рх.jpg',
    'Tesla Model S': 'тесла/с.webp',
    'Porsche 911': 'порш/911.jpeg',
    'Range Rover': 'ренч/рунч.jpeg',
    'Honda Civic': 'хонда/кирп.webp',
    'Hyundai Sonata': 'хундай/соната.jpg'
}

CARS_INFO = {
    'Тойота Камри': "Объёму: 2.5\nӨңү: Кара\nЖылы: 2020\nСостояние: Жаңы\nКоробка: Автомат",
    'BMW 3 Series': "Объёму: 3.0\nӨңү: Көк\nЖылы: 2019\nСостояние: Идеал\nКоробка: Автомат",
    'Mercedes S-Class': "Объёму: 3.5\nӨңү: Кара\nЖылы: 2021\nСостояние: Люкс\nКоробка: Автомат",
    'Audi A6': "Объёму: 2.0 Turbo\nӨңү: Кара\nЖылы: 2018\nСостояние: Жакшы\nКоробка: Автомат",
    'Lexus RX': "Объёму: 3.5\nӨңү: Ак\nЖылы: 2020\nСостояние: Идеал\nКоробка: Автомат",
    'Tesla Model S': "Объёму: 4.4\nӨңү: Кара\nЖылы: 2022\nЗапас хода: 550 км\nСостояние: Жаңы",
    'Porsche 911': "Объёму: 3.0 Turbo\nӨңү: Боз\nЖылы: 2017\nСостояние: Спорт\nПробег: 25,000 км",
    'Range Rover': "Объёму: 4.4\nӨңү: Кара\nЖылы: 2019\nСостояние: Люкс\nПробег: 60,000 км",
    'Honda Civic': "Объёму: 1.8\nӨңү: Каричновый\nЖылы: 2018\nСостояние: Жакшы\nПробег: 70,000 км",
    'Hyundai Sonata': "Объёму: 2.0\nӨңү: Кара\nЖылы: 2017\nСостояние: Орточо\nПробег: 80,000 км"
}


@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Бардык моделдер', callback_data='list_all'))
    kb.add(types.InlineKeyboardButton('Случайная машина', callback_data='random'))
    kb.add(types.InlineKeyboardButton('Переводчик 🌐', callback_data='translate'))  
    kb.add(types.InlineKeyboardButton('Настройки', callback_data='settings'))

    text = (
        "Саламатсызбы! Мен Машина ботумун 🚗\n\n"
        "Командалар:\n"
        " - /models — моделдерди көрүү\n"
        " - /random — кокус машина\n\n"
        "Төмөндөгү кнопкалардан тандаңыз:"
    )

    bot.send_message(message.chat.id, text, reply_markup=kb)


@bot.message_handler(commands=['models'])
def list_models_cmd(message):
    send_models_keyboard(message.chat.id)

@bot.message_handler(commands=['random'])
def random_car_cmd(message):
    model = random.choice(list(CARS.keys()))
    send_car_info(message.chat.id, model)


def send_models_keyboard(chat_id):
    kb = types.InlineKeyboardMarkup(row_width=2)
    for model in CARS.keys():
        kb.add(types.InlineKeyboardButton(model, callback_data=f'model::{model}'))
    kb.add(types.InlineKeyboardButton('Случайная', callback_data='random'))
    bot.send_message(chat_id, "Моделдерден бирин танда:", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data

    if data == 'list_all':
        send_models_keyboard(call.message.chat.id)

    elif data == 'random':
        model = random.choice(list(CARS.keys()))
        send_car_info(call.message.chat.id, model)

    elif data.startswith('model::'):
        model = data.split('::', 1)[1]
        send_car_info(call.message.chat.id, model)

    elif data == 'translate':     
        bot.send_message(call.message.chat.id, "Кайсы текстти котороюн? 🌐")
        bot.register_next_step_handler(call.message, do_translate)

    elif data == 'settings':
        bot.answer_callback_query(call.id, "Настройкаларды файлдан өзгөртө аласыз.")

    else:
        bot.answer_callback_query(call.id, "Белгисиз буйрук")


def send_car_info(chat_id, model_name):
    url = CARS.get(model_name)
    info = CARS_INFO.get(model_name, "Маалымат жок")

    caption = f"📌 Модель: *{model_name}*\n\n{info}"

    try:
        if url:
            bot.send_photo(chat_id, open(url, 'rb'), caption=caption, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, caption, parse_mode="Markdown")

    except Exception as e:
        bot.send_message(chat_id, caption + f"\n\nСүрөт жүктөлбөдү: {e}")


def do_translate(message):
    text = message.text
    try:
        result = message(source='auto', target='ru').translate(text)
        bot.send_message(message.chat.id, f"📌 Котормосу:\n{result}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ката чыкты: {e}")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    text = message.text.strip().lower()

    matches = [m for m in CARS.keys() if text in m.lower()]

    if matches:
        kb = types.InlineKeyboardMarkup()
        for m in matches:
            kb.add(types.InlineKeyboardButton(m, callback_data=f'model::{m}'))

        bot.send_message(
            message.chat.id,
            f"Табылды: {', '.join(matches)}\nТандаңыз:",
            reply_markup=kb
        )
    else:
        bot.send_message(message.chat.id, "Тапылган жок. /models колдонуп көрүңүз.")


if __name__ == '__main__':
    print("Бот иштеп жатат...")
    bot.infinity_polling()
