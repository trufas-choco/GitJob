from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json

# --- Vistas de Plantillas (Corregidas) ---
def inicio_sesion(request):
    # CORREGIDO: Apunta a 'login.html' que sí existe en tus plantillas.
    return render(request, 'login.html')
    
@login_required # Es buena práctica proteger el feed
def feed(request):
    # CORREGIDO: Apunta a 'feed.html' que sí existe en tus plantillas.
    return render(request, 'feed.html')

# --- Vistas Comentadas (Plantillas Faltantes) ---
# Has pedido no crear nuevos HTML. Estas vistas no se pueden usar
# porque sus plantillas ('menu_usuario.html', 'otro_template.html', 
# 'perfil_pruebaa.html') no están en la carpeta 'templates'.

# def menu_usuario(request):
#     return render(request, 'menu_usuario.html') # Este HTML no existe
    
# def otro_template(request):
#     return render(request, 'otro_template.html') # Este HTML no existe
        
# @login_required
# def mi_perfil(request):
#      return render(request, 'perfil_pruebaa.html', {'u': request.user}) # Este HTML no existe


# --- Vistas de API (NUEVAS - Requeridas por tu JS) ---

@csrf_exempt # Necesario para recibir 'fetch' POST desde el frontend
def api_login(request):
    """
    Maneja el inicio de sesión que viene desde 'login.js'
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Asumimos que el 'phone' se guarda en el campo 'username' de Django
            phone = data.get('phone')
            password = data.get('password')

            user = authenticate(request, username=phone, password=password)

            if user is not None:
                login(request, user) # Inicia la sesión y guarda la cookie
                # Enviamos la URL que 'login.js' espera recibir
                return JsonResponse({'redirectUrl': '/feed/'})
            else:
                # Error de autenticación
                return JsonResponse({'error': 'Teléfono o contraseña incorrectos'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def api_user_me(request):
    """
    Devuelve los datos del usuario actual para 'home.js'
    """
    if not request.user.is_authenticated:
        # Devuelve el error 401 que 'home.js' espera
        return JsonResponse({'error': 'No autenticado'}, status=401)

    # Devuelve los datos que 'home.js' necesita para el saludo
    return JsonResponse({
        'first_name': request.user.first_name,
        'username': request.user.username
    })

def registro(request):
    """
    Esta vista se encarga de mostrar la página de registro (GET)
    Y de procesar la creación del usuario (POST).
    """

    # --- LÓGICA PARA CREAR LA CUENTA (CUANDO SE ENVÍA EL FORMULARIO) ---
    if request.method == 'POST':
        # 1. Obtenemos los datos del formulario (de account.html)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        password = request.POST.get('new-password')

        # 2. Usamos el teléfono como 'username' (para que coincida con tu login)
        username = phone

        # 3. VERIFICAMOS SI EXISTE
        # Consultamos la base de datos para ver si ya hay un usuario con ese teléfono
        if User.objects.filter(username=username).exists():
            # Si existe, enviamos un error de vuelta al formulario
            context = {'error': 'El número de teléfono ya está registrado.'}
            return render(request, 'account.html', context)

        # 4. CREAMOS LA CUENTA
        # Si no existe, creamos el nuevo usuario
        try:
            user = User.objects.create_user(
                username=username,      # Guardamos el teléfono como username
                password=password,      # Django encripta la contraseña
                first_name=first_name,
                last_name=last_name
            )

            # 5. (Recomendado) Iniciar sesión automáticamente
            login(request, user)

            # 6. Redirigir al 'feed' cuando todo sale bien
            return redirect('feed') # 'feed' es el name= de tu URL en app/urls.py

        except Exception as e:
            # Por si ocurre cualquier otro error
            context = {'error': f'Error al crear la cuenta: {e}'}
            return render(request, 'account.html', context)


    # --- LÓGICA PARA MOSTRAR LA PÁGINA (CUANDO SE ENTRA POR PRIMERA VEZ) ---
    return render(request, 'account.html')