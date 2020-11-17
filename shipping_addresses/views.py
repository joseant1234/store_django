from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import ShippingAddress
from .forms import ShippingAddressForm
from django.shortcuts import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

# para proteger el acceso con el login se hereda al comienzo de la clase LoginRequiredMixin
class ShippingAddressListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'shipping_addresses/update.html'
    success_message = 'Dirección actualizada'

    def get_success_url(self):
        return reverse('shipping_addresses:shipping_addresses')


# decorador login_required permite acceder a la vista si está autenticado,
# login url es para redirect en caso el usuario cuando no puede entrar
@login_required(login_url='login')
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
