# catalog/models.py
from django.db import models
from django.contrib.auth.models import User

class Tienda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tiendas', null=True, blank=True)
    nombre = models.CharField(max_length=100) 
    color_hex = models.CharField(max_length=7, default="#0a8f34")

    class Meta:
        unique_together = ('usuario', 'nombre')

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().capitalize()
        super().save(*args, **kwargs)

class MaestroProducto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos_maestros', null=True, blank=True)
    nombre = models.CharField(max_length=200)
    tienda_habitual = models.ForeignKey(Tienda, on_delete=models.SET_NULL, null=True, blank=True)
    frecuencia_uso = models.PositiveIntegerField(default=0)
    zona = models.CharField(max_length=100, default="General")

    class Meta:
        unique_together = ('usuario', 'nombre')

    def __str__(self):
        return f"{self.nombre} ({self.zona})"