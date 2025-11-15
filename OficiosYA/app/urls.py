# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Vistas de página
    path('', views.inicio_sesion, name='inicio_sesion'),
    path('feed/', views.feed, name='feed'),
    path('registro/', views.registro, name='registro'), 

    # --- AÑADE ESTA LÍNEA ---
    path('publicar/', views.publicar, name='publicar'),
    # -------------------------
    
    # --- APIs NUEVAS ---
    path('api/login', views.api_login, name='api_login'),
    # ... (el resto de tus rutas)
]