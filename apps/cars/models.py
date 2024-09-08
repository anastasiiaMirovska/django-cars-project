from datetime import datetime

from django.core import validators as V
from django.db import models

from core.models import BaseModel

from apps.auth.serializers import UserModel
from apps.cars.choices.body_type_choices import BodyTypeChoices
from apps.cars.choices.currency_choices import CurrencyChoices
from apps.cars.choices.engine_type_choices import EngineTypeChoices
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
        ordering = ['brand']
        unique_together = ('name', 'brand')
    name = models.CharField(max_length=20, validators=(V.MinLengthValidator(1),))
    brand = models.ForeignKey(CarBrandModel, on_delete=models.CASCADE, related_name='models')


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'
        ordering = ('-id',)

    # ToDo розібратись чи треба валідацію максимальної ціни
    price = models.IntegerField(validators=(V.MinValueValidator(0), V.MaxValueValidator(1_000_000)))
    currency = models.CharField(max_length=3, choices=CurrencyChoices.choices, blank=False, null=False)
    year = models.IntegerField(validators=(V.MinValueValidator(1990), V.MaxValueValidator(datetime.now().year)))
    body_type = models.CharField(max_length=9, choices=BodyTypeChoices.choices, blank=False, null=False)
    car_model = models.ForeignKey(CarModelModel, on_delete=models.CASCADE, related_name='cars')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_cars')

    objects = CarManager()


class CarProfileModel(BaseModel):
    class Meta:
        db_table = 'car_profile'
        ordering = ['id']

    city = models.CharField(max_length=20, validators=(V.MinLengthValidator(1),))
    region = models.CharField(max_length=20, validators=(V.MinLengthValidator(1),))
    mileage = models.IntegerField(validators=(V.MinValueValidator(0),))
    is_used = models.BooleanField(default=False)
    engine_type = models.CharField(max_length=20, choices=EngineTypeChoices.choices, blank=False, null=False)
    transmission_type = models.CharField(max_length=20, choices=TransmissionTypeChoices, blank=False, null=False)
    description = models.TextField(max_length=255)
    car = models.OneToOneField(CarModel, on_delete=models.CASCADE, related_name='profile')

