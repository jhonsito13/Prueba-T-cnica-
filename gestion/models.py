from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('BASE', 'Usuario Base'),
    ]
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='BASE')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
class Acta(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADA', 'Completada'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha = models.DateTimeField(auto_now_add=True)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='actas_creadas')
    participantes = models.ManyToManyField(Usuario, related_name='actas_participante')
    archivo_pdf = models.FileField(upload_to='actas/', null=True, blank=True)
    
    def __str__(self):
        return self.titulo

class Compromiso(models.Model):
    acta = models.ForeignKey(Acta, on_delete=models.CASCADE, related_name='compromisos')
    descripcion = models.TextField()
    fecha_limite = models.DateField()
    responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, default='PENDIENTE')
    
    def __str__(self):
        return f"{self.descripcion[:50]}..."

class Gestion(models.Model):
    compromiso = models.ForeignKey(Compromiso, on_delete=models.CASCADE, related_name='gestiones')
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    archivo_adjunto = models.FileField(upload_to='gestiones/', null=True, blank=True)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Gestión - {self.fecha}" 

