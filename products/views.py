from django.shortcuts import render
from django.db.models import Q
from django.views.generic.list import ListView
from .models import Product
from django.views.generic.detail import DetailView

# por utilizar ListView es necesario definir el template_name y queryset, pues sino utilizar por valores por defecto definidos
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

class ProductDetailView(DetailView):
    # se indica cual es modelo
    # en la ruta se indica el parametro a utilizar para buscarse en el modelo
    model = Product
    template_name = 'products/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProductSearchListView(ListView):
    template_name = 'products/search.html'

    # sobreescribir el metodo del queryset
    def get_queryset(self):
        # con la Clase Q permite realizar multiples filtros
        filters = Q(title__icontains=self.query()) | Q(category__title__contains=self.query())
        return Product.objects.filter(filters)

    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['product_list'].count()
        return context
