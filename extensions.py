import json
import requests
from config import keys

class ConversionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str, keys: dict):
        if quote == base:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество {amount}.')

        response = requests.get(f'https://v6.exchangerate-api.com/v6/834f8a53547a4e214410540f/latest/USD{quote_ticker}/{base_ticker}/{amount}')
        if response.status_code != 200:
            raise ConversionException('Ошибка запроса к API.')

        total_base = json.loads(response.content).get(base_ticker)
        return total_base