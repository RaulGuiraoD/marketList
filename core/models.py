# core/models.py
from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'Prefiero no decirlo'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=100, blank=True)
    apellidos = models.CharField(max_length=100, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='N')
    presupuesto_mensual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    avatar_icon = models.CharField(max_length=20, default="👤")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"