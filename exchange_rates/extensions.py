from config import TOKEN, keys
import requests
import json


class APIException(Exception):
    pass


class Convert:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Нельзя конверитировать {base} в {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество конвертируемой валюты должно быть числом.\n'
                               f'Введено {amount}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюты {base} нет в списке конвертируемых.\n'
                               f'Посмотреть список доступных валют /values')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюты {quote} нет в списке конвертируемых.\n'
                               f'Посмотреть список доступных валют /values')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_result = json.loads(r.content)[keys[quote]]
        return float(total_result)