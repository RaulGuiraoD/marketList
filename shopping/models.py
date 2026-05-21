# shopping/models.py
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Tienda, MaestroProducto # <- Importaciones clave

class ListaCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listas', null=True, blank=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    esta_finalizada = models.BooleanField(default=False)
    fecha_finalizada = models.DateTimeField(null=True, blank=True)
    total_ticket = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Lista {self.tienda.nombre} - {self.fecha_creacion.strftime('%d/%m/%Y')}"

class ItemLista(models.Model):
    lista = models.ForeignKey(ListaCompra, related_name='items', on_delete=models.CASCADE)
    producto_maestro = models.ForeignKey(MaestroProducto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    comprado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto_maestro.nombre} en {self.lista}"