from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html', {
        'message': 'Listado de productos',
        'title': 'Productos',
        'products': [
            {
                'title': 'Playera',
                'price': 5,
                'stock': True
            },
            {
                'title': 'Polo',
                'price': 8,
                'stock': True
            },
            {
                'title': 'Raton',
                'price': 25,
                'stock': True
            }
        ]
    })
