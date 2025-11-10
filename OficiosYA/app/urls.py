# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('menu', views.menu_usuario, name='menu_usuario'),
    path('otro', views.otro_template, name='otro_template'),
    path('', views.inicio_sesion, name='inicio_sesion'),
     # cambia 'hola' por tu vista real si ya tienes otra.

    path('feed', views.feed, name='feed'),
    path('tipousuario', views.tipousuario, name='tipousuario'),
    path('perfilusuario', views.perfilusuario, name='perfilusuario'),
    path('feedfinal', views.feedfinal, name='feedfinal'),
    #pato (perfil)
    path('perfil', views.mi_perfil, name='mi_perfil'),
    path('generar-aviso', views.generar_aviso, name='publicar')
]
