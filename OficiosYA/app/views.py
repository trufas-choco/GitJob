from django.shortcuts import render, redirect 
from .models import Producto
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import requests

def login_view(request):
    if request.method == 'POST':
        username_from_form = request.POST.get('username')
        password_from_form = request.POST.get('password')
        user = authenticate(request, username=username_from_form, password=password_from_form)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            context = {'error': 'Nombre de usuario o contraseña incorrectos.'}
            return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')        


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('new-password')
        pass2 = request.POST.get('confirm-password')
        
        if pass1 != pass2:
            context = {'error': 'Las contraseñas no coinciden.'}
            return render(request, 'signup.html', context)
        if User.objects.filter(username=username).exists():
            context = {'error': 'Ese nombre de usuario ya está en uso.'}
            return render(request, 'signup.html', context)
        try:
            user = User.objects.create_user(username=username, password=pass1)
            user.save()
            login(request, user)
            return redirect('inicio')

        except Exception as e:
            context = {'error': f'Ha ocurrido un error: {e}'}
            return render(request, 'signup.html', context)
    else:
        return render(request, 'signup.html')
  
def reset(request):
    return render(request, 'reset.html')
def inicio(request):
    return render(request, 'home.html')
def publicar(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        imagen = request.FILES.get('imagen')  
        mensaje_exito = "¡Tu producto se ha subido con éxito!"
        producto = Producto.objects.create(
            usuario=request.user,
            nombre=nombre,
            descripcion=descripcion,
            imagen=imagen
        )
        return redirect('home.html')
    return render(request, 'publicar.html')




@csrf_exempt
def publicacion(request):
    aviso = None
    error = None
    descripcion_inicial = ""

    if request.method == "POST":
        descripcion_inicial = request.POST.get("descripcion", "").strip()
        if not descripcion_inicial:
            error = "Por favor, ingresa una descripción."
        else:
            try:
                # Llamada a la API local de Ollama
                r = requests.post(
                    "http://127.0.0.1:11434/api/generate", #o poner chat
                    json={
                        "model": "llama3.2:3b",  # liviano y rápido
                        "messages": [
                            {
                                "role": "system",
                                "content": "Eres un asistente que redacta avisos de trabajo o servicios "
                                           "para personas que ofrecen algo. Tu tarea es crear publicaciones claras, "
                                           "atractivas y confiables para que los potenciales clientes o trabajadores "
                                           "entiendan qué se ofrece. Escribe en español de Chile, con tono cercano y profesional."
                                        
                            },
                            {
                                "role": "user",
                                "content":  "Genera un aviso atractivo y claro en base a esta descripción del servicio o trabajo que se ofrece:\n\n"
                                            f"{descripcion_inicial}\n\n"
                                            "Incluye las siguientes secciones:\n"
                                            "TÍTULO:\n"
                                            "DESCRIPCIÓN:\n"
                                            "REQUISITOS (si aplica):\n"
                                            "BENEFICIOS o CONDICIONES:\n"
                                            "CONTACTO:"
                            }
                        ],
                        "stream": False,
                        "options": {"temperature": 0.4, "num_ctx": 2048}
                    },
                    timeout=60,
                )
                r.raise_for_status()
                data = r.json()
                aviso = data.get("message", {}).get("content", "").strip()
            except Exception as e:
                error = f"No pude generar el aviso: {e}"

    return render(request, "publicar.html", {
        "aviso": aviso,
        "error": error,
        "descripcion": descripcion_inicial
    })
