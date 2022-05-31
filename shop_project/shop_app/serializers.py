from rest_framework import serializers

from .models import City, Street, Shop


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ('id', 'name')


class ShopSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(queryset=City.objects.all(), slug_field='name')
    street = serializers.SlugRelatedField(queryset=Street.objects.all(), slug_field='name')

    class Meta:
        model = Shop
        fields = ('id', 'name', 'city', 'street', 'house_num', 'open_time', 'close_time')
