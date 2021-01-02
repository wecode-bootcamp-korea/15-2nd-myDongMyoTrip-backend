import json

from django.db.models import Q
from django.db        import transaction
from django.views     import View
from django.http      import JsonResponse

from user.utils       import authorize_user
from .models          import (
    Region,
    Airport,
    Airline,
    Flight,
    SeatClass,
    FlightPassenger,
    FlightBookingInformation,
    DetailedPrice,
    PassengerType,
    PassengerInformation,
    Payment
)

class RegionAirportView(View):
    def get(self, request):
        regions = Region.objects.prefetch_related('airport_set')

        regions = [{
            'id'        : region.id,
            'name'      : region.name,
            'airports'  : [{
                'id'    : airport.id,
                'name'  : airport.name,
                'code'  : airport.code
                } for airport in region.airport_set.all()]
            } for region in regions]

        return JsonResponse({'message': 'SUCCESS', 'regions': regions}, status=200)

class FlightListView(View):
    def get(self, request):
        try:
            departure_airport       = request.GET.get('departure_airport', None)
            arrival_airport         = request.GET.get('arrival_airport', None)
            departure_date          = request.GET.get('departure_date', None)
            arrival_date            = request.GET.get('arrival_date', None)
            airline_id              = request.GET.getlist('airline', None)
            seat_class_id           = request.GET.getlist('seat_class', None)
            order                   = request.GET.get('order', None)

            q = Q()
            if departure_airport:
                q &= Q(departure_airport=departure_airport)
            if arrival_airport:
                q &= Q(arrival_airport=arrival_airport)
            if departure_date:
                q &= Q(departure_date=departure_date)
            if arrival_date:
                q &= Q(arrival_date=arrival_date)
            if airline_id:
                q &= Q(airline__in=airline_id)
            if seat_class_id:
                q &= Q(seat_class__in=seat_class_id)

            sorting_type_set = {
                '0' : 'total_price',
                '1' : 'departure_time',
                '2' : '-departure_time'
            }

            flights = Flight.objects.select_related(
                'airline',
                'departure_airport',
                'arrival_airport',
                'detailed_price',
                'seat_class',
                ).filter(q).order_by(sorting_type_set[order])

            flight_list = [{
                'id'                     : flight.id,
                'number'                 : flight.number,
                'departure_time'         : flight.departure_time,
                'arrival_time'           : flight.arrival_time,
                'departure_date'         : flight.departure_date,
                'arrival_date'           : flight.arrival_date,
                'remain_seat'            : flight.remain_seat,
                'total_price'            : float(flight.total_price),
                'airline_name'           : flight.airline.name,
                'airline_logo_url'       : flight.airline.logo_url,
                'departure_airport_name' : flight.departure_airport.name,
                'departure_airport_code' : flight.departure_airport.code,
                'arrival_airport_name'   : flight.arrival_airport.name,
                'arrival_airport_code'   : flight.arrival_airport.code,
                'base_fare'              : float(flight.total_price) - float(flight.detailed_price.tax_and_utility_charge),
                'fuel_surcharge'         : float(flight.detailed_price.fuel_surcharge),
                'tax_and_utility_charge' : float(flight.detailed_price.tax_and_utility_charge),
                'service_fee'            : float(flight.detailed_price.service_fee),
                'seat_class'             : flight.seat_class.name,
                } for flight in flights]

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status = 400)

        return JsonResponse({'message': 'SUCCESS', 'flight_list': flight_list}, status = 200)
