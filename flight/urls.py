from django.urls  import path
from flight.views   import RegionAirportView, FlightListView

urlpatterns = [
    path('/region-airport', RegionAirportView.as_view()),
    path('', FlightListView.as_view()),
]
