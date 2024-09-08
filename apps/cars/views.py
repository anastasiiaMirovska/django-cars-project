from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.pagination import PagePagination
from core.permissions.is_admin_or_write_only import IsAdminOrWriteOnly
from core.services.email_service import EmailService

from apps.cars.filter import CarFilter
from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializer


class CarListCreateView(ListCreateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsAdminOrWriteOnly,)
    # filterset_class = CarFilter


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()

    def get_permissions(self):
        car = self.get_object()
        user = self.request.user
        if car.user == user.id:
            permissions = (AllowAny(),)
        return (IsAdminUser(),)


class TestEmailView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        EmailService.send_test()
        return Response(status=status.HTTP_204_NO_CONTENT)