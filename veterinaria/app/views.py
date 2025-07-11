from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import Servicio, PerfilUsuario, Mascota, Cita
from .forms import RegistroUsuarioForm, MascotaForm, CitaForm, EditarPerfilForm

def index(request):
    # Obtener algunos servicios destacados para mostrar
    servicios_destacados = Servicio.objects.filter(activo=True)[:6]
    context = {
        'servicios_destacados': servicios_destacados
    }
    return render(request, 'index.html', context)

def servicios(request):
    # Obtener todos los servicios activos agrupados por categoría
    servicios_list = Servicio.objects.filter(activo=True).order_by('categoria', 'nombre')
    
    # Agrupar servicios por categoría
    servicios_por_categoria = {}
    for servicio in servicios_list:
        categoria = servicio.get_categoria_display()
        if categoria not in servicios_por_categoria:
            servicios_por_categoria[categoria] = []
        servicios_por_categoria[categoria].append(servicio)
    
    context = {
        'servicios_por_categoria': servicios_por_categoria
    }
    return render(request, 'servicios.html', context)

@login_required
def perfil(request):
    # Obtener o crear perfil de usuario
    perfil_usuario, created = PerfilUsuario.objects.get_or_create(user=request.user)
    
    # Obtener mascotas del usuario
    mascotas = Mascota.objects.filter(propietario=request.user, activa=True)
    
    # Obtener citas próximas
    citas_proximas = Cita.objects.filter(
        propietario=request.user,
        fecha_hora__gte=timezone.now(),
        estado__in=['programada', 'confirmada']
    ).order_by('fecha_hora')[:5]
    
    # Obtener historial de citas
    historial_citas = Cita.objects.filter(
        propietario=request.user
    ).order_by('-fecha_hora')[:10]
    
    context = {
        'perfil_usuario': perfil_usuario,
        'mascotas': mascotas,
        'citas_proximas': citas_proximas,
        'historial_citas': historial_citas
    }
    return render(request, 'perfil.html', context)

def login_view(request):
    # Si el usuario ya está autenticado, redirigir al perfil
    if request.user.is_authenticated:
        return redirect('perfil')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.get_full_name() or user.username}!')
                # Obtener next parameter o ir a perfil por defecto
                next_url = request.GET.get('next', 'perfil')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        
        elif action == 'register':
            form = RegistroUsuarioForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, '¡Registro exitoso! Ya puedes iniciar sesión.')
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
    
    return render(request, 'login.html')

def logout_view(request):
    """Vista personalizada para logout que acepta GET y POST"""
    if request.user.is_authenticated:
        username = request.user.get_full_name() or request.user.username
        logout(request)
        messages.success(request, f'¡Hasta luego, {username}! Has cerrado sesión exitosamente.')
    return redirect('index')

@login_required
def agendar(request):
    if request.method == 'POST':
        form = CitaForm(user=request.user, data=request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.propietario = request.user
            cita.save()
            messages.success(request, '¡Cita agendada exitosamente!')
            return redirect('perfil')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CitaForm(user=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'agendar.html', context)

def nosotros(request):
    return render(request, 'nosotros.html')

@login_required
def editar_perfil(request):
    perfil_usuario, created = PerfilUsuario.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=perfil_usuario)
    
    context = {
        'form': form
    }
    return render(request, 'editar_perfil.html', context)

@login_required
def agregar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.propietario = request.user
            mascota.save()
            messages.success(request, f'¡Mascota {mascota.nombre} agregada exitosamente!')
            return redirect('perfil')
    else:
        form = MascotaForm()
    
    context = {
        'form': form
    }
    return render(request, 'agregar_mascota.html', context)

@login_required
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id, propietario=request.user)
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, f'Información de {mascota.nombre} actualizada exitosamente.')
            return redirect('perfil')
    else:
        form = MascotaForm(instance=mascota)
    
    context = {
        'form': form,
        'mascota': mascota
    }
    return render(request, 'editar_mascota.html', context)

@login_required
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, propietario=request.user)
    
    if cita.fecha_hora > timezone.now() and cita.estado in ['programada', 'confirmada']:
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada exitosamente.')
    else:
        messages.error(request, 'No se puede cancelar esta cita.')
    
    return redirect('perfil')

# API endpoints para mejorar la experiencia del usuario
@login_required
def api_disponibilidad_citas(request):
    """API para verificar disponibilidad de citas en una fecha específica"""
    fecha = request.GET.get('fecha')
    if not fecha:
        return JsonResponse({'error': 'Fecha requerida'}, status=400)
    
    try:
        from datetime import datetime
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        # Obtener citas ocupadas para esa fecha
        citas_ocupadas = Cita.objects.filter(
            fecha_hora__date=fecha_obj,
            estado__in=['programada', 'confirmada', 'en_proceso']
        ).values_list('fecha_hora__time', flat=True)
        
        # Generar horarios disponibles (ejemplo: cada 30 minutos de 8:00 a 18:00)
        horarios_disponibles = []
        from datetime import time, timedelta
        
        hora_inicio = time(8, 0)  # 8:00 AM
        hora_fin = time(18, 0)    # 6:00 PM
        
        current_time = datetime.combine(fecha_obj, hora_inicio)
        end_time = datetime.combine(fecha_obj, hora_fin)
        
        while current_time <= end_time:
            if current_time.time() not in citas_ocupadas:
                horarios_disponibles.append(current_time.strftime('%H:%M'))
            current_time += timedelta(minutes=30)
        
        return JsonResponse({
            'horarios_disponibles': horarios_disponibles
        })
        
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)