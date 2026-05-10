from django.urls import path
from . import views

app_name = 'bakery'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('category/<str:category_id>/', views.category_items, name='category_items'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<str:category_id>/<str:item_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<path:key>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmed/<int:order_id>/', views.order_confirmed, name='order_confirmed'),
]
