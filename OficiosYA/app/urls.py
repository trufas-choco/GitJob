# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('menu', views.menu_usuario, name='menu_usuario'),
    path('otro/', views.otro_template, name='otro_template'),
    path('', views.inicio_sesion, name='inicio_sesion'),
     # cambia 'hola' por tu vista real si ya tienes otra


    #pato (perfil)
    path('perfil/', views.mi_perfil, name='mi_perfil'),
]
