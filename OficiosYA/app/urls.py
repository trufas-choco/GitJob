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

    path('perfil/', views.perfil, name='perfil'),

    # -------------------------
    path('publicacion/<int:pk>/', views.publicacion_detalle, name='publicacion_detalle'),
    # --- APIs NUEVAS ---
    path('api/login', views.api_login, name='api_login'),
    path('api/publicaciones_cercanas/', views.api_publicaciones_cercanas, name='api_publicaciones_cercanas'),
    # ... (el resto de tus rutas)
]
