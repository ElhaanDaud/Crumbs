from django.urls import path
from . import views

app_name = 'bakery'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmed/', views.order_confirmed, name='order_confirmed'),
]
