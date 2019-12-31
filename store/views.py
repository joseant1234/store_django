from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django # se renombra la funcion pues ya esta definido en la vista la funcion login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout as logout_django
from .forms import RegisterForm
from django.contrib.auth.models import User

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
            messages.success(request, 'Bienvenido {}'.format(user.username))
            # recibe como argunmento el nombre de la ruta
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña no válidos')

    return render(request, 'users/login.html', {})

def logout(request):
    # el objeto request tiene la sesion
    logout_django(request)
    messages.success(request, 'La sesión de usuario fue cerrada')
    return redirect('login')

def register(request):
    # inicializa con valores
    # form = RegisterForm({
    #     'username': 'Usuario',
    #     'email': 'usuario@email.com'
    # })
    # si la peticion es por el metodo POST utiliza los datos enviados en el formulario
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # cleaned_data trae la informacion del formulario
        # username = form.cleaned_data.get('username')
        # email = form.cleaned_data.get('email')
        # password = form.cleaned_data.get('password')

        # el metodo create_user se encarga de encriptar la constraseña
        # user = User.objects.create_user(username, email, password)

        user = form.save()

        if user:
            login_django(request, user)
            messages.success(request, 'Usuario fue creado')
            return redirect('index')

    return render(request, 'users/register.html', { 'form': form })
