from django.db import models
from user.models import Customer, Service_Boy
from hospital.models import Hospital_Detail
from django.utils import timezone
import datetime

# Create your models here.
class Package(models.Model):
    package_id = models.AutoField(primary_key=True)
    package_name = models.CharField(max_length=100, default='package')
    package_creation_date = models.DateField()

    def __str__(self):
        return self.package_name

class Service(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=50, default='service')
    service_amount = models.IntegerField(default=0)
    service_addition_date = models.DateField()

    def __str__(self):
        return self.service_name

class Service_Chosen(models.Model):
    customer_chosen = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_chosen_id = models.AutoField(primary_key=True)
    service_list = models.CharField(max_length=200)
    total_price = models.CharField(max_length=100)
    price = models.CharField(max_length=100,default='')
    coupon = models.CharField(max_length=100,default='No Coupon')
    hospital_id = models.CharField(max_length=10, default='')
    hospital_name = models.CharField(max_length=100, default='')
    service_boy_id = models.CharField(max_length=200, default='')
    service_offer_amount = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default='In Cart')
    service_addition_date = models.DateTimeField(default=datetime.datetime.now())

class Deals_and_Offer(models.Model):
    offer_id = models.AutoField(primary_key=True)
    offer_name = models.CharField(max_length=100, default='season offer')
    offer_amount = models.IntegerField(default=0)
    offer_code = models.CharField(max_length=100, default='')
    offer_date = models.DateField(default=timezone.now())
    valid_to = models.DateField()

    def __str__(self):
        return self.offer_code

class Confirm_Order(models.Model):
    Order_ID = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_chosen = models.ForeignKey(Service_Chosen, on_delete=models.CASCADE, default='')
    # service_boy = models.ForeignKey(Service_Boy, on_delete=models.CASCADE)
    pickup_address = models.CharField(max_length=1000)
    drop_address = models.IntegerField()
    otp = models.CharField(max_length=6, default='')
    hospital_name = models.CharField(default='', max_length=1000)
    price = models.IntegerField()
    PIN = models.CharField(max_length=100, default='')
    payment_method = models.CharField(default='pending', max_length=100)
    service_date_time = models.CharField(default='', max_length=100)
    order_date = models.DateTimeField(default=datetime.datetime.now())

