from rest_framework import serializers

from .models import User, Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    used_gb = serializers.FloatField(read_only=True)
    total_gb_limit = serializers.FloatField(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'is_active', 
            'end_date', 
            'trial_activated', 
            'used_gb', 
            'total_gb_limit',
        ]


class UserSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'first_name', 
            'date_joined',
            'subscription',  
        ]