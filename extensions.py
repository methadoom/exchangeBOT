import requests
import json
from config import keys

class ExchangeException(Exception):
    pass

class ExchangeB:
    @staticmethod
    def exchange(quote: str, base: str, amount: str):
        if quote == base:
            raise ExchangeException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExchangeException(f'Не удалось обработать валюты {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExchangeException(f'Не удалось обработать валюты {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ExchangeException(f'Не удалось обрабоать количество {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base