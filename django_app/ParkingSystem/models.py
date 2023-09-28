from django.db import models

# Create your models here.
class Car(models.Model):
    license_plate = models.CharField(max_length=10, unique=True)
    parked_at = models.DateTimeField(null=True, blank=True, max_length=9)
    car_type = models.CharField(max_length=255,default='小型车')
    def __str__(self):
        return self.license_plate
    

class ParkingRecord(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    license_plate = models.CharField(max_length=10)

class ParkingRate(models.Model):
    car_type = models.CharField(max_length=255,)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

class GlobalSettings(models.Model):
    parking_spots = models.PositiveIntegerField()
    origin_parking_spots = models.PositiveIntegerField()

