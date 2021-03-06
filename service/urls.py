from django.urls import path

from . import views

app_name = 'service'

urlpatterns = [
    path('', views.index, name='index'),
    path('customer_dashboard/<int:myid>', views.customer_dashboard, name='customer_dashboard'),
    path('customer_dashboard/<int:myid>/search', views.search, name='search'),
    path('customer_dashboard/<int:myid>/order_confirm', views.order_confirm, name='order_confirm'),
    path('customer_dashboard/<int:myid>/orders', views.orders, name='orders'),
    path('customer_dashboard/<int:myid>/contact_us', views.contact_us, name='contact_us'),
    path('customer_dashboard/<int:myid>/my_account', views.my_account, name='my_account'),
    path('customer_dashboard/<int:myid>/service_boy_on_way', views.service_boy_on_way, name='service_boy_on_way'),
    path('logout', views.Logout, name='logout'),
]
