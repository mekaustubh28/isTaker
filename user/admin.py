from django.contrib import admin
from .models import Customer, Service_Boy, Temp, Admin_Staff

admin.site.register(Customer)
admin.site.register(Temp)


@admin.register(Service_Boy)
class Service_BoyAdmin(admin.ModelAdmin):
    list_display=['email', 'available', 'status', 'current_status']

@admin.register(Admin_Staff)
class Admin_StaffAdmin(admin.ModelAdmin):
    list_display=['first_name', 'email', 'status']
