from django.urls import path
from . import views

# con app_name se esta definiendo q las rutas son parte de la aplicación
app_name = 'products'

# <PK> indica q el parametro es el # ID
urlpatterns = [
    path('search', views.ProductSearchListView.as_view(), name='search'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product'),
]
