from .models import Cart

def get_or_create_cart(request):
    # si el usuario está autenticado se obtiene el usuario actual
    user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id') # si no existe la llave hace un return de un None
    # no se usa get porque envia una exception si no encuentra un registro con esa condicional
    # filter hace un return de una lista
    # si la lista está vacia, el metodo first return un None
    cart = Cart.objects.filter(cart_id=cart_id).first()

    if cart is None:
        cart = Cart.objects.create(user=user)

    # si el usuario existe (está autenticado) y el carrito actual no tiene usuario
    if user and cart.user is None:
        cart.user = user
        cart.save()

    request.session['cart_id'] = cart.cart_id

    return cart
