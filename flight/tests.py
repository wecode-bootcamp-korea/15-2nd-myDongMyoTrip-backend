import datetime

from django.test import TestCase, Client
from .models     import (Region,
    Airport,
    Airline,
    Flight,
    DetailedPrice,
    SeatClass,
)

class RegionAirportTest(TestCase):
    def setUp(self):
        client   = Client()
        Region.objects.create(
            id   = 1,
            name = 'Asia'
        )

        Airport.objects.create(
            id = 1,
            name      = 'Singapore',
            code      = 'SIN',
            region_id = 1
        )

        Airport.objects.create(
            id = 2,
            name = 'Bangkok',
            code = 'BKK',
            region_id = 1
        )

    def tearDown(self):
        Region.objects.all().delete()
        Airport.objects.all().delete()

    def test_regionairportview_get_success(self):
        response = self.client.get('/flight/region-airport')

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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'regions': regions})

class FlightListTest(TestCase):
    maxDiff = None
    def setUp(self):
        client = Client()
        Airline.objects.create(
            id       = 1,
            name     = 'wecode_air',
            logo_url = 'https://wecode.co.kr'
        )

        Region.objects.create(
            id   = 1,
            name = 'Asia'
        )

        Airport.objects.bulk_create([
            Airport(
                id = 1,
                name      = 'Singapore',
                code      = 'SIN',
                region_id = 1
            ),
            Airport(
                id = 2,
                name = 'Bangkok',
                code = 'BKK',
                region_id = 1
            )
        ])

        DetailedPrice.objects.create(
            id                     = 1,
            base_fare              = 42000.00,
            fuel_surcharge         = 0.00,
            tax_and_utility_charge = 8000.00,
            service_fee            = 0.00
        )

        SeatClass.objects.create(
            id   = 1,
            name = '일반석'
        )

        Flight.objects.bulk_create([
            Flight(
                id                   = 1,
                number               = 'TW731',
                departure_time       = '15:00:00',
                arrival_time         = '20:00:00',
                departure_date       = '2021-01-01',
                arrival_date         = '2021-01-01',
                remain_seat          = 9,
                total_price          = 50000.00,
                airline_id           = 1,
                departure_airport_id = 1,
                arrival_airport_id   = 2,
                detailed_price_id    = 1,
                seat_class_id        = 1
            ),
            Flight(
                id                   = 2,
                number               = 'TW731',
                departure_time       = '20:00:00',
                arrival_time         = '23:00:00',
                departure_date       = '2021-01-01',
                arrival_date         = '2021-01-01',
                remain_seat          = 9,
                total_price          = 50000.00,
                airline_id           = 1,
                departure_airport_id = 2,
                arrival_airport_id   = 1,
                detailed_price_id    = 1,
                seat_class_id        = 1
            )
        ])

    def tearDown(self):
        Flight.objects.all().delete()
        Airline.objects.all().delete()
        Airport.objects.all().delete()
        DetailedPrice.objects.all().delete()
        SeatClass.objects.all().delete()

    def test_flightlistview_get_success(self):
        response = self.client.get('/flight?order=0')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS',
            'flight_list': [
                {
                    'id'                     : 1,
                    'number'                 : 'TW731',
                    'departure_time'         : '15:00:00',
                    'arrival_time'           : '20:00:00',
                    'departure_date'         : '2021-01-01',
                    'arrival_date'           : '2021-01-01',
                    'remain_seat'            : 9,
                    'total_price'            : 50000.0,
                    'airline_name'           : 'wecode_air',
                    'airline_logo_url'       : 'https://wecode.co.kr',
                    'departure_airport_name' : 'Singapore',
                    'departure_airport_code' : 'SIN',
                    'arrival_airport_name'   : 'Bangkok',
                    'arrival_airport_code'   : 'BKK',
                    'base_fare'              : 42000.00,
                    'fuel_surcharge'         : 0.00,
                    'tax_and_utility_charge' : 8000.00,
                    'service_fee'            : 0.00,
                    'seat_class'             : '일반석'
                },
                {
                    'id'                     : 2,
                    'number'                 : 'TW731',
                    'departure_time'         : '20:00:00',
                    'arrival_time'           : '23:00:00',
                    'departure_date'         : '2021-01-01',
                    'arrival_date'           : '2021-01-01',
                    'remain_seat'            : 9,
                    'total_price'            : 50000.0,
                    'airline_name'           : 'wecode_air',
                    'airline_logo_url'       : 'https://wecode.co.kr',
                    'departure_airport_name' : 'Bangkok',
                    'departure_airport_code' : 'BKK',
                    'arrival_airport_name'   : 'Singapore',
                    'arrival_airport_code'   : 'SIN',
                    'base_fare'              : 42000.00,
                    'fuel_surcharge'         : 0.00,
                    'tax_and_utility_charge' : 8000.00,
                    'service_fee'            : 0.00,
                   'seat_class'              : '일반석'
                }
            ]
        }
                )

    def test_flightlistview_get_filtering_success(self):
        response = self.client.get('/flight?order=0&seat_class_id=1&departure_airport_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS',
            'flight_list': [
                {
                    'id'                     : 1,
                    'number'                 : 'TW731',
                    'departure_time'         : '15:00:00',
                    'arrival_time'           : '20:00:00',
                    'departure_date'         : '2021-01-01',
                    'arrival_date'           : '2021-01-01',
                    'remain_seat'            : 9,
                    'total_price'            : 50000.0,
                    'airline_name'           : 'wecode_air',
                    'airline_logo_url'       : 'https://wecode.co.kr',
                    'departure_airport_name' : 'Singapore',
                    'departure_airport_code' : 'SIN',
                    'arrival_airport_name'   : 'Bangkok',
                    'arrival_airport_code'   : 'BKK',
                    'base_fare'              : 42000.00,
                    'fuel_surcharge'         : 0.00,
                    'tax_and_utility_charge' : 8000.00,
                    'service_fee'            : 0.00,
                    'seat_class'             : '일반석'
                },
                {
                    'id'                     : 2,
                    'number'                 : 'TW731',
                    'departure_time'         : '20:00:00',
                    'arrival_time'           : '23:00:00',
                    'departure_date'         : '2021-01-01',
                    'arrival_date'           : '2021-01-01',
                    'remain_seat'            : 9,
                    'total_price'            : 50000.0,
                    'airline_name'           : 'wecode_air',
                    'airline_logo_url'       : 'https://wecode.co.kr',
                    'departure_airport_name' : 'Bangkok',
                    'departure_airport_code' : 'BKK',
                    'arrival_airport_name'   : 'Singapore',
                    'arrival_airport_code'   : 'SIN',
                    'base_fare'              : 42000.00,
                    'fuel_surcharge'         : 0.00,
                    'tax_and_utility_charge' : 8000.00,
                    'service_fee'            : 0.00,
                   'seat_class'              : '일반석'
                }
            ]
        }
                )
