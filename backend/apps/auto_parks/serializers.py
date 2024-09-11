from django.db.transaction import atomic

from rest_framework import serializers

from apps.auto_parks.models import AutoParkModel


class AutoParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoParkModel
        fields = (
            'id',
            'name',
            'address',
            'phone',
            'description',
            'main_user',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('main_user', 'created_at', 'updated_at')

    @atomic
    def create(self, validated_data):
        request = self.context.get('request', None)
        validated_data['main_user'] = request.user
        auto_park = AutoParkModel.objects.create(**validated_data)
        return auto_park
