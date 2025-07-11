from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('agendar/', views.agendar, name='agendar'),
    path('nosotros/', views.nosotros, name='nosotros'),
    
    # URLs para gestión de perfil y mascotas
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('agregar-mascota/', views.agregar_mascota, name='agregar_mascota'),
    path('editar-mascota/<int:mascota_id>/', views.editar_mascota, name='editar_mascota'),
    path('cancelar-cita/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    
    # API endpoints
    path('api/disponibilidad-citas/', views.api_disponibilidad_citas, name='api_disponibilidad_citas'),
]