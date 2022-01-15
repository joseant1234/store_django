from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order


def validate_cart_and_order(function):
    def wrap(request, *args, **kwargs):
        cart = get_or_create_cart(request)
        order = get_or_create_order(cart, request)
        # la funcion recibe 3 parametros obligatorios: request, cart, order
        return function(request, cart, order, *args, **kwargs)
    return wrap
