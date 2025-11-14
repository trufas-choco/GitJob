from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    usuario= models.ForeignKey(User, on_delete=models.CASCADE)
    nombre= models.CharField(max_length=50)
    precio= models.DecimalField(max_digits=10,decimal_places=2)
    imagen= models.ImageField(upload_to='productos/', blank=True, null=True)
    descripcion= models.TextField(blank=True)
    fecha_publi= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"




