import telebot
from config import keys, TOKEN
from extensions import ExchangeException, ExchangeB

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет! Я Бот-Конвертер валют и я могу:  \n- Показать список доступных валют через команду /values \
    \n- Вывести конвертацию валюты через команду <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n \
- Напомнить, что я могу через команду /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество валюты>\nУвидеть список всез доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def get_change(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) !=3:
            raise ExchangeException('Слишком нмого параметров')

        quote, base, amount = values
        total_base = ExchangeB.get_change(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Переводим {base} в {quote}\n{amount} у.е. = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()