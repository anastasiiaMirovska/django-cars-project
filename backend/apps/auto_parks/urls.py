from django.urls import path

from .views import AutoParkCreateView, AutoParkListView, AutoParkRetrieveUpdateDestroyView

urlpatterns = [
    path('', AutoParkListView.as_view(), name='dealership-list'),
    path('/create', AutoParkCreateView.as_view(), name='dealership-create'),
    path('/<int:pk>', AutoParkRetrieveUpdateDestroyView.as_view(), name='dealership-retrieve-update-destroy'),
]

