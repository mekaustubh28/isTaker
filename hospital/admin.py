from django.contrib import admin
from .models import Hospital_Detail
# Register your models here.


@admin.register(Hospital_Detail)
class Hospital_DetailAdmin(admin.ModelAdmin):
    list_display=['hospital_name', 'hospital_id', 'hospital_pin', 'hospital_city']


