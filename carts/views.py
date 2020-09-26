from django.shortcuts import render, redirect, get_object_or_404
from .utils import get_or_create_cart
from products.models import Product
from .models import CartProducts

# Create your views here.
def cart(request):
    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', {
      'cart': cart
    })

def add(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    # (valorLlave, valorPorDefecto)
    quantity = int(request.POST.get('quantity', 1))

    # cart.products.add(product, through_defaults = {
    #     'quantity': quantity
    # })

    # cart_product = CartProducts.objects.create(cart=cart, product=product, quantity=quantity)
    # para extender metodos al objecto objects, se debe de crear un manager
    # con objects se interactua con la base de datos
    cart_product = CartProducts.objects.create_or_update_quantity(cart=cart, product=product, quantity=quantity)


    return render(request, 'carts/add.html', {
        'quantity': quantity,
        'cart_product': cart_product,
        'product': product
    })

def remove(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    cart.products.remove(product)

    return redirect('carts:cart')
