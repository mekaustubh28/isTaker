from django.urls import path

from . import views

app_name = 'hospital'

urlpatterns = [
    path('hospital_list', views.index, name='index'),
]
