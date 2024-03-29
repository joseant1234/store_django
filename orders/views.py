from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import EmptyQuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from carts.utils import destroy_cart, get_or_create_cart
from orders.mails import Mail
from shipping_addresses.models import ShippingAddress

from .models import Order
from .utils import breadcrumb, destroy_order, get_or_create_order
from .decorators import validate_cart_and_order
import threading

class OrderListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'orders/orders.html'

    def get_queryset(self):
        # EmptyQuerySet devuelve una lista vacía
        # return EmptyQuerySet
        return self.request.user.orders_completed()


# decorador que redirige si el usuario no está autenticado
@login_required(login_url='login')
@validate_cart_and_order
def order(request, cart, order):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)

    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb()
    })

@login_required(login_url='login')
@validate_cart_and_order
def address(request, cart, order):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)

    shipping_address = order.get_or_set_shipping_address()
    # can_choose_address = request.user.shippingaddress_set.count() > 1
    can_choose_address = request.user.has_shipping_addresses()

    return render(request, 'orders/address.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'can_choose_address': can_choose_address,
        'breadcrumb': breadcrumb(address=True),
    })

@login_required(login_url='login')
def select_address(request):
    # shipping_addresses = request.user.shippingaddress_set.all()
    shipping_addresses = request.user.addresses

    return render(request, 'orders/select_address.html', {
        'breadcrumb': breadcrumb(address=True),
        'shipping_addresses': shipping_addresses
    })

@login_required(login_url='login')
@validate_cart_and_order
def set_address(request, cart, order, pk):
    # el parametro pk seria *args, **kwargs del decorator
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)

    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    order.update_shipping_address(shipping_address)

    return redirect('orders:address')

@login_required(login_url='login')
@validate_cart_and_order
def confirm(request, cart, order):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)

    shipping_address =  order.shipping_address

    if shipping_address is None:
        return redirect('orders:address')

    return render(request, 'orders/confirm.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(address=True, confirmation=True)
    })

@login_required(login_url='login')
@validate_cart_and_order
def cancel(request, cart, order):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()
    destroy_cart(request)
    destroy_order(request)

    messages.error(request, 'Orden cancelada')
    return redirect('index')

@login_required(login_url='login')
@validate_cart_and_order
def complete(request, cart, order):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.complete()
    # en target se pone la tarea q se quiere ejecutar en segundo plano
    # en una tupla se indica los argumentos
    thread = threading.Thread(target=Mail.send_complete_order, args=(
        order, request.user
    ))
    thread.start()

    destroy_cart(request)
    destroy_order(request)

    messages.success(request, 'Compra completada exitosamente')
    return redirect('index')
