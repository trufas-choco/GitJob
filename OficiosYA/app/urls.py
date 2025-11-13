# app/urls.py
from django.urls import path
from . import views
from app import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('inicio', views.inicio, name='inicio'),
    path('publicar', views.publicacion, name='publicar'),
    

]
