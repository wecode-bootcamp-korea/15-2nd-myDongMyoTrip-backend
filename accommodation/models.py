from django.db import models

class Theme(models.Model):
    name                = models.CharField(max_length=45)
    accommodation_theme = models.ManyToManyField('Accommodation', through='AccommodationTheme')
    
    class Meta:
        db_table = 'themes'

class AccommodationTheme(models.Model):
    theme         = models.ForeignKey('Theme', on_delete=models.CASCADE)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accommodation_themes'

class Accommodation(models.Model):
    name                      = models.CharField(max_length=45)
    price                     = models.DecimalField(max_digits=10, decimal_places=2)
    description               = models.CharField(max_length=500)
    number_of_guest           = models.IntegerField(default=1)
    star_rating               = models.DecimalField(max_digits=5, decimal_places=2)
    check_in                  = models.DateField()
    check_out                 = models.DateField()
    address                   = models.CharField(max_length=100)
    is_immediate_confirmation = models.BooleanField(default=False)
    host                      = models.ForeignKey('Host', on_delete=models.CASCADE, null=True)
    accommodation_service     = models.ManyToManyField('FreeService', through='AccommodationService')
    accommodation_facility    = models.ManyToManyField('SharedFacility', through='AccommodationFacility')
    accommodation_dormitory   = models.ManyToManyField('Dormitory', through='AccommodationDormitory')
    accommodation_room        = models.ManyToManyField('GeneralRoom', through='AccommodationRoom')

    class Meta:
        db_table = 'accommodations'

class Host(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.CharField(max_length=2000)

    class Meta:
        db_table = 'hosts'

class RoomAmenity(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'room_amenities'


class RoomType(models.Model):
    name                = models.CharField(max_length=45)
    price               = models.DecimalField(max_digits=10, decimal_places=2)
    minimum             = models.IntegerField(default=1)
    maximum             = models.IntegerField(default=2)
    number_of_bed       = models.IntegerField(default=1)
    minimum_reservation = models.IntegerField(default=1)
    image_url           = models.CharField(max_length=2000, null=True)
    accommodation       = models.ForeignKey('Accommodation', on_delete=models.CASCADE) 
    room_type_amenity   = models.ManyToManyField('RoomAmenity', through='RoomTypeAmenity')

    class Meta:
        db_table = 'room_types'

class RoomTypeAmenity(models.Model):
    room_type    = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    room_amenity = models.ForeignKey('RoomAmenity', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'room_type_amenities'

class AccommodationImage(models.Model):
    image_url     = models.CharField(max_length=2000)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accommodation_images'

class FreeService(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.CharField(max_length=2000, null=True)

    class Meta:
        db_table = 'free_services'

class AccommodationService(models.Model):
    free_service  = models.ForeignKey('FreeService', on_delete=models.CASCADE)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'accommodation_services'

class SharedFacility(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.CharField(max_length=2000, null=True)

    class Meta:
        db_table = 'shared_facilities'

class AccommodationFacility(models.Model):
    shared_facility = models.ForeignKey('SharedFacility', on_delete=models.CASCADE)
    accommodation   = models.ForeignKey('Accommodation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accommodation_facilities'

class Dormitory(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'dormitories'

class AccommodationDormitory(models.Model):
    dormitory     = models.ForeignKey('Dormitory', on_delete=models.CASCADE)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accommodation_dormitories'

class GeneralRoom(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'general_rooms'

class AccommodationRoom(models.Model):
    general_room  = models.ForeignKey('GeneralRoom', on_delete=models.CASCADE)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accommodation_rooms'

class Review(models.Model):
    user          = models.ForeignKey('user.User', on_delete=models.CASCADE)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE)
    context       = models.CharField(max_length=500)
    created_at    = models.DateTimeField(auto_now_add=True)
    star_rating   = models.DecimalField(max_digits=5, decimal_places=1)
    image_url     = models.CharField(max_length=2000)

    class Meta:
        db_table = 'reviews'

class AgeGroup(models.Model):
    age = models.CharField(max_length=45)

    class Meta:
        db_table = 'age_groups'

class TravelType(models.Model):
    type = models.CharField(max_length=45)

    class Meta:
        db_table = 'travel_types'
 
class Reservation(models.Model):
    accommodation         = models.ForeignKey('Accommodation', on_delete=models.CASCADE)
    user                  = models.ForeignKey('user.User', on_delete=models.CASCADE)
    gender                = models.ForeignKey('flight.Gender', on_delete=models.CASCADE)
    accommodation_payment = models.ForeignKey('AccommodationPayment', on_delete=models.CASCADE)
    age_group             = models.ForeignKey('AgeGroup', on_delete=models.CASCADE)
    travel_type           = models.ForeignKey('TravelType', on_delete=models.CASCADE)
    name                  = models.CharField(max_length=45)
    date_of_birth         = models.DateField()
    estimate_arrival_time = models.TimeField()
    total_price           = models.DecimalField(max_digits=15, decimal_places=2)
    is_privcy_agreement   = models.BooleanField(default=False)

    class Meta:
        db_table = 'reservations'
   
class Coupon(models.Model):
    code        = models.CharField(max_length=45)
    user_coupon = models.ManyToManyField('user.User', through='UserCoupon')

    class Meta:
        db_table = 'coupons'

class UserCoupon(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
    coupon      = models.ForeignKey('Coupon', on_delete=models.CASCADE)
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user_coupons'

class AccommodationPayment(models.Model):
    payment_method    = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, default=1)
    is_payment_status = models.BooleanField(default=False)
    total_price       = models.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        db_table = 'accommodation_payments'

class PaymentMethod(models.Model):
    name    = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'payment_methods'
