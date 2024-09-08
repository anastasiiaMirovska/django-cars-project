from django.db.models import Avg, Q

from rest_framework import status
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

from apps.cars.filter import CarFilter
from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializer


class CarCreateView(CreateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsAuthenticated,)


class CarListView(ListAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)


# class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     serializer_class = CarSerializer
#     queryset = CarModel.objects.all()

    # def get(self, request, *args, **kwargs):
    #     permission_classes = (AllowAny,)
    # def put(self, request, *args, **kwargs):
    #     permission_classes = (IsOwnCar,)
    # def patch(self, request, *args, **kwargs):
    #     permission_classes = (IsOwnCar,)
    # def delete(self, request, *args, **kwargs):
    #     permission_classes = (IsOwnCar,)


class CarRetrieveView(RetrieveAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)


class CarUpdateView(UpdateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwnCar,)

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

