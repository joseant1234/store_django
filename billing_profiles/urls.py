from django.urls import path

from products.urls import urlpatterns

from . import views

app_name = 'billing_profiles'

urlpatterns = [
    path('new', views.create, name='create')
]
