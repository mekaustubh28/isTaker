from django.contrib import admin
from .models import Package, Service, Service_Chosen, Deals_and_Offer, Confirm_Order
# Register your models here.

admin.site.register(Package)
admin.site.register(Deals_and_Offer)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display=['service_name', 'package']

@admin.register(Service_Chosen)
class Service_ChosenAdmin(admin.ModelAdmin):
    list_display=['service_chosen_id', 'customer_chosen', 'service_addition_date', 'status']

@admin.register(Confirm_Order)
class Confirm_OrderAdmin(admin.ModelAdmin):
    list_display=['Order_ID', 'price', 'service_date_time', 'order_date','payment_method']

