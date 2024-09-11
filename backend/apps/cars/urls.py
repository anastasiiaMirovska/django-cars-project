from django.urls import path

from apps.cars.views import (  # TestEmailView,; AveragePriceStatistics,; AverageRegionPriceStatistics,
    AverageCityPriceStatistics,
    AveragePriceStatistics,
    AverageRegionPriceStatistics,
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
    ViewCountView,
)


class BrandDeleteView:
    pass


urlpatterns = [
    path('', CarListView.as_view(), name='car_list'),
    path('/create', CarCreateView.as_view(), name='car_create'),
    path('/<int:pk>/retrieve', CarRetrieveView.as_view(), name='car_retrieve'),
    path('/<int:pk>/update', CarUpdateView.as_view(), name='car_update'),
    path('/<int:pk>/destroy', CarDestroyView.as_view(), name='car_destroy'),
    path('/<int:car_id>/views/<str:period>', ViewCountView.as_view(), name='view_count'),

    path('/brands', BrandListView.as_view(), name='car_brand_list'),
    path('/brands/create', BrandCreateView.as_view(), name='car_brand_create'),
    path('/brands/<int:pk>/retrieve', BrandRetrieveView.as_view(), name='ca_brand_retrieve'),
    path('/brands/<int:pk>/update', BrandUpdateView.as_view(), name='car_brand_update'),
    path('/brands/<int:pk>/destroy', BrandDestroyView.as_view(), name='car_brand_destroy'),

    path('/models', ModelListView.as_view(), name='car_model_list'),
    path('/models/create', ModelCreateView.as_view(), name='car_model_create'),
    path('/models/<int:pk>/retrieve', ModelRetrieveView.as_view(), name='car_model_retrieve'),
    path('/models/<int:pk>/update', ModelUpdateView.as_view(), name='car_model_update'),
    path('/models/<int:pk>/destroy', ModelDestroyView.as_view(), name='car_model_destroy'),

    # path('/test', TestEmailView.as_view()),
    path('/<int:pk>/avg_price', AveragePriceStatistics.as_view(), name='average_price_statistics'),
    path('/<int:pk>/avg_region_price', AverageRegionPriceStatistics.as_view(), name='average_region_price_statistics'),
    path('/<int:pk>/avg_city_price', AverageCityPriceStatistics.as_view(), name='average_city_price_statistics'),
]
