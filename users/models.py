# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models

from orders.common import OrderStatus


# si es necesario sobreescribir el modeo User, se debe crear un modelo user q extienden de AbstractUser o AbstractBseUser
# AbstractUser (se puede utilizar atributos: username, first_name, last_name, email, password, groups, user_permissions, is_staff, is_active, is_superuser, last_login, date_joined) - AbstractBaseUser (se puede utilizar atributos: id, password, last_login)
class User(AbstractUser):
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    def has_shipping_address(self):
        return self.shipping_address is not None

    def orders_completed(self):
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')

# para agregar metodos a un model existente se usa proxy model. El proxy model no genera una tabla en la base de datos
class Customer(User):
    class Meta:
        proxy = True

    # metodos a extender a la clase User

    def get_products(self):
        return []

# agregar un modelo con una relacion uno a uno si es necesario agregar atributos
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
