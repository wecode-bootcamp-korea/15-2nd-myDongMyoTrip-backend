from django.urls            import path, include
from rest_framework.routers import DefaultRouter

from flight.views import RegionAirportList, FlightViewSet #FlightList

flight_list = FlightViewSet.as_view({'get': 'list'})
flight_detail = FlightViewSet.as_view({'get': 'retrieve'})

router = DefaultRouter(trailing_slash=False)
router.register(r'flight', FlightViewSet)


urlpatterns = [
    path('region-airport', RegionAirportList.as_view()),
    path('', include(router.urls))
]
