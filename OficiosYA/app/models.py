from django.db import models
from django.contrib.auth.models import User

class Publicacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='publicaciones/') 
    # --- AÑADE ESTAS DOS LÍNEAS ---
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    # ---------------------------------
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Publicación de {self.usuario.username}"