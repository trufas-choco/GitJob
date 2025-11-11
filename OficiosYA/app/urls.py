# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('inicio', views.inicio, name='incio'),
    path('publicar', views.publicacion, name='publicar'),
    

]
