from django.urls import path

from . import views

app_name = 'service_boy'

urlpatterns = [
    path('/<int:ID>', views.service_boy_dashboard, name='service_boy_dashboard'),
    path('/<int:ID>/start_ride', views.start_ride, name='start_ride'),
    path('/<int:ID>/all_services', views.all_services, name='all_services'),
    path('/<int:ID>/availability', views.availability, name='availability'),

]
