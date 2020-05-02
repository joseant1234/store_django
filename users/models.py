from django.db import models
from django.contrib.auth.models import User

# para agregar metodos a un model existente se usa proxy model. El proxy model no genera una tabla en la base de datos
class Customer(User):
    class Meta:
        proxy = True

    # metodos a extender a la clase User

    def get_products(self):
        return []
