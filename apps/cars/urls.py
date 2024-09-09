from django.urls import path

from apps.cars.views import (  # TestEmailView,
    AveragePriceStatistics,
    BrandCreateView,
    BrandDestroyView,
    BrandListView,
    BrandRetrieveView,
    BrandUpdateView,
    CarCreateView,
    CarDestroyView,
    CarListView,
    CarRetrieveView,
    CarUpdateView,
    ModelCreateView,
    ModelDestroyView,
    ModelListView,
    ModelRetrieveView,
    ModelUpdateView,
)


class BrandDeleteView:
    pass


urlpatterns = [
    path('', CarListView.as_view(), name='car_list_create'),
    path('/create', CarCreateView.as_view(), name='car_create'),
    path('/<int:pk>/retrieve', CarRetrieveView.as_view(), name='car_retrieve_update_delete'),
    path('/<int:pk>/update', CarUpdateView.as_view(), name='car_retrieve_update_delete'),
    path('/<int:pk>/delete', CarDestroyView.as_view(), name='car_retrieve_update_delete'),

    path('/brands', BrandListView.as_view(), name='car_brand_list_create'),
    path('/brands/create', BrandCreateView.as_view(), name='car_brand_create'),
    path('/brands/<int:pk>/retrieve', BrandRetrieveView.as_view(), name='ca_brand_retrieve_update_delete'),
    path('/brands/<int:pk>/update', BrandUpdateView.as_view(), name='car_brand_retrieve_update_delete'),
    path('/brands/<int:pk>/delete', BrandDestroyView.as_view(), name='car_brand_retrieve_update_delete'),

    path('/models', ModelListView.as_view(), name='car_model_list_create'),
    path('/models/create', ModelCreateView.as_view(), name='car_model_create'),
    path('/models/<int:pk>/retrieve', ModelRetrieveView.as_view(), name='car_model_retrieve_update_delete'),
    path('/models/<int:pk>/update', ModelUpdateView.as_view(), name='car_model_retrieve_update_delete'),
    path('/models/<int:pk>/delete', ModelDestroyView.as_view(), name='car_model_retrieve_update_delete'),

    # path('/test', TestEmailView.as_view()),
    path('/<int:pk>/avg_price', AveragePriceStatistics.as_view(), name='average_price_statistics'),
]