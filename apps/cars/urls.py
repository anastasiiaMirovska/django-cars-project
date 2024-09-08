from django.urls import path

from apps.cars.views import (
    AveragePriceStatistics,
    CarCreateView,
    CarDeleteView,
    CarListView,
    CarRetrieveView,
    CarUpdateView,
    TestEmailView,
)

urlpatterns = [
    path('', CarListView.as_view(), name='car_list_create'),
    path('/create', CarCreateView.as_view(), name='car_create'),
    path('/<int:pk>/retrieve', CarRetrieveView.as_view(), name='car_retrieve_update_delete'),
    path('/<int:pk>/update', CarUpdateView.as_view(), name='car_retrieve_update_delete'),
    path('/<int:pk>/delete', CarDeleteView.as_view(), name='car_retrieve_update_delete'),
    path('/test', TestEmailView.as_view()),
    path('/<int:pk>/avg_price', AveragePriceStatistics.as_view(), name='average_price_statistics'),
]