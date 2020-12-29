from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_talbe = 'regions'

class Airport(models.Model):
    name   = models.CharField(max_length=45)
    code   = models.CharField(max_length=45)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        db_table = 'airports'

class Airline(models.Model):
    name     = models.CharField(max_length=45)
    logo_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'airlines'

class SeatClass(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'seat_classes'

class DetailedPrice(models.Model):
    base_fare              = models.DecialField(max_digits=10, decimal_places=2)
    fuel_surcharge         = models.DecialField(max_digits=10, decimal_places=2, default=0)
    tax_and_utility_charge = models.DecialField(max_digits=10, decimal_places=2, default=8000)
    service_fee            = models.DecialField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'detailed_price'

class Flight(models.Model):
    airline           = models.ForeignKey(Airline, on_delete=models.CASCADE)
    number            = models.CharField(max_length=45)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure')
    arrival_airport   = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival')
    departure_time    = models.TimeField()
    arrival_time      = models.TimeField()
    departure_date    = models.DateField()
    arrival_date      = models.DateField()
    seat_class        = models.ForeignKey(SeatClass, on_delete=models.CASCADE)
    remain_seat       = models.IntegerField(default=9)
    total_price       = models.DecialField(max_digits=10, decimal_places=2)
    detailed_price    = models.ForeignKey(DetailedPrice, on_delete=models.CASCADE)

    class Meta:
        db_table = 'flights'

class Gender(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'genders'

class Nationality(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'nationalities'

class PassengerInformation(models.Model):
    name        = models.CharField(max_length=45)
    gender      = models.ForeignKey(Gender, on_delete=models.CASCADE)
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE)
    birth_date  = DateField()

    class Meta:
        db_table = 'passenger_informations'

class Payment(models.Model):
    cardholder_name   = models.CharField(max_length=45)
    card_company      = models.CharField(max_length=45)
    card_number       = models.IntegerField()
    expiration_date   = models.DateField()
    installment_month = models.IntegerField()
    card_password     = models.IntegerField()
    birth_date        = models.IntegerField()

    class Meta:
        db_table = 'payments'

class FlightBookingInformation(models.Model):
    user                     = models.ForeignKey(user.User, on_delete=models.CASCADE)
    flight                   = models.ForeignKey(Flight, on_delete=models.CASCADE)
    phone_number             = models.CharField(max_length=45)
    passenger_information    = models.ForeignKey(PassengerInformation, on_delete=models.CASCADE)
    payment                  = models.ForeignKey(Payment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'flight_booking_informations'

class PassengerType(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'passenger_types'

class FlightPassenger(models.Model):
    passenger_type             = models.ForeignKey(PassengerType, on_delete=models.CASCADE)
    number                     = models.IntegerField()
    flight_booking_information = models.ForeignKey(FlightBookingInformation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'flight_passengers'
