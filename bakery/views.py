from django.shortcuts import render


def home(request):
    return render(request, 'bakery/home.html')


def menu(request):
    return render(request, 'bakery/menu.html')


def cart(request):
    return render(request, 'bakery/cart.html')


def checkout(request):
    return render(request, 'bakery/checkout.html')


def order_confirmed(request):
    return render(request, 'bakery/order_confirmed.html')
