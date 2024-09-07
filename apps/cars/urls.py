from django.urls import path

from apps.cars.views import CarListCreateView, CarRetrieveUpdateDestroyView, TestEmailView

urlpatterns = [
    path('', CarListCreateView.as_view(), name='car_list_create'),
    path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view(), name='car_retrieve_update_delete'),
    path('/test', TestEmailView.as_view())
]