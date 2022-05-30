from datetime import datetime

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import City, Shop, Street
from .serializers import CitySerializer, ShopSerializer
from .utils import str_time_to_object_time, time_is_valid


class CityViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(methods=['GET'], detail=True, url_path='street', url_name='get_streets')
    def get_streets(self, request, pk=None):
        street_queryset = Street.objects.filter(city=pk).all()
        return Response(
            dict(streets=[i.name for i in street_queryset]),
            status=status.HTTP_200_OK
        )


class ShopViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    open_choices = ("0", "1")

    def create(self, request, *args, **kwargs):
        data = request.data
        open_time = data.get("open_time")
        close_time = data.get("close_time")
        if not time_is_valid(open_time):
            return Response("Incorrect open_time format", status=status.HTTP_400_BAD_REQUEST)
        if not time_is_valid(close_time):
            return Response("Incorrect close_time format", status=status.HTTP_400_BAD_REQUEST)

        data["open_time"] = str_time_to_object_time(open_time)
        data["close_time"] = str_time_to_object_time(close_time)

        city = data.get("city")
        street = data.get("street")
        city_obj = City.objects.filter(name=city)
        street_obj = Street.objects.filter(name=street)

        # city = data.get("city")
        # city_obj = City.objects.filter(name=city)
        # if not city_obj.exists():
        #     city_obj = City(name=city)
        #     city_obj.save()
        # else:
        #     city_obj = city_obj.first()
        #
        # street = data.get("street")
        # street_obj = Street.objects.filter(name=street, city=city_obj)
        # if not street_obj.exists():
        #     street_obj = Street(name=street, city=city_obj)
        #     street_obj.save()
        # else:
        #     street_obj = street_obj.first()

        data["city"] = city_obj.pk
        data["street"] = street_obj.pk

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        query_params = request.query_params
        street = query_params.get("street")
        city = query_params.get("city")
        open_ = query_params.get("open")
        if open_ not in self.open_choices:
            return Response("Parameter \"open\" must be 0 or 1", status=status.HTTP_400_BAD_REQUEST)

        # if street:
        #     queryset = queryset.filter(street=street)
        # if city:
        #     queryset = queryset.filter(city=city)
        if open_:
            curr_time = datetime.time(datetime.now())
            if open_ == "0":
                queryset = queryset.filter(close_time__gte=curr_time, open_time__lt=curr_time)
            else:
                queryset = queryset.filter(open_time__gte=curr_time, close_time__lt=curr_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
