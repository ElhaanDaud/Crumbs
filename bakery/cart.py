CART_SESSION_KEY = 'crumbs_cart'


def get_cart(request):
    return request.session.get(CART_SESSION_KEY, {})


def add_to_cart(request, item_id, category_id, name, price, quantity=1, weight=None, size=None):
    cart = request.session.get(CART_SESSION_KEY, {})
    key = f'{category_id}:{item_id}'
    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'item_id': item_id,
            'category_id': category_id,
            'name': name,
            'price': float(price),
            'quantity': quantity,
            'weight': weight,
            'size': size,
        }
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def remove_from_cart(request, key):
    cart = request.session.get(CART_SESSION_KEY, {})
    cart.pop(key, None)
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def clear_cart(request):
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True
