import telebot
import json

import weather
import npu


with open("secret.json", "rt") as file:
    keys = json.loads(file.read())
    bot_key = keys["bot_key"]

bot = telebot.TeleBot(bot_key)

# Тело бота

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Я kiselBot, персональный ассистент (правда пока только стажируюсь),'
                                      f' приятно познакомиться, {message.from_user.first_name}.')
    bot.send_message(message.chat.id, 'Можем с тобой поболтать. Если не знаешь о чем, то просто напиши /help,'
                                      ' чтобы узнать мои основные функции.')


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, npu.help_bot())


@bot.message_handler(content_types=['document', 'audio', 'photo', 'sticker', 'video'])
def send_echo(message):
    bot.send_message(message.chat.id, 'Прости, но я работаю пока что только с текстовыми сообщениями')


@bot.message_handler(content_types=['text'])
def send_echo(message):
    mes = npu.cleaner(message.text)
    if mes == 'привет':
        answer = npu.botnpu(mes)
    else:
        try:
            answer = weather.get_weather_data(mes)
        except (weather.pyowm.commons.exceptions.NotFoundError, weather.pyowm.commons.exceptions.APIRequestError):
            answer = npu.botnpu(mes)
    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
