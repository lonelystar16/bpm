from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Servicio(models.Model):
    CATEGORIA_CHOICES = [
        ('consulta', 'Consulta General'),
        ('cirugia', 'Cirugía'),
        ('laboratorio', 'Laboratorio'),
        ('farmacia', 'Farmacia'),
        ('peluqueria', 'Peluquería'),
        ('hospitalizacion', 'Hospitalización'),
        ('emergencia', 'Emergencia'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.IntegerField(help_text="Duración en minutos")
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Servicios"
        ordering = ['categoria', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    fecha_nacimiento = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"

class Mascota(models.Model):
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]
    
    ESPECIE_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('ave', 'Ave'),
        ('otro', 'Otro'),
    ]
    
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=50)
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES)
    raza = models.CharField(max_length=50, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Peso en kg")
    color = models.CharField(max_length=30, blank=True)
    observaciones = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.especie}) - {self.propietario.get_full_name() or self.propietario.username}"

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_asistio', 'No Asistió'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas')
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='programada')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='normal')
    motivo = models.TextField(help_text="Motivo de la consulta")
    observaciones = models.TextField(blank=True)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_hora']
        verbose_name_plural = "Citas"
    
    def __str__(self):
        return f"Cita: {self.mascota.nombre} - {self.servicio.nombre} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"
    
    def is_upcoming(self):
        return self.fecha_hora > timezone.now() and self.estado in ['programada', 'confirmada']
