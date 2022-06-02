from datetime import datetime

from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import City, Shop, Street
from .serializers import CitySerializer, ShopSerializer


class CityViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(
        methods=['GET'],
        detail=True,
        url_path='street',
        url_name='get_streets',
        queryset=Shop.objects.select_related("city", "street").all(),
    )
    def get_streets(self, request, pk=None):
        streets = self.get_queryset().filter(city=pk).all()
        street_names = [item.street.name for item in streets]
        return Response(street_names, status=status.HTTP_200_OK)


class ShopViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Shop.objects.select_related("city", "street").all()
    serializer_class = ShopSerializer
    open_choices = ("0", "1")

    def create(self, request, *args, **kwargs):
        request_data = request.data
        city, street = request_data.get("city"), request_data.get("street")
        city_obj, _ = City.objects.get_or_create(name=city)
        street_obj, _ = Street.objects.get_or_create(name=street)
        serializer_context = {
            "city": city_obj,
            "street": street_obj,
        }
        serializer = self.get_serializer(data=request_data, context=serializer_context)
        if serializer.is_valid():
            self.perform_create(serializer)
            shop_id = serializer.data.get("id")
            return Response(shop_id, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        street = query_params.get("street")
        city = query_params.get("city")
        open_ = query_params.get("open")

        queryset = self.get_queryset()
        if street:
            queryset = queryset.filter(street__name=street)
        if city:
            queryset = queryset.filter(city__name=city)
        if open_:
            curr_time = datetime.time(timezone.now())
            if open_ == "0":
                queryset = queryset.filter(Q(close_time__gte=curr_time) | Q(open_time__lt=curr_time))
            elif open_ == "1":
                queryset = queryset.filter(Q(open_time__gte=curr_time) & Q(close_time__lt=curr_time))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
