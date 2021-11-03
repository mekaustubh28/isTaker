from django.contrib import admin
from .models import Hospital_Detail, Hotel_Detail
# Register your models here.


@admin.register(Hospital_Detail)
class Hospital_DetailAdmin(admin.ModelAdmin):
    list_display=['hospital_name', 'hospital_id', 'hospital_pin', 'hospital_city']

@admin.register(Hotel_Detail)
class Hotel_DetailAdmin(admin.ModelAdmin):
    list_display=['hotel_name', 'hotel_id', 'hotel_pin']



