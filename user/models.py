from django.db import models
from django.utils import timezone
# Create your models here.


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_husband_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    mobile = models.IntegerField()
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    city_village = models.CharField(max_length=100)
    PIN = models.IntegerField()
    Adhaar = models.IntegerField()
    password = models.CharField(max_length=200)
    created_on = models.DateField(default=timezone.now())

    def __str__(self):
        return self.email


class Service_Boy(models.Model):
    service_boy_id = models.AutoField(primary_key=True)
    ID = models.CharField(max_length=10 , default='19990101')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    father_husband_name = models.CharField(max_length=200, default='')
    gender = models.CharField(max_length=200, default='')
    address = models.CharField(max_length=200, default='')
    city_village = models.CharField(max_length=100, default='')
    district = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    pin = models.CharField(max_length=200, default='')
    email = models.EmailField(max_length=254)
    mother_tongue = models.CharField(max_length=100, default='')
    rating = models.FloatField(default=0)
    education = models.CharField(max_length=100, default='')
    DOB = models.CharField(max_length=50, default='')
    pin_serve = models.CharField(max_length=200,default='')
    languages = models.CharField(max_length=200, default='')
    mobile = models.IntegerField()
    adhaar = models.IntegerField()
    pan = models.IntegerField()
    account = models.CharField(max_length=200, default='')
    ifsc_code = models.CharField(max_length=200, default='')
    branch = models.CharField(max_length=200,default='')
    image = models.FileField(upload_to='user/images')
    password = models.CharField(max_length=200, default='')
    status = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    created_on = models.DateField(default=timezone.now())
    

class Temp(models.Model):
    image = models.FileField(upload_to='user/temp_images')
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.email