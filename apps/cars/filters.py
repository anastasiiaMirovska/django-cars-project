from django_filters import rest_framework as filters

from apps.cars.choices.body_type_choices import BodyTypeChoices
from apps.cars.choices.currency_choices import CurrencyChoices
from apps.cars.choices.engine_type_choices import EngineTypeChoices
from apps.cars.choices.transmission_type_choices import TransmissionTypeChoices


class CarFilter(filters.FilterSet):

    is_used = filters.BooleanFilter('is_used')

    # -------------------------------------Search------------------------------------
    brand = filters.CharFilter('car_model__brand__name', lookup_expr='icontains')
    car_model = filters.CharFilter('car_model__name', lookup_expr='icontains')
    city = filters.CharFilter('profile__city', lookup_expr='icontains')
    region = filters.CharFilter('profile__region')

    # -------------------------------------Filter------------------------------------

    year_gte = filters.NumberFilter('year', lookup_expr='gte')
    year_lte = filters.NumberFilter('year', lookup_expr='lte')
    price_gte = filters.NumberFilter('price', lookup_expr='gte')
    price_lte = filters.NumberFilter('price', lookup_expr='lte')
    mileage_gte = filters.NumberFilter('profile__mileage', lookup_expr='gte')
    mileage_lte = filters.NumberFilter('profile__mileage', lookup_expr='lte')
    engine_volume_gte = filters.NumberFilter('profile__engine_volume', lookup_expr='gte')
    engine_volume_lte = filters.NumberFilter('profile__engine_volume', lookup_expr='lte')

    # -------------------------------------Choices------------------------------------

    currency = filters.ChoiceFilter('currency', choices=CurrencyChoices.choices)
    body = filters.ChoiceFilter('profile__body', choices=BodyTypeChoices.choices)
    engine_type = filters.ChoiceFilter('profile__engine', choices=EngineTypeChoices.choices)
    transmission = filters.ChoiceFilter('profile__transmission', choices=TransmissionTypeChoices.choices)

    # -------------------------------------Ordering------------------------------------

    order = filters.OrderingFilter(
        fields=(
            'year',
            'price',
            ('id', 'pk')
        )
    )
