from django.forms import ModelForm
from .models import ShippingAddress

# crear un formulario a partir del modelo
class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        # atributos del modelo que estarán en el formulario
        fields = [
            'line1', 'line2', 'city', 'state', 'country', 'postal_code', 'reference'
        ]
