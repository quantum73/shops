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
    city = CitySerializer(read_only=True)
    street = StreetSerializer(read_only=True)

    class Meta:
        model = Shop
        fields = ('id', 'name', 'city', 'street', 'house_num', 'open_time', 'close_time')
