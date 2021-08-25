from django.contrib import admin
from .models import Customer, Service_Boy, Temp

admin.site.register(Customer)
admin.site.register(Temp)


@admin.register(Service_Boy)
class Service_BoyAdmin(admin.ModelAdmin):
    list_display=['email', 'available', 'status']
