from django.shortcuts import reverse, render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import ShippingAddress
from .forms import ShippingAddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order
from django.http import HttpResponseRedirect

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

    # metodo permite implementar validaciones sobre la petición
    def dispath(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    # redirigir a los usuario no autenticado
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/delete.html'
    # redigir a la url una vez que se ejecutó la acción
    success_url = reverse_lazy('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        # se obtiene la dirección, si la direccion es por default renvia a la lista de direcciones
        if self.get_object().default:
            return redirect('shipping_addresses:shipping_addresses')

        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        # si tiene al menos una orden no puede ser eliminado y se hace redirect a la vista de direcciones
        if self.get_object().has_orders():
            return redirect('shipping_addresses:shipping_addresses')

        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)

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
        # shipping_address.default = not ShippingAddress.objects.filter(user=request.user).exists()

        shipping_address.default = not request.user.has_shipping_address()
        # con el usuario asignado se persiste el shipping address
        shipping_address.save()

        if request.GET.get('next'):
            if request.GET['next'] == reverse('orders:address'):
                cart = get_or_create_cart(request)
                order = get_or_create_order(cart, request)
                order.update_shipping_address(shipping_address)

                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Dirección creada')
        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/create.html', {
        'form': form
    })

@login_required(login_url='login')
def default(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    if request.user.has_shipping_address():
        request.user.shipping_address.update_default()

    shipping_address.update_default(True)

    return redirect('shipping_addresses:shipping_addresses')
