from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Cake, Beverage, Cookie, Pastry, CustomerOrder
from .cart import get_cart, add_to_cart, remove_from_cart, clear_cart
from .forms import CustomerDetailsForm

import random


TIDBITS = [
    'Enjoy the best of baking with crumbs!',
    'Every flavour has a story to tell!',
    'Count the memories not the calories!',
    'We bet you will keep coming back!',
    'A wonderful gift for your loved ones!',
    'Celebrate with crumbs!',
]

NICEDAY_MESSAGES = [
    'Hope you have a good day :)',
    'Stay hydrated :)',
    'Just in case no one has told you already... you are amazing :)',
    'Be a rainbow in someones storm :)',
    'Perfection is accepting your imperfections :)',
]


def home(request):
    return render(request, 'bakery/home.html')


def menu_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'tidbit': random.choice(TIDBITS),
        'niceday': random.choice(NICEDAY_MESSAGES),
    }
    return render(request, 'bakery/menu.html', context)


def category_items(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    items = []
    price_label = ''
    unit_label = ''
    if category_id == 'C00':
        items = Cake.objects.all()
        price_label = 'Price (per kg)'
        unit_label = 'kg'
    elif category_id == 'B00':
        items = Beverage.objects.all()
        price_label = 'Price (medium)'
        unit_label = 'size'
    elif category_id == 'K00':
        items = Cookie.objects.all()
        price_label = 'Price (per 500g)'
        unit_label = 'g'
    elif category_id == 'P00':
        items = Pastry.objects.all()
        price_label = 'Price (per piece)'
        unit_label = 'piece'

    context = {
        'category': category,
        'items': items,
        'price_label': price_label,
        'unit_label': unit_label,
    }
    return render(request, 'bakery/category_items.html', context)


def add_to_cart_view(request, category_id, item_id):
    category = get_object_or_404(Category, pk=category_id)

    item = None
    price = 0
    name = ''
    weight = None
    size = None

    if category_id == 'C00':
        item = get_object_or_404(Cake, pk=item_id)
        name = item.name
        price = item.price_1kg
        weight = request.GET.get('weight', 0.5)
    elif category_id == 'B00':
        item = get_object_or_404(Beverage, pk=item_id)
        name = item.name
        price = item.price_medium
        size = request.GET.get('size', 'medium')
    elif category_id == 'K00':
        item = get_object_or_404(Cookie, pk=item_id)
        name = item.name
        price = item.price_500g
        weight = request.GET.get('weight', 500)
    elif category_id == 'P00':
        item = get_object_or_404(Pastry, pk=item_id)
        name = item.name
        price = item.price_per_piece

    add_to_cart(request, item_id, category_id, name, price,
                weight=weight, size=size)
    messages.success(request, f'{name} added to cart!')
    return redirect('bakery:category_items', category_id=category_id)


def remove_from_cart_view(request, key):
    remove_from_cart(request, key)
    messages.info(request, 'Item removed from cart.')
    return redirect('bakery:cart')


def cart_view(request):
    cart = get_cart(request)
    subtotal = sum(
        float(item['price']) * int(item['quantity'])
        for item in cart.values()
    )
    context = {
        'cart': cart,
        'subtotal': subtotal,
    }
    return render(request, 'bakery/cart.html', context)


def checkout_view(request):
    cart = get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('bakery:menu')

    form = CustomerDetailsForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        subtotal = sum(
            float(item['price']) * int(item['quantity'])
            for item in cart.values()
        )
        taxes = subtotal * 0.18
        delivery_charge = 0

        if form.cleaned_data['delivery_option'] == 'yes':
            if subtotal + taxes > 500:
                delivery_charge = 50
            else:
                messages.info(
                    request,
                    'Home delivery available for orders above ₹500 (after tax).'
                )
                grand_total = subtotal + taxes + delivery_charge
                return render(request, 'bakery/checkout.html', {
                    'form': form,
                    'cart': cart,
                    'subtotal': subtotal,
                    'taxes': taxes,
                    'delivery_charge': delivery_charge,
                    'grand_total': grand_total,
                    'delivery_not_eligible': True,
                })

        grand_total = subtotal + taxes + delivery_charge

        order = CustomerOrder.objects.create(
            name=form.cleaned_data['name'],
            phone_no=form.cleaned_data['phone_no'],
            address=(
                form.cleaned_data['address']
                if form.cleaned_data['delivery_option'] == 'yes'
                else '-'
            ),
            amount=int(grand_total),
        )

        clear_cart(request)
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('bakery:order_confirmed', order_id=order.id)

    subtotal = sum(
        float(item['price']) * int(item['quantity'])
        for item in cart.values()
    )
    taxes = subtotal * 0.18
    delivery_charge = 50 if subtotal + taxes > 500 else 0
    grand_total = subtotal + taxes + delivery_charge

    context = {
        'form': form,
        'cart': cart,
        'subtotal': subtotal,
        'taxes': taxes,
        'delivery_charge': delivery_charge,
        'grand_total': grand_total,
    }
    return render(request, 'bakery/checkout.html', context)


def order_confirmed(request, order_id):
    order = get_object_or_404(CustomerOrder, pk=order_id)
    return render(request, 'bakery/order_confirmed.html', {'order': order})
