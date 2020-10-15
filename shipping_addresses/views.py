from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import ShippingAddress
from .forms import ShippingAddressForm
from django.contrib import messages

# Create your views here.
class ShippingAddressListView(ListView):
    model = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

def create(request):
    # inicializar el formulario con los valores del request con el metodo post
    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # con el commit en false, el metodo save creará una instancia shipping address pero no la va a persistir
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        # se asigna default si es q no hay direcciones para el usuario
        shipping_address.default = not ShippingAddress.objects.filter(user=request.user).exists()
        # con el usuario asignado se persiste el shipping address
        shipping_address.save()

        messages.success(request, 'Dirección creada')
        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/create.html', {
        'form': form
    })
