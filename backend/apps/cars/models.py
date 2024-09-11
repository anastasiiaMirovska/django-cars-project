from datetime import datetime

from django.core import validators as V
from django.db import models

from core.models import BaseModel

from apps.auth.serializers import UserModel
from apps.cars.choices.body_type_choices import BodyTypeChoices
from apps.cars.choices.currency_choices import CurrencyChoices
from apps.cars.choices.engine_type_choices import EngineTypeChoices
from apps.cars.choices.region_choices import RegionChoices
from apps.cars.choices.transmission_type_choices import TransmissionTypeChoices
from apps.cars.managers import CarManager


class CarBrandModel(models.Model):
    class Meta:
        db_table = 'car_brands'
        ordering = ['name']

    name = models.CharField(unique=True, max_length=20, validators=(V.MinLengthValidator(1),))


class CarModelModel(models.Model):
    class Meta:
        db_table = 'car_models'
        ordering = ['-brand']
        unique_together = ('name', 'brand')

    name = models.CharField(max_length=20, validators=(V.MinLengthValidator(1),))
    brand = models.ForeignKey(CarBrandModel, on_delete=models.CASCADE, related_name='models')


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'
        ordering = ('-id',)

    # price = models.IntegerField(validators=(V.MinValueValidator(0), V.MaxValueValidator(100_000_000)))
    # currency = models.CharField(max_length=3, choices=CurrencyChoices.choices, blank=False, null=False)
    year = models.IntegerField(validators=(V.MinValueValidator(1990), V.MaxValueValidator(datetime.now().year)))
    is_used = models.BooleanField(default=False)
    body_type = models.CharField(max_length=9, choices=BodyTypeChoices.choices, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    edit_attempts = models.IntegerField(default=0, validators=(V.MaxValueValidator(3),))

    car_model = models.ForeignKey(CarModelModel, on_delete=models.CASCADE, related_name='cars')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_cars')

    objects = CarManager()


class CarProfileModel(BaseModel):
    class Meta:
        db_table = 'car_profile'
        ordering = ['id']

    city = models.CharField(max_length=20, validators=(V.MinLengthValidator(1),))
    region = models.CharField(max_length=20, choices=RegionChoices.choices, validators=(V.MinLengthValidator(1),))
    mileage = models.IntegerField(validators=(V.MinValueValidator(0), V.MaxValueValidator(999_999_999)))
    engine_type = models.CharField(max_length=20, choices=EngineTypeChoices.choices, blank=False, null=False)
    engine_volume = models.FloatField(validators=(V.MinValueValidator(0.1), V.MaxValueValidator(100)))
    transmission_type = models.CharField(max_length=20, choices=TransmissionTypeChoices.choices, blank=False, null=False)
    description = models.TextField(max_length=255)
    color = models.CharField(max_length=20)
    owner_amount = models.IntegerField(default=0, validators=(V.MaxValueValidator(30),))

    car = models.OneToOneField(CarModel, on_delete=models.CASCADE, related_name='profile')


class CarPriceModel(models.Model):
    class Meta:
        db_table = 'car_price'
        ordering = ['id']
    initial_price = models.DecimalField(max_digits=20, decimal_places=5, validators=[V.MinValueValidator(1), ])
    initial_currency = models.CharField(max_length=3, choices=CurrencyChoices.choices)

    price_in_USD = models.DecimalField(max_digits=20, decimal_places=5)
    price_in_EUR = models.DecimalField(max_digits=20, decimal_places=5)
    price_in_UAH = models.DecimalField(max_digits=20, decimal_places=5)

    car = models.OneToOneField(CarModel, on_delete=models.CASCADE, related_name='price')

    def save(self, *args, **kwargs):
        usd_rate_sale = CurrencyModel.objects.get(currency='USD').sale_price
        usd_rate_buy = CurrencyModel.objects.get(currency='USD').buy_price
        eur_rate_sale = CurrencyModel.objects.get(currency='EUR').sale_price
        eur_rate_buy = CurrencyModel.objects.get(currency='EUR').buy_price

        if self.initial_currency == 'USD':
            self.price_in_USD = self.initial_price
            self.price_in_EUR = self.initial_price * usd_rate_buy / eur_rate_sale
            self.price_in_UAH = self.initial_price * usd_rate_buy
        elif self.initial_currency == 'EUR':
            self.price_in_EUR = self.initial_price
            self.price_in_USD = self.initial_price * eur_rate_buy / usd_rate_sale
            self.price_in_UAH = self.initial_price * eur_rate_buy
        elif self.initial_currency == 'UAH':
            self.price_in_UAH = self.initial_price
            self.price_in_USD = self.initial_price / usd_rate_sale
            self.price_in_EUR = self.initial_price / eur_rate_sale

        super().save(*args, **kwargs)


class CurrencyModel(models.Model):
    class Meta:
        db_table = 'currency'
        ordering = ['id']
    currency = models.CharField(max_length=3, choices=CurrencyChoices.choices, unique=True)
    buy_price = models.DecimalField(max_digits=10, decimal_places=5, validators=(V.MinValueValidator(0.1), ),)
    sale_price = models.DecimalField(max_digits=10, decimal_places=5, validators=(V.MinValueValidator(0.1), ))
    last_update = models.DateTimeField(auto_now=True)


class ViewStatisticsModel(models.Model):
    class Meta:
        db_table = 'views'
        ordering = ('id',)

    viewed_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='views')
