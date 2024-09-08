from rest_framework import serializers

from apps.cars.models import CarBrandModel, CarModel, CarModelModel, CarProfileModel
from apps.users.serializers import ProfileSerializer


class CarProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarProfileModel
        fields = (
            'id',
            'city',
            'region',
            'mileage',
            'is_used',
            'engine_type',
            'transmission_type',
            'description',
        )


class CarSerializer(serializers.ModelSerializer):
    profile = CarProfileSerializer()
    car_model = CarModelModel()

    class Meta:
        model = CarModel
        fields = (
            'id',
            'price',
            'currency',
            'year',
            'body_type',
            'car_model',
            'created_at',
            'updated_at',
            'profile'
        )


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrandModel
        fields = ('name',)


class CarModelSerializer(serializers.ModelSerializer):
    brand = CarBrandSerializer()

    class Meta:
        model = CarModelModel
        fields = (
            'name',
            'brand'
        )

