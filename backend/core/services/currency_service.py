import json
from datetime import timezone
from decimal import Decimal
from urllib import error, request

from django.core.exceptions import ObjectDoesNotExist

import requests
from configs.celery import app

from core.exceptions.currency_exception import CurrencyException

from apps.cars.models import CarPriceModel, CurrencyModel

PRIVATBANK_API_URL = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'

# @app.task

class CurrencyService:

    @staticmethod
    @app.task
    def fetch_currency():
        response = requests.get(PRIVATBANK_API_URL)

        if response.status_code == 200:
            data = response.json()
            for item in data:
                currency = item['ccy']
                if currency in ['USD', 'EUR']:
                    buy_price = Decimal(item['buy'])
                    sale_price = Decimal(item['sale'])

                    CurrencyModel.objects.update_or_create(
                        currency=currency,
                        defaults={
                            'buy_price': buy_price,
                            'sale_price': sale_price
                        }
                    )
            CurrencyService.update_car_prices.delay()
        else:
            raise CurrencyException

    @staticmethod
    @app.task
    def update_car_prices():
        usd_rate_sale = CurrencyModel.objects.get(currency='USD').sale_price
        usd_rate_buy = CurrencyModel.objects.get(currency='USD').buy_price
        eur_rate_sale = CurrencyModel.objects.get(currency='EUR').sale_price
        eur_rate_buy = CurrencyModel.objects.get(currency='EUR').buy_price

        for car_price in CarPriceModel.objects.all():
            if car_price.initial_currency == 'USD':
                car_price.price_in_USD = car_price.initial_price
                car_price.price_in_EUR = car_price.initial_price * usd_rate_buy / eur_rate_sale
                car_price.price_in_UAH = car_price.initial_price * usd_rate_buy
            elif car_price.initial_currency == 'EUR':
                car_price.price_in_EUR = car_price.initial_price
                car_price.price_in_USD = car_price.initial_price * eur_rate_buy / usd_rate_sale
                car_price.price_in_UAH = car_price.initial_price * eur_rate_buy
            elif car_price.initial_currency == 'UAH':
                car_price.price_in_UAH = car_price.initial_price
                car_price.price_in_USD = car_price.initial_price / usd_rate_sale
                car_price.price_in_EUR = car_price.initial_price / eur_rate_sale
            car_price.save()
