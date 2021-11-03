from django.db import models
from user.models import Customer
from django.utils import timezone

# Create your models here.
class Hospital_Detail(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.CharField(max_length=1000)
    hospital_district = models.CharField(max_length=200)
    hospital_city = models.CharField(max_length=200)
    hospital_state = models.CharField(max_length=200)
    hospital_pin = models.IntegerField(default=0)
    hospital_rating = models.IntegerField(default=0)
    hospital_contact = models.IntegerField(default=987654321012)
    hospital_image = models.FileField(upload_to='hospital/images', default='')
    hospital_addition_date = models.DateField(default=timezone.now())

    def __str__(self):
        return self.hospital_name

class Hotel_Detail(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    hotel_name = models.CharField(max_length=200)
    hotel_pin = models.IntegerField(default=0)
    hotel_rating = models.IntegerField(default=0)
    hotel_price = models.IntegerField(default=0)
    hotel_description = models.CharField(default='', max_length=5000)
    hotel_contact = models.IntegerField(default=9876543210)
    hotel_image_1 = models.FileField(upload_to='hotel/images', default='')
    hotel_image_2 = models.FileField(upload_to='hotel/images', default='')
    hotel_image_3 = models.FileField(upload_to='hotel/images', default='')
    hotel_image_4 = models.FileField(upload_to='hotel/images', default='')
    hotel_image_5 = models.FileField(upload_to='hotel/images', default='')
    hotel_addition_date = models.DateField(default=timezone.now())

    def __str__(self):
        return self.hotel_name

