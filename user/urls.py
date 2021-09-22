from django.urls import path
from . import views
from service.views import search

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.Login, name='Login'),
    path('signUp', views.SignUp, name='SignUp'),
    path('hospital_search', views.hospital, name= 'search'),
    path('contact_us', views.contact_us, name= 'contact_us'),
    path('create_new_account', views.create_new_account, name='create_new_account'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    # path('customer_dashboard', views.customer_dashboard, name='customer_dashboard'),
]