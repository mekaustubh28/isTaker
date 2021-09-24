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