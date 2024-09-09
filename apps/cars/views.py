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

from apps.cars.filters import CarFilter
from apps.cars.models import CarBrandModel, CarModel, CarModelModel, CarProfileModel
from apps.cars.serializers import CarBrandSerializer, CarModelSerializer, CarSerializer


# --------------------------------------- Cars views start --------------------------------------------
class CarCreateView(CreateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsAuthenticated,)


class CarListView(ListAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)
    filterset_class = CarFilter


class CarRetrieveView(RetrieveAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)


class CarUpdateView(UpdateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwnCar,)


class CarDestroyView(DestroyAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwnCar,)

# --------------------------------------- Cars views end --------------------------------------------
# --------------------------------------- Brands views start --------------------------------------------

class BrandCreateView(CreateAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarBrandModel.objects.all()


class BrandListView(ListAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = (AllowAny,)
    queryset = CarBrandModel.objects.all()
    pagination_class = None

class BrandRetrieveView(RetrieveAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = (AllowAny,)
    queryset = CarBrandModel.objects.all()


class BrandUpdateView(UpdateAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarBrandModel.objects.all()


class BrandDestroyView(DestroyAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarBrandModel.objects.all()

# --------------------------------------- Brands views end --------------------------------------------
# --------------------------------------- Car models views start --------------------------------------------


class ModelCreateView(CreateAPIView):
    serializer_class = CarModelSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarModelModel.objects.all()


class ModelListView(ListAPIView):
    serializer_class = CarModelSerializer
    permission_classes = (AllowAny,)
    queryset = CarModelModel.objects.all()
    pagination_class = None


class ModelRetrieveView(RetrieveAPIView):
    serializer_class = CarModelSerializer
    permission_classes = (AllowAny,)
    queryset = CarModelModel.objects.all()


class ModelUpdateView(UpdateAPIView):
    serializer_class = CarModelSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarModelModel.objects.all()


class ModelDestroyView(DestroyAPIView):
    serializer_class = CarModelSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarModelModel.objects.all()

# --------------------------------------- Car models views end --------------------------------------------

# class TestEmailView(GenericAPIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, *args, **kwargs):
#         EmailService.send_test()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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

