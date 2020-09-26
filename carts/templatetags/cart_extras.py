from django import template

register = template.Library()
# registrar las  funciones como filters

@register.filter()
def quantity_products_format(quantity = 1):
    return '{} {}'.format(quantity, 'productos' if quantity > 1 else 'producto')

@register.filter()
def quantity_add_format(quantity = 1):
    return '{} {}'.format(
        quantity_products_format(quantity),
        'agregados' if quantity > 1 else 'agregado'
    )
