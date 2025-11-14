# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Vistas de página
    path('', views.inicio_sesion, name='inicio_sesion'),
    path('feed/', views.feed, name='feed'),

    # --- AÑADIR ESTA LÍNEA ---
    path('registro/', views.registro, name='registro'), 
    # -------------------------
    
    # --- APIs NUEVAS ---
    path('api/login', views.api_login, name='api_login'),
    path('api/user/me', views.api_user_me, name='api_user_me'),

    # --- Vistas Comentadas (porque falta el HTML) ---
    # path('menu', views.menu_usuario, name='menu_usuario'),
    # path('otro/', views.otro_template, name='otro_template'),
    # path('perfil/', views.mi_perfil, name='mi_perfil'),
]