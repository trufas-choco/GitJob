# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Vistas de página (Corregidas para usar las plantillas existentes)
    path('', views.inicio_sesion, name='inicio_sesion'),
    path('feed/', views.feed, name='feed'),
    
    # --- Vistas Comentadas (porque falta el HTML) ---
    # path('menu', views.menu_usuario, name='menu_usuario'),
    # path('otro/', views.otro_template, name='otro_template'),
    # path('perfil/', views.mi_perfil, name='mi_perfil'),
    
    # --- APIs NUEVAS (Requeridas por tu JS) ---
    # Esta es la URL que 'login.js' está buscando
    path('api/login', views.api_login, name='api_login'),
    # Esta es la URL que 'home.js' está buscando
    path('api/user/me', views.api_user_me, name='api_user_me'),
]