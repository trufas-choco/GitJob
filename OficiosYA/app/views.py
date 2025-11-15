from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim
from .models import Publicacion
import json
import math
import requests

# --- Vistas de Plantillas ---

@login_required 
def feed(request):
    # 1. Obtenemos todas las publicaciones de la base de datos
    publicaciones = Publicacion.objects.all().order_by('-created_at')

    # 2. Las pasamos al contexto del template
    context = {
        'publicaciones': publicaciones
    }
    return render(request, 'feed.html', context)

def inicio_sesion(request):
    # Apunta a 'login.html'
    return render(request, 'login.html')

@login_required 
def publicar(request):
    """
    GET  -> muestra la página
    POST -> según el botón:
            - 'generate_ia': genera texto con IA y solo recarga el formulario
            - sin 'generate_ia': intenta guardar la publicación
    """
    descripcion_context = ""
    error = None

    if request.method == 'POST':

        # ==============================
        # 1) BOTÓN: "Generar Con IA"
        # ==============================
        if 'generate_ia' in request.POST:
            descripcion_inicial = request.POST.get('descripcion', '').strip()
            precio_raw = request.POST.get('precio', '').strip() 
            print(">>> [IA] POST:", request.POST)  # para ver en consola
            print(">>> [IA] descripcion entrada:", descripcion_inicial)

            if not descripcion_inicial:
                return render(request, 'publicar.html', {
                    'descripcion': '',
                    'error': 'Escriba una descripción breve antes de usar la IA.',
                })

            try:
                r = requests.post(
                    "http://localhost:11434/api/chat",
                    json={ "model": "llama3.2:3b", "messages": [ 
                        { "role": "system", "content": 
                         ( "Eres un asistente experto en redacción de avisos laborales y de servicios para Chile. Tu estilo es claro, profesional, cercano y persuasivo, evitando textos genéricos o exagerados." ) }, 
                         { "role": "user", "content": ( "Genera un aviso atractivo y claro en base a esta descripción:\n\n" f"{descripcion_inicial}\n\n" "Incluye:\n" 
                                                       "TÍTULO:\n" "DESCRIPCIÓN:\n" ) } ],
                                                        "stream": False, "options": {"temperature": 0.4, "num_ctx": 500} },
                    timeout=60
                )
                print("Status:", r.status_code)

                data = r.json()
                descripcion_generada = data["message"]["content"].strip()
                descripcion_context = descripcion_generada
                print(">>> [IA] descripcion salida:", descripcion_context)
                

            except Exception as e:
                print(f"Error con Ollama: {e}")
                error = "No se pudo conectar con la IA. Verifique que Ollama esté corriendo."
                descripcion_context = descripcion_inicial

            # IMPORTANTE: aquí SOLO recargamos el formulario, NO guardamos nada
            return render(request, 'publicar.html', {
                'descripcion': descripcion_context,
                'precio': precio_raw,
                'error': error,
               
            })

        # ==============================
        # 2) BOTÓN: "Aceptar" (publicar)
        # ==============================
        try:
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
            imagenes = request.FILES.getlist('imagen')
            lat_val = request.POST.get('latitude')
            lon_val = request.POST.get('longitude')

            primera_imagen = imagenes[0] if imagenes else None

            if not primera_imagen:
                context = {
                    'error': 'Debes subir al menos una imagen.',
                    'descripcion': descripcion or ''
                }
                return render(request, 'publicar.html', context)

            # ----- GEOCODING -----
            region_nombre = None
            if lat_val and lon_val:
                try:
                    geolocator = Nominatim(user_agent="oficiosya_app")
                    location = geolocator.reverse((lat_val, lon_val), language='es')

                    if location and 'state' in location.raw['address']:
                        region_nombre = location.raw['address']['state']
                except Exception as e:
                    print(f"Error de Geocoding: {e}")
            # ----------------------

            Publicacion.objects.create(
                usuario=request.user,
                descripcion=descripcion,
                precio=precio,
                imagen=primera_imagen,
                latitude=float(lat_val) if lat_val else None,
                longitude=float(lon_val) if lon_val else None,
                region=region_nombre
            )

            return redirect('feed')

        except Exception as e:
            context = {
                'error': f'Error al publicar: {e}',
                'descripcion': request.POST.get('descripcion', '')
            }
            return render(request, 'publicar.html', context)

    # GET: página vacía
    return render(request, 'publicar.html', {
        'descripcion': '',
        'error': None,
    })


def registro(request):
    """
    Maneja la creación de nuevas cuentas (Registro).
    """
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        password = request.POST.get('new-password')
        username = phone # Usamos el teléfono como username

        if User.objects.filter(username=username).exists():
            context = {'error': 'El número de teléfono ya está registrado.'}
            return render(request, 'account.html', context)

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return redirect('feed')
        except Exception as e:
            context = {'error': f'Error al crear la cuenta: {e}'}
            return render(request, 'account.html', context)

    return render(request, 'account.html')

@login_required
def publicacion_detalle(request, pk):
    """
    Muestra la página de detalle para una publicación específica (por su ID/pk).
    """
    publicacion = get_object_or_404(Publicacion, pk=pk)
    context = {
        'publicacion': publicacion
    }
    return render(request, 'publicacion_detalle.html', context)

# ... (justo después de publicacion_detalle) ...

@login_required
def perfil(request):
    """
    Muestra la página de perfil del usuario que ha iniciado sesión.
    """
    # 1. Obtenemos solo las publicaciones creadas por el usuario actual
    publicaciones_propias = Publicacion.objects.filter(usuario=request.user).order_by('-created_at')
    
    context = {
        # Pasamos el usuario (para el nombre) y sus publicaciones
        'usuario': request.user,
        'publicaciones': publicaciones_propias
    }
    
    # 3. Renderiza la plantilla 'perfil.html'
    return render(request, 'perfil.html', context)


# --- Vistas de API ---

@csrf_exempt 
def api_login(request):
    """
    Maneja el inicio de sesión que viene desde 'login.js'.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get('phone')
            password = data.get('password')
            user = authenticate(request, username=phone, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'redirectUrl': '/feed/'})
            else:
                return JsonResponse({'error': 'Teléfono o contraseña incorrectos'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def api_user_me(request):
    """
    Devuelve los datos del usuario actual para 'home.js'.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)

    return JsonResponse({
        'first_name': request.user.first_name,
        'username': request.user.username
    })

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en km entre dos puntos (lat, lon) en la Tierra.
    """
    R = 6371  # Radio de la Tierra en km
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

@login_required
def api_publicaciones_cercanas(request):
    """
    Devuelve una lista de publicaciones cercanas a la ubicación del usuario (para 'home.js').
    """
    try:
        user_lat = float(request.GET.get('lat'))
        user_lon = float(request.GET.get('lon'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Ubicación no proporcionada'}, status=400)

    DISTANCIA_LIMITE = 10  # Límite en KM

    publicaciones_cercanas = []
    publicaciones = Publicacion.objects.exclude(usuario=request.user).exclude(latitude__isnull=True)

    for pub in publicaciones:
        distancia = haversine(user_lat, user_lon, pub.latitude, pub.longitude)
        
        if distancia <= DISTANCIA_LIMITE:
            publicaciones_cercanas.append({
                'id': pub.id,
                'descripcion': pub.descripcion,
                'precio': pub.precio,
                'imagen_url': pub.imagen.url,
                'vendedor_nombre': pub.usuario.first_name,
                'distancia_km': round(distancia, 1)
            })

    return JsonResponse({'publicaciones': publicaciones_cercanas})