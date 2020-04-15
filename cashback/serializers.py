from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Revendedor, Compras


class RevendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revendedor
        fields = '__all__'


class ComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compras
        fields = '__all__'


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")