from django.db import models
from django.contrib.auth.models import AbstractUser

class Roll(models.Model):
    nombre = models.CharField(max_length=30)
    # Permisos
    gestionar_usuarios = models.BooleanField(default=False)
    gestionar_roles = models.BooleanField(default=False)
    gestionar_cuotas = models.BooleanField(default=False)
    gestionar_actas = models.BooleanField(default=False)
    gestionar_reportes = models.BooleanField(default=False)
    gestionar_noticias = models.BooleanField(default=False)

class Usuario(AbstractUser):
    solapin = models.CharField(max_length=7,unique=True)
    roll = models.ForeignKey(Roll, on_delete=models.CASCADE, related_name='usuarios',null=True)
    salario = models.PositiveIntegerField(default=0)
    
    def cuota(self):
        return self.salario*0.10