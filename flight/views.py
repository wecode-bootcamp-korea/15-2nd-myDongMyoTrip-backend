from rest_framework import generics, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from flight.models      import Region, Flight
from flight.serializers import RegionSerializer, FlightSerializer

class RegionAirportList(generics.ListAPIView):
    queryset         = Region.objects.all()
    serializer_class = RegionSerializer
 
class FlightViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset         = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends  = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields  = ['total_price', 'departure_time']
    search_fields    = ['airline__name', 'departure_airport__name']
    filterset_fields = ['airline__id', 'seat_class__id', 'departure_time_range__name']

    def get_queryset(self):
        airline              = self.request.query_params.get('airline')
        seat_class           = self.request.query_params.get('seat_class')
        departure_time_range = self.request.query_params.get('departure_time_range')
        if airline:
            ids = [int(x) for x in airline.split(',')] 
            queryset = Flight.objects.filter(airline__in=ids)
        if seat_class:
            ids = [int(x) for x in seat_class.split(',')]
            queryset = Flight.objects.filter(seat_class__in=ids)
        if departure_time_range:
            ids  = [int(x) for x in departure_time_range.split(',')]
            queryset = Flight.objects.filter(departure_time_range__in=ids)
        else:
            queryset = Flight.objects.all()
        return queryset
