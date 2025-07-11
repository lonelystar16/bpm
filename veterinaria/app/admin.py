from django.contrib import admin
from .models import Servicio, PerfilUsuario, Mascota, Cita

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'duracion_estimada', 'activo']
    list_filter = ['categoria', 'activo', 'created_at']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'activo']
    ordering = ['categoria', 'nombre']

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefono', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'telefono']
    readonly_fields = ['created_at']

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'especie', 'raza', 'propietario', 'activa', 'created_at']
    list_filter = ['especie', 'sexo', 'activa', 'created_at']
    search_fields = ['nombre', 'raza', 'propietario__username', 'propietario__first_name', 'propietario__last_name']
    list_editable = ['activa']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('propietario')

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['mascota', 'servicio', 'fecha_hora', 'estado', 'prioridad', 'propietario']
    list_filter = ['estado', 'prioridad', 'servicio__categoria', 'fecha_hora', 'created_at']
    search_fields = ['mascota__nombre', 'propietario__username', 'propietario__first_name', 'propietario__last_name']
    list_editable = ['estado', 'prioridad']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'fecha_hora'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('mascota', 'servicio', 'propietario')
    
    def propietario(self, obj):
        return obj.propietario.get_full_name() or obj.propietario.username
    propietario.short_description = 'Propietario'
