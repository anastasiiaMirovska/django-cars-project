from django.urls import path

from apps.cars.views import CarCreateView, CarListView, CarRetrieveUpdateDestroyView, TestEmailView

urlpatterns = [
    path('', CarListView.as_view(), name='car_list_create'),
    path('/create', CarCreateView.as_view(), name='car_create'),
    path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view(), name='car_retrieve_update_delete'),
    path('/test', TestEmailView.as_view())
]