# bpm

Sistema de gestión veterinaria - Mascota Feliz

## Descripción

Este proyecto es una aplicación web desarrollada con Django para la gestión de citas, servicios y perfiles de mascotas en una veterinaria. Incluye funcionalidades como agendamiento de citas, registro de usuarios, perfil de mascotas y visualización de servicios.

## Características principales

- Registro e inicio de sesión de usuarios
- Agendamiento de citas para diferentes servicios veterinarios
- Gestión de perfil de usuario y mascotas
- Listado de servicios y farmacia
- Interfaz moderna y responsiva con Bootstrap
- Uso de archivos estáticos con la sintaxis de Django (`{% static %}`)
- Navegación entre vistas usando `{% url %}`
- Sección "Nosotros" con historia desde 1990 y equipo ampliado
- Formularios interactivos con validación y almacenamiento local (localStorage)
- Modal de confirmación para agendar citas

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tuusuario/bpm.git
   cd bpm
   ```

2. **Crea y activa un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realiza las migraciones:**
   ```bash
   python manage.py migrate
   ```

5. **Ejecuta el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

6. **Accede a la aplicación:**
   - [http://localhost:8000/](http://localhost:8000/)

## Rutas principales

- `/` — Página principal
- `/nosotros/` — Sobre la veterinaria y el equipo
- `/servicios/` — Listado de servicios veterinarios
- `/perfil/` — Perfil del usuario y mascotas
- `/login/` — Inicio de sesión y registro
- `/agendar/` — Formulario para agendar citas

## Estructura del proyecto

- `app/` — Aplicación principal con vistas y templates
- `static/` — Archivos estáticos (CSS, JS, imágenes)
- `templates/` — Archivos HTML de las vistas

## Notas

- Todos los archivos estáticos (CSS, JS, imágenes) se referencian usando la etiqueta `{% static %}` de Django.
- Las rutas internas usan la etiqueta `{% url %}` para una navegación robusta.
- La sección "Nosotros" ahora refleja el inicio de la veterinaria en 1990, el crecimiento y el equipo actualizado.
- Los formularios de autenticación y agendamiento usan validación en el frontend y almacenamiento en localStorage para demostración.
- Puedes personalizar los templates y estilos en la carpeta `static/css/styles.css`.

---

Desarrollado por el equipo de Mascota Feliz.