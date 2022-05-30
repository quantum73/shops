from rest_framework import routers

from .views import CityViewSet, ShopViewSet

router = routers.DefaultRouter()
router.register('city', CityViewSet)
router.register('shop', ShopViewSet)
shop_router = router.urls
