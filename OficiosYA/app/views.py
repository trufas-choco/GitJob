from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def menu_usuario(request):
    return render(request, 'menu_usuario.html')
def otro_template(request):
    return render(request, 'otro_template.html')
def inicio_sesion(request):
    return render(request, 'inicio_sesion.html')
