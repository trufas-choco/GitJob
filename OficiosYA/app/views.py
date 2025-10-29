from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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

    #probando perfil))) pato
def mi_perfil(request):
     return render(request, 'perfil_pruebaa.html', {'u': request.user})