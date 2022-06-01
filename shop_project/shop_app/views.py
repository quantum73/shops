from datetime import datetime

from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import City, Shop, Street
from .serializers import CitySerializer, ShopSerializer, StreetSerializer


class CityViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(methods=['GET'], detail=True, url_path='street', url_name='get_streets')
    def get_streets(self, request, pk=None):
        city_queryset = self.queryset.filter(id=pk)
        if not city_queryset.exists():
            return Response(
                dict(results=[f"City with ID number #{pk} does not exist"]),
                status=status.HTTP_400_BAD_REQUEST
            )

        streets = city_queryset.first().streets.all()
        street_page = self.paginate_queryset(streets)
        if street_page is not None:
            serializer = StreetSerializer(street_page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StreetSerializer(streets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    open_choices = ("0", "1")

    def create(self, request, *args, **kwargs):
        data = request.data
        city = data.get("city")
        street = data.get("street")
        city_obj = City.objects.filter(name=city)
        street_obj = Street.objects.filter(name=street)
        if not city_obj.exists():
            city_obj = City(name=city)
            city_obj.save()
        else:
            city_obj = city_obj.first()
        if not street_obj.exists():
            street_obj = Street(name=street)
            street_obj.save()
        else:
            street_obj = street_obj.first()

        city_and_street_relate = city_obj.streets.filter(name=street)
        if not city_and_street_relate.exists():
            city_obj.streets.add(street_obj)

        data["city"] = city_obj
        data["street"] = street_obj

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        query_params = request.query_params
        street = query_params.get("street")
        city = query_params.get("city")
        open_ = query_params.get("open")

        if street:
            queryset = queryset.filter(street__name=street)
        if city:
            queryset = queryset.filter(city__name=city)
        if open_:
            if open_ not in self.open_choices:
                return Response(
                    dict(results=["Parameter \"open\" must be 0 or 1"]),
                    status=status.HTTP_400_BAD_REQUEST
                )

            curr_time = datetime.time(datetime.utcnow())
            if open_ == "0":
                queryset = queryset.filter(Q(close_time__gte=curr_time) | Q(open_time__lt=curr_time))
            else:
                queryset = queryset.filter(Q(open_time__gte=curr_time) & Q(close_time__lt=curr_time))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
