from django.db import models
from user.models import Customer, Service_Boy
from hospital.models import Hospital_Detail
from service.models import Service_Chosen
# Create your models here.
import datetime

class Admin_Control(models.Model):
    Order_ID = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_chosen = models.ForeignKey(Service_Chosen, on_delete=models.CASCADE, default='')
    service_boy = models.ForeignKey(Service_Boy, on_delete=models.CASCADE)
    pickup_address = models.CharField(max_length=1000)
    drop_address = models.CharField(max_length=1000)
    hospital = models.ForeignKey(Hospital_Detail, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, default='')
    price = models.IntegerField()
    payment_method = models.CharField(default='pending', max_length=100)
    service_date_time = models.CharField(default='', max_length=100)
    order_date = models.DateTimeField(default=datetime.datetime.now())


class Customer_Ongoing_Trip(models.Model):
    customer_trip_id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField(default=0)
    customer_FName = models.CharField(default='', max_length=1000)
    customer_LName = models.CharField(default='', max_length=1000)
    customer_mobile = models.CharField(default='', max_length=20)
    date_of_booking = models.DateTimeField(default=datetime.datetime.now())
    date_of_service = models.CharField(default='', max_length=100)
    amount = models.IntegerField(default=0)
    service_boy_id = models.IntegerField(default=0)
    service_boy_name = models.CharField(default='', max_length=200)
    gender = models.CharField(default='', max_length=50)
    hospital_name = models.CharField(default='', max_length=1000)
    hospital_id = models.IntegerField(default=0)
    selected_service = models.CharField(default='', max_length=2000)
    start_date_time = models.DateTimeField(default=datetime.datetime.now())

class Service_Boy_Ongoing_Trip(models.Model):
    service_boy_trip_id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField(default=0)
    customer_FName = models.CharField(default='', max_length=1000)
    customer_LName = models.CharField(default='', max_length=1000)
    customer_mobile = models.CharField(default='', max_length=20)
    service_boy_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    service_boy_name = models.CharField(default='', max_length=200)
    date_of_booking = models.DateTimeField(default=datetime.datetime.now())
    date_of_service = models.CharField(default='', max_length=100)
    hospital_name = models.CharField(default='', max_length=1000)
    hospital_id = models.IntegerField(default=0)
    selected_service = models.CharField(default='', max_length=2000)
    start_date_time = models.DateTimeField(default=datetime.datetime.now())


class Customer_Service_Hist(models.Model):
    customer_trip_id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField(default=0)
    customer_FName = models.CharField(default='', max_length=1000)
    customer_LName = models.CharField(default='', max_length=1000)
    customer_mobile = models.CharField(default='', max_length=20)
    date_of_booking = models.DateTimeField(default=datetime.datetime.now())
    date_of_service = models.CharField(default='', max_length=100)
    selected_service = models.CharField(default='', max_length=2000)
    status = models.CharField(default='', max_length=100)
    amount = models.IntegerField(default=0)
    service_boy_id = models.IntegerField(default=0)
    service_boy_name = models.CharField(default='', max_length=200)
    hospital_name = models.CharField(default='', max_length=1000)
    hospital_id = models.IntegerField(default=0)

class Service_Boy_Service_Hist(models.Model):
    service_boy_trip_id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField()
    customer_FName = models.CharField(default='', max_length=1000)
    customer_LName = models.CharField(default='', max_length=1000)
    customer_mobile = models.CharField(default='', max_length=20)
    status = models.CharField(default='', max_length=100)
    amount = models.IntegerField(default=0)
    service_boy_id = models.IntegerField(default=0)
    service_boy_name = models.CharField(default='', max_length=200)
    date_of_booking = models.DateTimeField(default=datetime.datetime.now())
    date_of_service = models.CharField(default='', max_length=100)
    hospital_name = models.CharField(default='', max_length=1000)
    hospital_id = models.IntegerField(default=0)
    selected_service = models.CharField(default='', max_length=2000)