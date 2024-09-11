from datetime import timedelta

from django.db.models import Avg, Q
from django.db.transaction import atomic
from django.utils.decorators import method_decorator
from django.utils.timezone import now

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
    get_object_or_404,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from core.pagination import PagePagination
from core.permissions.is_admin_or_write_only import IsAdminOrWriteOnly
from core.permissions.is_car_owner_and_premium import IsCarOwnerAndPremium
from core.permissions.is_own_car_permission import IsOwnCar
from core.permissions.is_premium_permisssion import IsPremium
from core.services.email_service import EmailService
from core.services.word_validation_service import validate_inappropriate_language

from apps.cars.filters import CarFilter
from apps.cars.models import CarBrandModel, CarModel, CarModelModel, CarProfileModel, ViewStatisticsModel
from apps.cars.serializers import CarBrandSerializer, CarModelSerializer, CarSerializer


# --------------------------------------- Cars views start --------------------------------------------
class CarCreateView(CreateAPIView):
    """Create a new car"""
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsAuthenticated,)

@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_summary='Get all cars'))
class CarListView(ListAPIView):
    """List all cars"""
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)
    filterset_class = CarFilter




@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_summary='Get a specific car'))
class CarRetrieveView(RetrieveAPIView):
    """Get a specific car"""
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        car = self.get_object()
        ViewStatisticsModel.objects.create(car=car)
        return response


class CarUpdateView(UpdateAPIView):
    """Update a car"""
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwnCar,)


class CarDestroyView(DestroyAPIView):
    """Delete car"""
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwnCar,)


class ViewCountView(APIView):
    permission_classes = (IsCarOwnerAndPremium,)

    def get(self, request, car_id, period):
        car = get_object_or_404(CarModel, id=car_id)

        self.check_object_permissions(request, car)

        if period == 'day':
            start_date = now() - timedelta(days=1)
        elif period == 'week':
            start_date = now() - timedelta(weeks=1)
        elif period == 'month':
            start_date = now() - timedelta(days=30)
        elif period == 'all_time':
            start_date = None
        else:
            return Response({'error': 'Invalid period'}, status=400)

        if start_date:
            view_count = ViewStatisticsModel.objects.filter(car=car, viewed_at__gte=start_date).count()
        else:
            view_count = ViewStatisticsModel.objects.filter(car=car).count()

        return Response({
            'car_id': car_id, 'period': period, 'view_count': view_count
        })

# --------------------------------------- Cars views end --------------------------------------------
# --------------------------------------- Brands views start --------------------------------------------

class BrandCreateView(CreateAPIView):
    """Create a new car brand"""
    serializer_class = CarBrandSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarBrandModel.objects.all()


@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_summary='Get all brands'))
class BrandListView(ListAPIView):
    """List all car brands"""
    serializer_class = CarBrandSerializer
    permission_classes = (AllowAny,)
    queryset = CarBrandModel.objects.all()
    pagination_class = None

@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_summary='Get a specific brand'))
class BrandRetrieveView(RetrieveAPIView):
    """Get a specific car brand"""
    serializer_class = CarBrandSerializer
    permission_classes = (AllowAny,)
    queryset = CarBrandModel.objects.all()


class BrandUpdateView(UpdateAPIView):
    """Update a car brand"""
    serializer_class = CarBrandSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarBrandModel.objects.all()


class BrandDestroyView(DestroyAPIView):
    """Delete car brand"""
    serializer_class = CarBrandSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarBrandModel.objects.all()

# --------------------------------------- Brands views end --------------------------------------------
# --------------------------------------- Car models views start --------------------------------------------


class ModelCreateView(CreateAPIView):
    """Create a new car model"""
    serializer_class = CarModelSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarModelModel.objects.all()

@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_summary='Get all car models'))
class ModelListView(ListAPIView):
    """List all car models"""
    serializer_class = CarModelSerializer
    permission_classes = (AllowAny,)
    queryset = CarModelModel.objects.all()
    pagination_class = None


@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_summary='Get a specific car model'))
class ModelRetrieveView(RetrieveAPIView):
    """Get a specific car model"""
    serializer_class = CarModelSerializer
    permission_classes = (AllowAny,)
    queryset = CarModelModel.objects.all()


class ModelUpdateView(UpdateAPIView):
    """Update a car model"""
    serializer_class = CarModelSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarModelModel.objects.all()


class ModelDestroyView(DestroyAPIView):
    """Delete car model"""
    serializer_class = CarModelSerializer
    permission_classes = (IsAdminUser,)
    queryset = CarModelModel.objects.all()

# --------------------------------------- Car models views end --------------------------------------------


class AveragePriceStatistics(RetrieveAPIView):
    """Get average car price in Ukraine"""
    permission_classes = (IsPremium,)
    queryset = CarModel.objects.all()

    def get(self, *args, **kwargs):
        average = CarModel.objects.average_price_statistics(car=self.get_object())
        return Response({'average_price in UAH': average}, status=status.HTTP_200_OK)


class AverageRegionPriceStatistics(RetrieveAPIView):
    """Get average car price in the region"""
    permission_classes = (IsPremium,)
    queryset = CarModel.objects.all()

    def get(self, *args, **kwargs):
        average = CarModel.objects.average_region_price_statistics(car=self.get_object())
        return Response({'average_price in UAH': average}, status=status.HTTP_200_OK)


class AverageCityPriceStatistics(RetrieveAPIView):
    """Get average car price in the city"""
    permission_classes = (IsPremium,)
    queryset = CarModel.objects.all()

    def get(self, *args, **kwargs):
        average = CarModel.objects.average_city_price_statistics(car=self.get_object())
        return Response({'average_price in UAH': average}, status=status.HTTP_200_OK)

