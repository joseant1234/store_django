from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product

# por utilizar ListView es necesario definir el template_name y queryset
# templateName es el nombre del template a utilizar
# queryset es la consulta para obtener el listado de objetos
class ProductListView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all().order_by('-id')

    # sobreescribir el metodo para pasar el contexto de la clase al template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de productos'
        context['products'] = context['product_list']

        return context
