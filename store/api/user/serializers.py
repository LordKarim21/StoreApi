from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model.
    """

    class Meta:
        model = models.User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model.
    """
    profile = UserSerializer(read_only=True)

    class Meta:
        model = models.Payment
        fields = '__all__'
