import telebot
from config import keys, TOKEN
from utils import ConversionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

# Объявление keys не требуется здесь, если оно уже есть в config.py

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n\n'\
           'Увидить список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.reply_to(message, text)

if __name__ == '__main__':
    bot.polling(none_stop=True)

