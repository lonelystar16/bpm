from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def servicios(request):
    return render(request, 'servicios.html')

def perfil(request):
    return render(request, 'perfil.html')

def login(request):
    return render(request, 'login.html')

def agendar(request):
    return render(request, 'agendar.html')

def nosotros(request):
    return render(request, 'nosotros.html')