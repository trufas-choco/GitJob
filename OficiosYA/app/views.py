from django.shortcuts import render, redirect 
from .models import Producto
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests

def login(request):
    return render(request, 'index.html')
def signup(request):
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
