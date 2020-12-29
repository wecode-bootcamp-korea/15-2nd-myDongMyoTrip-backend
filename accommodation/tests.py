from django.test import TestCase
<<<<<<< HEAD
import json

from user.models   import User
from accommodation.models  import Accommodation
from django.test   import Client

class AccommodationDetail(TestCase):
    def setUp(self):

        Theme.objects.create(
            name      = '제주시',
            image_url = 'www.wecode.co.kr'
        )
        AccommodationTheme.objects.create(
            theme_id         = 1,
            accommodation_id = 1
        )
        Accommodation.objects.create(
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
        Host.objects.create(
            Name      = '제주시',
            image_url = 'www.wecode.co.kr'
        )
        RoomAmenity.objects.create(
            name = '화장실'
        )
        RoomType.objects.create(
            name='6인 여성방',
            price=25000,
            minimum = 1,
            maximum = 4,
            number_of_bed = 4,
            minimum_reservation = 1,
            image_url = 'www.wecode.co.kr',
            accommodation_id = 1,
        )
        RoomTypeAmenity.objects.create(
            room_type_id = 1,
            room_amenity_id = 2
        )
        AccommodationImage.objects.create(
            image_url='www.wecode.co.kr',
            accommodation_id=1
        )
        FreeService.objects.create(
            name='짐보관',
            image_url='www.wecode.co.kr'
        )
        AccommodationService.objects.create(
            free_service_id = 1,
            accommodation_id =1
        )
        SharedFacility.objects.create(
            name='수건',
            image_url='www.wecode.co.kr'
        )
        AccommodationFacility.objects.create(
            shared_facility_id=1,
            accommodation_id=1
        )
        Dormitory.objects.create(
            name = '여성전용'
        )
        AccommodationDormitory.objects.create(
            dormitory_id=1,
            accommodation_id =1
        )
        GeneralRoom.objects.create(
            name = '1인실'
        )
        AccommodationRoom.objects.create(
            general_room_id=1,
            accommodation_id=1
        )
        Review.objects.create(
            user_id = 1,
            accommodation_id = 1,
            context = 'hello',
            star_rating = 4.0,
            image_url ='www.wecode.co.kr',
        )
        AgeGroup.objects.create(
            age = '10대' 
        )
        TravelType.objects.create(
            type = '부모님과 함께여행'
        )
        Reservation.objects.create(
            accommodation_id=1,
            user_id=1,
            gender=1,
            accommodation_payment_id=1,
            age_group_id=1,
            travel_type_id=1,
            name='우혁준',
            date_of_birth="2020-05-12",
            estimate_arrival_time="15:00",
            total_price=25000,
            is_privacy_agreement=False,
        )
        Coupon.objects.create(
            code='1234567'
        )
        UserCoupon.objects.create(
            user_id=1,
            coupon_id=1,
            reservation_id = 1
        )
        AccommodationPayment.objects.create(
            payment_method_id=1,
            is_payment_status=False,
            total_price  = 250000
        )
    
    def tearDown(self) :
        Theme.objects.all().delete()
        AccommodationTheme.objects.all().delete()
        Accommodation.objects.all().delete()
        Host.objects.all().delete()
        RoomAmenity.objects.all().delete()
        RoomType.objects.all().delete()
        RoomTypeAmenity.objects.all().delete()
        AccommodationImage.objects.all().delete()
        FreeService.objects.all().delete()
        AccommodationService.objects.all().delete()
        SharedFacility.objects.all().delete()
        AccommodationFacility.objects.all().delete()
        Dormitory.objects.all().delete()
        AccommodationDormitory.objects.all().delete()
        GeneralRoom.objects.all().delete()
        AccommodationRoom.objects.all().delete()
        Review.objects.all().delete()
        AgeGroup.objects.all().delete()
        TravelType.objects.all().delete()
        Reservation.objects.all().delete()
        Coupon.objects.all().delete()
        UserCoupon.objects.all().delete()
        AccommodationPayment.objects.all().delete()
        PaymentMethod.objects.all().delete()
=======

# Create your tests here.
>>>>>>> 4aaed4f... Add: Accommodation 숙소디테일 API 구현, 유닛테스트 완료
