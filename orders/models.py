import uuid
from enum import Enum

from django.db import models
from django.db.models.signals import pre_save

from carts.models import Cart
from shipping_addresses.models import ShippingAddress
from users.models import User


class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

choices = [(tag, tag.value) for tag in OrderStatus]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=choices, default=OrderStatus.CREATED) #Enum
    shipping_total = models.DecimalField(default=5, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    shipping_address = models.ForeignKey(ShippingAddress, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id

    def get_or_set_shipping_address(self):
        if self.shipping_address:
            return self.shipping_address
        shipping_address = self.user.shipping_address
        if shipping_address:
            self.shipping_address = shipping_address
            self.save()

        return shipping_address

    def get_total(self):
        return self.cart.total + self.shipping_total

    def update_total(self):
        self.total = self.get_total()
        self.save()

def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        # str lo convierte a una cadena
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()


# pre_save.connect(registar callback, clase sender)
pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)
