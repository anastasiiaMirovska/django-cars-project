from django.db.transaction import atomic

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
            'is_used',
            'body_type',
            'car_model',
            'created_at',
            'updated_at',
            'profile',
        )

    @atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        request = self.context.get('request', None)
        validated_data['user'] = request.user
        car = CarModel.objects.create_car(**validated_data)
        CarProfileModel.objects.create(car=car, **profile_data)
        return car


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

