from rest_framework import serializers

from .models import Tariff


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = [
            'id',
            'name', 
            'duration_days', 
            'price',  
            'order',
            'is_bestseller',
            'original_price',
        ]