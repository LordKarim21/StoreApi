from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model, providing order details.
    """
    class Meta:
        model = Order
        fields = '__all__'
