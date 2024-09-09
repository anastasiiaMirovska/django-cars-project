from django.db.transaction import atomic

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.services.email_service import EmailService
from core.services.word_validation_service import validate_inappropriate_language

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


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrandModel
        fields = ('id', 'name',)


class CarModelSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=CarBrandModel.objects.all())

    class Meta:
        model = CarModelModel
        fields = (
            'id',
            'name',
            'brand'
        )

    def create(self, validated_data):
        brand = validated_data.pop('brand')
        if isinstance(brand, int):  # Якщо переданий ID, отримуємо відповідний бренд.
            brand = CarBrandModel.objects.get(id=brand)
        validated_data['brand'] = brand
        return super().create(validated_data)


class CarSerializer(serializers.ModelSerializer):
    profile = CarProfileSerializer()
    car_model = serializers.PrimaryKeyRelatedField(queryset=CarModelModel.objects.all())

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
            'edit_attempts',
            'is_active'
        )

    def validate(self, data):

        request = self.context.get('request', None)
        instance = self.instance

        profile_data = data.get('profile', {})
        inappropriate_fields = validate_inappropriate_language(profile_data)

        if instance:
            instance.edit_attempts += 1

            if inappropriate_fields:
                if instance.edit_attempts >= 3:
                    instance.is_active = False
                    instance.save()
                    EmailService.check_bad_words_email(user_id=request.user.id, car_id=instance.id)
                    raise ValidationError("Too many failed attempts. The listing has been deactivated.")

                instance.save()
                raise ValidationError(
                    f"Forbidden words detected in fields: {', '.join(inappropriate_fields)}. Attempts remaining: {3 - instance.edit_attempts}."
                )

            instance.edit_attempts = 0
            instance.is_active = True

        return data

    @atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        # car_model = validated_data.pop('car_model')
        request = self.context.get('request', None)
        validated_data['user'] = request.user

        car_model = validated_data.pop('car_model')
        if isinstance(car_model, int):
            car_model = CarModelModel.objects.get(id=car_model)
        validated_data['car_model'] = car_model
        is_active = False
        if not validate_inappropriate_language(profile_data):
            is_active = True

        car = CarModel.objects.create_car(**validated_data, is_active=is_active)
        CarProfileModel.objects.create(car=car, **profile_data)
        car.save()

        return car

    @atomic
    def update(self, instance, validated_data):
        return instance

