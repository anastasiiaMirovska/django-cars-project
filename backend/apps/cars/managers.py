from django.db import models
from django.db.models import Avg, Q

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class CarManager(models.Manager):
    def create_car(self, user, **kwargs):
        if not user.is_premium and self.filter(user=user).count() >= 1:
            raise ValidationError("Non-premium users can only add one car.")
        return self.create(user=user, **kwargs)

    # def average_price_statistics(self, car):
    #     car_is_used = car.is_used
    #     car_model = car.car_model_id
    #
    #     cars = self.filter(car_model_id=car_model, is_used=car_is_used).exclude(pk=car.id)
    #     average_price = cars.aggregate(Avg('price'))['price__avg']
    #     return average_price
    #
    # def average_region_price_statistics(self, car):
    #     car_is_used = car.is_used
    #     car_model = car.car_model_id
    #     region = car.profile.region
    #
    #     cars = self.filter(car_model_id=car_model, is_used=car_is_used, profile__region=region).exclude(pk=car.id)
    #     average_price = cars.aggregate(Avg('price'))['price__avg']
    #     return average_price
