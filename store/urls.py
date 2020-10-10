"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from products.views import ProductListView
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings

# con el metodo as_view le indica a django q se va a utlizar la clase como una vista
# el include('products.urls') permite incluir las rutas de la aplicacion products
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProductListView.as_view(), name='index'),
    path('users/login', views.login, name='login'),
    path('users/logout', views.logout, name="logout"),
    path('users/register', views.register, name="register"),
    path('products/', include('products.urls')),
    path('carts/', include('carts.urls')),
    path('order/', include('orders.urls')),
    path('addresses', include('shipping_addresses.urls')),
]

# permite mostrar las imagenes en el template
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
