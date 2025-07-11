from django.core.management.base import BaseCommand
from app.models import Servicio

class Command(BaseCommand):
    help = 'Crea servicios básicos para la veterinaria'

    def handle(self, *args, **options):
        servicios_datos = [
            {
                'nombre': 'Consulta General',
                'descripcion': 'Examen médico general para evaluar el estado de salud de tu mascota',
                'categoria': 'consulta',
                'precio': 45000,
                'duracion_estimada': 30
            },
            {
                'nombre': 'Vacunación',
                'descripcion': 'Aplicación de vacunas según el calendario de vacunación',
                'categoria': 'consulta',
                'precio': 35000,
                'duracion_estimada': 15
            },
            {
                'nombre': 'Cirugía Menor',
                'descripcion': 'Procedimientos quirúrgicos menores ambulatorios',
                'categoria': 'cirugia',
                'precio': 150000,
                'duracion_estimada': 60
            },
            {
                'nombre': 'Esterilización',
                'descripcion': 'Cirugía de esterilización para perros y gatos',
                'categoria': 'cirugia',
                'precio': 200000,
                'duracion_estimada': 90
            },
            {
                'nombre': 'Exámenes de Laboratorio',
                'descripcion': 'Análisis clínicos, hemograma, química sanguínea',
                'categoria': 'laboratorio',
                'precio': 80000,
                'duracion_estimada': 15
            },
            {
                'nombre': 'Radiografías',
                'descripcion': 'Estudios radiológicos para diagnóstico',
                'categoria': 'laboratorio',
                'precio': 65000,
                'duracion_estimada': 20
            },
            {
                'nombre': 'Peluquería Completa',
                'descripcion': 'Baño, corte, limpieza de oídos y corte de uñas',
                'categoria': 'peluqueria',
                'precio': 40000,
                'duracion_estimada': 60
            },
            {
                'nombre': 'Baño Medicado',
                'descripcion': 'Baño con productos especiales para problemas dermatológicos',
                'categoria': 'peluqueria',
                'precio': 50000,
                'duracion_estimada': 45
            },
            {
                'nombre': 'Hospitalización',
                'descripcion': 'Cuidado y monitoreo durante recuperación',
                'categoria': 'hospitalizacion',
                'precio': 120000,
                'duracion_estimada': 1440  # 24 horas
            },
            {
                'nombre': 'Emergencia 24h',
                'descripcion': 'Atención de urgencias veterinarias',
                'categoria': 'emergencia',
                'precio': 100000,
                'duracion_estimada': 45
            },
            {
                'nombre': 'Medicamentos',
                'descripcion': 'Venta de medicamentos veterinarios',
                'categoria': 'farmacia',
                'precio': 25000,
                'duracion_estimada': 10
            },
            {
                'nombre': 'Alimento Especializado',
                'descripcion': 'Alimentos terapéuticos y de alta calidad',
                'categoria': 'farmacia',
                'precio': 45000,
                'duracion_estimada': 5
            }
        ]

        for servicio_data in servicios_datos:
            servicio, created = Servicio.objects.get_or_create(
                nombre=servicio_data['nombre'],
                defaults=servicio_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Servicio "{servicio.nombre}" creado exitosamente')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Servicio "{servicio.nombre}" ya existe')
                )

        self.stdout.write(
            self.style.SUCCESS('¡Servicios básicos creados exitosamente!')
        )
