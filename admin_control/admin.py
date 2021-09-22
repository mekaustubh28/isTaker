from django.contrib import admin
from .models import Admin_Control, Customer_Ongoing_Trip, Customer_Service_Hist, Service_Boy_Ongoing_Trip, Service_Boy_Service_Hist, Testimonial
# Register your models here.

@admin.register(Admin_Control)
class Admin_ControlAdmin(admin.ModelAdmin):
    list_display=['Order_ID', 'customer', 'service_boy','payment_method', 'service_date_time', 'order_date']

@admin.register(Customer_Ongoing_Trip)
class Customer_Ongoing_TripAdmin(admin.ModelAdmin):
    list_display=['customer_id', 'service_boy_id', 'hospital_id']

@admin.register(Customer_Service_Hist)
class Customer_Service_HistAdmin(admin.ModelAdmin):
    list_display=['customer_id', 'service_boy_id', 'hospital_id', 'status']

@admin.register(Service_Boy_Ongoing_Trip)
class Service_Boy_Ongoing_TripAdmin(admin.ModelAdmin):
    list_display=['service_boy_id', 'customer_id', 'hospital_id']

@admin.register(Service_Boy_Service_Hist)
class Service_Boy_Service_HistAdmin(admin.ModelAdmin):
    list_display=['service_boy_id', 'customer_id', 'hospital_id', 'status']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display=['customer_id', 'date_time']

