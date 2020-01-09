from django.urls import path
from . import views

# <PK> indica q el parametro es el # ID
urlpatterns = [
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product')
]
