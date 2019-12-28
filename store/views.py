from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django # se renombra la funcion pues ya esta definido en la vista la funcion login
from django.shortcuts import redirect

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

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # si existe el usuario, muestra el user sino envia None a la variable
        user = authenticate(username=username, password=password)

        if user:
            # se va a generar sesion. Requiera la peticion y el usuario
            login_django(request, user)
            # recibe como argunmento el nombre de la ruta
            return redirect('index')

    return render(request, 'users/login.html', {})
