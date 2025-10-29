from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests

def menu_usuario(request):
    return render(request, 'menu_usuario.html')
def otro_template(request):
    return render(request, 'otro_template.html')
def inicio_sesion(request):
    return render(request, 'inicio_sesion.html')
    
def feed(request):
    return render(request, 'prueba_feed.html')
def tipousuario(request):
    return render(request, 'tipousuario.html')
def perfilusuario(request):
    return render(request, 'perfilusuario.html')
def feedfinal(request):
    return render(request, 'feedfinal.html')

    #probando perfil))) pato
def mi_perfil(request):
     return render(request, 'perfil_pruebaa.html', {'u': request.user})




@csrf_exempt
def generar_aviso(request):
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
                    "http://127.0.0.1:11434/api/chat",
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

    return render(request, "generar_avisos.html", {
        "aviso": aviso,
        "error": error,
        "descripcion": descripcion_inicial
    })
