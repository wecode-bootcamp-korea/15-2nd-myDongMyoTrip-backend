from django.test import TestCase
from django.test import Client
from django.http import JsonResponse
import json
import unittest

from user.models   import User
from accommodation.models import (
    Theme,
    AccommodationTheme, 
    Accommodation, 
    Host, 
    RoomAmenity, 
    RoomType,
    RoomTypeAmenity,
    AccommodationImage,
    FreeService,
    AccommodationService,
    SharedFacility,
    AccommodationFacility,
    Dormitory,
    AccommodationDormitory,
    GeneralRoom,
    AccommodationRoom,
    Review,
    AgeGroup,
    TravelType,
    Reservation,
    Coupon,
    UserCoupon,
)


class AccommodationDetail(TestCase):
    
    def setUp(self):
        self.client = Client()
        theme = Theme.objects.create(
            name      = '제주시',
        )
        host = Host.objects.create(
            id        = 1,
            name      = '제주시',
            image_url = 'www.wecode.co.kr'
        )
        accommodation = Accommodation.objects.create(
            id                        = 1,
            name                      = '제주시',
            price                     = 25000,
            description               = '제주시',
            number_of_guest           = 2,
            star_rating               = 4.0,
            check_in                  = "2020-05-12",
            check_out                 = "2020-06-13",
            address                   = '제주시',
            host_id                   = 1,
            is_immediate_confirmation = False,
        )

    def tearDown(self) :
        Theme.objects.all().delete()
        Accommodation.objects.all().delete()
        Host.objects.all().delete()


    def test_accommodationdetailview_get_success(self):   
        accommodation_id = 1
        response = self.client.get(f'/accommodation/{accommodation_id}')
        self.assertEqual(response.status_code, 200)

    def test_accommodationdetailview_get_fail(self):
        response = self.client.get('/accommodation/2')
        self.assertEqual(response.json(),
            {'message':'ACCOMMODATION_NOT_FOUND'}
        )
        self.assertEqual(response.status_code, 404)

    def test_accommodationdetailview_get_not_found(self):
        response = self.client.get('accommodation/2')
        self.assertEqual(response.status_code, 404)

class AccommodationDetail(TestCase):
    
    def setUp(self):
        self.client = Client()

        host = Host.objects.create(
            id        = 1,
            name      = '제주시',
            image_url = 'www.wecode.co.kr'
        )
        shared_facility = SharedFacility.objects.create(
            id = 1,
            name='에어컨',
            image_url= 'www.wecode.co.kr'
        )
        shared_facility2 = SharedFacility.objects.create(
            id = 2,
            name='세탁기',
            image_url= 'www.daum.net'
        )

        accommodation = Accommodation.objects.create(
            id                        = 1,
            name                      = '제주시',
            price                     = 25000,
            description               = '제주시',
            number_of_guest           = 2,
            star_rating               = 4.0,
            check_in                  = "2020-05-12",
            check_out                 = "2020-06-13",
            address                   = '제주시',
            host_id                   = 1,
            is_immediate_confirmation = False, 
        )
        accommodation2 = Accommodation.objects.create(
            id                        = 2,
            name                      = '서귀포시',
            price                     = 25000,
            description               = '제주시',
            number_of_guest           = 2,
            star_rating               = 4.0,
            check_in                  = "2020-05-12",
            check_out                 = "2020-06-13",
            address                   = '제주시',
            host_id                   = 1,
            is_immediate_confirmation = False, 
        )
        
        AccommodationFacility.objects.create(shared_facility=shared_facility, accommodation=accommodation)
        AccommodationFacility.objects.create(shared_facility=shared_facility2, accommodation=accommodation2)

        def tearDown(self) :
            shared_facility.objects.all().delete()
            shared_facility2.objects.all().delete()
            accommodation.objects.all().delete()
            accommodation2.objects.all().delete()  


    def test_accommodationlistview_get_success(self):
        response = self.client.get('/accommodation/list', content_type = 'application/json')
        result={
            'accommodation_list': [
                {
                'id'               : 1,
                'name'             : '제주시',
                'check-in'         : "2020-05-12",
                'check-out'        : "2020-06-13",
                'number_of_guest'  : 2,
                'description'      : '제주시',
                'star_rating'      : 4.0,
                'number_of_reviews': 2,
                'price'            : 25000,
                'image_url'        : 'www.wecode.co.kr'
                }
            ] 
        }
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_accommodationlistview_get_filtering_shared_facility(self):
        response = self.client.get('/acccommodation/list?shared_facility_id=2')
        self.assertEqual(response.json(), {
            'message': 'SUCCESS',
            'accommodation_list': [
                {
                    'id'               : 2,
                    'name'             : '제주시',
                    'check-in'         : "2020-05-12",
                    'check-out'        : "2020-06-13",
                    'number_of_guest'  : 2,
                    'description'      : '제주시',
                    'star_rating'      : 4.0,
                    'number_of_reviews': 2,
                    'price'            : 25000,
                    'image_url'        : 'www.wecode.co.kr'
                }
            ]
        }
        )

        self.assertEqual(response.status_code, 200)
