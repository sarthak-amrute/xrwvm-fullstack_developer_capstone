from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Station Wagon'),
        ('COUPE', 'Coupe'),
        ('TRUCK', 'Pickup Truck'),
        ('MINIVAN', 'Mini Van'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=10, choices=CAR_TYPES, default='SEDAN')
    year = models.IntegerField(default=2023)
    dealer_id = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.car_make.name} {self.name}"
