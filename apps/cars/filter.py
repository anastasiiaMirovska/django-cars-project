from django_filters import rest_framework as filters

from apps.cars.choices.body_type_choices import BodyTypeChoices


class CarFilter(filters.FilterSet):
    year_gt = filters.NumberFilter('year', 'gt')
    body = filters.CharFilter('body_type', choices=BodyTypeChoices.choices)
    order = filters.OrderingFilter(
        fields=(
            'brand',
            'price',
            ('id', 'asd')
        )
    )