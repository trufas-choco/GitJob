# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_usuario, name='menu_usuario'),
    path('otro/', views.otro_template, name='otro_template'),
     # cambia 'hola' por tu vista real si ya tienes otra
]
