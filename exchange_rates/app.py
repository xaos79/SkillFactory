import telebot
from config import TOKEN, keys
from extensions import Convert, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message: telebot.types.Message):
    text = 'Данный бот предназначен для конвертации валюты.\n' \
           'Введите сообщение в виде:\n' \
           '<имя валюты, цену которой Вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.\n' \
           'Пример: рубль доллар 1\n' \
           'Для прсомотра доступных валют введите: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text += f'\n{key}'

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split()

        if len(value) != 3:
            raise APIException('Неверное число значений в запросе.')

        base, quote, amount = message.text.split()
        total_result = Convert.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка сервера.\n{e}')

    else:
        text = f'{amount} {keys[base]} = {float(amount) * total_result} {keys[quote]}'
        bot.reply_to(message, text)
        print(text)


bot.polling()
