from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.permissions.is_owner_or_admin import IsOwnerOrAdmin

from apps.auto_parks.models import AutoParkModel
from apps.auto_parks.serializers import AutoParkSerializer


class AutoParkListView(ListAPIView):
    """List all auto parks"""
    serializer_class = AutoParkSerializer
    queryset = AutoParkModel.objects.all()
    permission_classes = (AllowAny,)


class AutoParkCreateView(CreateAPIView):
    """Create own auto park"""
    serializer_class = AutoParkSerializer
    queryset = AutoParkModel.objects.all()
    permission_classes = (IsAuthenticated,)


class AutoParkRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
        get:
            get auto park details
        put:
            update auto park details
        patch:
            update auto park details partially
        delete:
            delete auto park
    """
    serializer_class = AutoParkSerializer
    queryset = AutoParkModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)
        return (IsOwnerOrAdmin(),)

