from django.db.models import Avg, Q
from django.db.transaction import atomic

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.pagination import PagePagination
from core.permissions.is_admin_or_write_only import IsAdminOrWriteOnly
from core.permissions.is_own_car_permission import IsOwnCar
from core.permissions.is_premium_permisssion import IsPremium
from core.services.email_service import EmailService
from core.services.word_validation_service import validate_inappropriate_language

from apps.cars.filter import CarFilter
from apps.cars.models import CarBrandModel, CarModel, CarProfileModel
from apps.cars.serializers import CarBrandSerializer, CarSerializer


# --------------------------------------- Cars views start --------------------------------------------
class CarCreateView(CreateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsAuthenticated,)

    # @atomic
    # def post(self, request, *args, **kwargs):
    #     serializer = CarSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = request.user
    #
    #
    #     # Create car with is_active=False if inappropriate language is detected
    #     inappropriate_fields = validate_inappropriate_language(profile_data)
    #     is_active = True
    #     if inappropriate_fields:
    #         is_active = False
    #
    #     car = CarModel.objects.create_car(
    #         **serializer.validated_data,
    #         is_active=is_active,
    #         user=user
    #     )
    #     car.save()
    #
    #     if not is_active:
    #         raise ValidationError(
    #             f"Foul language in the margins: {', '.join(inappropriate_fields)}. Fix it and try again.")
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


    # @atomic
    # def post(self, request, *args, **kwargs):
    #     serializer = CarSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     profile_data = serializer.validated_data.pop('profile', {})
    #     user = request.user
    #
    #     # Створення автомобіля
    #     car = CarModel.objects.create_car(user=user, **serializer.validated_data)
    #
    #     # Створення профілю автомобіля
    #     if profile_data:
    #         CarProfileModel.objects.create(car=car, **profile_data)
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class CarListView(ListAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)


class CarRetrieveView(RetrieveAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)


class CarUpdateView(UpdateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwnCar,)

    # def patch(self, request, *args, **kwargs):
    # @atomic
    # def patch(self, request, *args, **kwargs):
    #     car = self.get_object()
    #     serializer = self.get_serializer(car, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #
    #     profile_data = serializer.validated_data.pop('profile', None)
    #     inappropriate_fields = validate_inappropriate_language(profile_data) if profile_data else []
    #
    #     if inappropriate_fields:
    #         car.edit_attempts += 1
    #         if car.edit_attempts >= 3:
    #             # Send email to manager
    #             EmailService.check_bad_words_email(user_id=str(car.user.id), car_id=str(car.id))
    #             raise ValidationError(f"Foul language detected. You have exceeded the maximum number of attempts.")
    #         car.save()
    #         raise ValidationError(
    #             f"Foul language in the margins: {', '.join(inappropriate_fields)}. Fix it and try again.")
    #
    #     # If no inappropriate language, reset edit_attempts and set is_active to True
    #     car.is_active = True
    #     car.edit_attempts = 0
    #     car.save()
    #
    #     return super().patch(request, *args, **kwargs)


class CarDeleteView(DestroyAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwnCar,)


class TestEmailView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        EmailService.send_test()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AveragePriceStatistics(RetrieveAPIView):
    permission_classes = (IsPremium,)
    queryset = CarModel.objects.all()

    def get(self, *args, **kwargs):
        car = self.get_object()
        car_is_used = car.is_used
        car_model = car.car_model_id
        cars = CarModel.objects.filter(Q(car_model_id=car_model) & Q(is_used=car_is_used)).exclude(pk=car.id)
        average_price = cars.aggregate(Avg('price'))['price__avg']
        return Response({'average_price': average_price}, status=status.HTTP_200_OK)

# --------------------------------------- Cars views end --------------------------------------------
# --------------------------------------- Brands views start --------------------------------------------


class BrandsCreateAPIView(CreateAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarBrandModel.objects.all()


class BrandsListAPIView(ListAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = (AllowAny,)
    queryset = CarBrandModel.objects.all()

class BrandRetrieveAPIView(RetrieveAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarBrandModel.objects.all()


class BrandUpdateAPIView(UpdateAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarBrandModel.objects.all()


class BrandDestroyAPIView(DestroyAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarBrandModel.objects.all()

# --------------------------------------- Brands views end --------------------------------------------