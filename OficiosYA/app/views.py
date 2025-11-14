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

# ... (al final del archivo, junto con las otras vistas)

def registro(request):
    """
    Esta vista se encarga de mostrar la página de registro (account.html)
    """
    return render(request, 'account.html')