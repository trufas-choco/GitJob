# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hola, name='home'),   # cambia 'hola' por tu vista real si ya tienes otra
]
