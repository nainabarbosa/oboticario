from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Revendedor, Compras


class RevendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class ComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")