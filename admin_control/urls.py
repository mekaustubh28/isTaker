from django.urls import path

from . import views

app_name = 'adminControl'

urlpatterns = [
    path('jhbo92dasdSABoiu8o08BFjkl', views.admin_control, name='admin_control'),
    path('jhbo92dasdSABoiu8o08BFjkl/hospitals', views.hospitals, name='hospitals'),
    path('jhbo92dasdSABoiu8o08BFjkl/pending_service', views.pending_service, name='pending_service'),
    path('jhbo92dasdSABoiu8o08BFjkl/pending_applications', views.pending_applications, name='pending_applications'),
    path('jhbo92dasdSABoiu8o08BFjkl/all_services', views.all_services, name='all_services'),
    path('jhbo92dasdSABoiu8o08BFjkl/customers', views.customer, name='customer'),
    path('jhbo92dasdSABoiu8o08BFjkl/service_boys', views.service_boys, name='service_boys'),
    path('admin_staff_logout', views.admin_staff_logout, name='admin_staff_logout'),
]
