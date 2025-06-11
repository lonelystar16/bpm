from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', views.login, name='login'),
    path('agendar/', views.agendar, name='agendar'),
]