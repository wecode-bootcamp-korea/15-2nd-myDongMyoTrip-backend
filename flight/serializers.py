from rest_framework           import serializers
from rest_framework.exceptions import ValidationError

from flight.models                  import Region, Airport, Flight

class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Airport
        exclude = ['region']

class RegionSerializer(serializers.ModelSerializer):
    airport_set = AirportSerializer(many=True, read_only=True)

    class Meta:
        model  = Region
        fields = ['name', 'airport_set']

class FlightSerializer(serializers.ModelSerializer):
    airline           = serializers.CharField(source='airline.name')
    seat_class        = serializers.CharField(source='seat_class.name')
    detailed_price    = serializers.CharField(source='detailed_price.tax_and_utility_charge')
    departure_airport = serializers.CharField(source='departure_airport.code') 
    arrival_airport   = serializers.CharField(source='arrival_airport.code') 
    
    class Meta:
        model  = Flight
        fields = '__all__'
