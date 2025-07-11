# bpm

Sistema de gestión veterinaria - Mascota Feliz

## Descripción

Este proyecto es una aplicación web desarrollada con Django para la gestión completa de citas, servicios y perfiles de mascotas en una veterinaria. Incluye un sistema completo de autenticación, CRUD para mascotas y citas, y una interfaz moderna y responsiva.

## Características principales

- **Sistema de Autenticación Completo**
  - Registro e inicio de sesión de usuarios
  - Gestión de perfiles de usuario
  - Protección de rutas con autenticación

- **Gestión de Mascotas**
  - Registro de mascotas con información detallada (nombre, especie, raza, sexo, peso, etc.)
  - Edición de información de mascotas
  - Historial médico por mascota

- **Sistema de Citas**
  - Agendamiento de citas para diferentes servicios veterinarios
  - Validación de horarios y disponibilidad
  - Gestión de estados de citas (programada, confirmada, completada, cancelada)
  - Cancelación de citas por parte del usuario

- **Catálogo de Servicios**
  - 12 servicios pre-configurados (consultas, cirugías, laboratorio, farmacia, peluquería, etc.)
  - Servicios organizados por categorías
  - Información detallada de precios y duración
  - Panel administrativo para gestión de servicios

- **Interfaz de Usuario**
  - Diseño responsivo con Bootstrap 5
  - Navegación intuitiva con estados de autenticación
  - Mensajes de feedback para todas las acciones
  - Formularios con validación tanto en frontend como backend

- **Panel Administrativo**
  - Gestión completa de usuarios, mascotas, citas y servicios
  - Filtros avanzados y búsqueda
  - Reportes y estadísticas

## Modelos de Datos

El sistema incluye 4 modelos principales:

1. **PerfilUsuario**: Extiende el modelo User de Django con información adicional
2. **Servicio**: Catálogo de servicios veterinarios con precios y categorías
3. **Mascota**: Información detallada de las mascotas de los usuarios
4. **Cita**: Sistema de agendamiento con validaciones y estados

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
   cd veterinaria
   python manage.py migrate
   ```

5. **Crea servicios básicos:**
   ```bash
   python manage.py crear_servicios
   ```

6. **Crea un superusuario (opcional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecuta el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

8. **Accede a la aplicación:**
   - [http://localhost:8000/](http://localhost:8000/) - Aplicación principal
   - [http://localhost:8000/admin/](http://localhost:8000/admin/) - Panel administrativo

## Rutas principales

- `/` — Página principal
- `/nosotros/` — Sobre la veterinaria y el equipo
- `/servicios/` — Listado de servicios veterinarios
- `/login/` — Inicio de sesión y registro
- `/perfil/` — Perfil del usuario y mascotas (requiere autenticación)
- `/agendar/` — Formulario para agendar citas (requiere autenticación)
- `/editar-perfil/` — Editar información personal
- `/agregar-mascota/` — Registrar nueva mascota
- `/editar-mascota/<id>/` — Editar información de mascota
- `/cancelar-cita/<id>/` — Cancelar cita programada

## Funcionalidades CRUD Implementadas

### Usuarios
- ✅ **Create**: Registro de nuevos usuarios con perfil completo
- ✅ **Read**: Visualización de perfil y datos personales
- ✅ **Update**: Edición de información personal
- ✅ **Delete**: A través del panel administrativo

### Mascotas
- ✅ **Create**: Registro de nuevas mascotas
- ✅ **Read**: Visualización de mascotas en perfil
- ✅ **Update**: Edición de información de mascotas
- ✅ **Delete**: Desactivación (soft delete)

### Citas
- ✅ **Create**: Agendamiento de nuevas citas
- ✅ **Read**: Visualización de citas próximas e historial
- ✅ **Update**: Cambio de estados y cancelación
- ✅ **Delete**: Cancelación de citas

### Servicios
- ✅ **Create**: A través del panel administrativo
- ✅ **Read**: Catálogo público de servicios
- ✅ **Update**: Gestión a través del admin
- ✅ **Delete**: Desactivación de servicios

## Validaciones Implementadas

- **Fechas de citas**: No se pueden agendar en el pasado
- **Horarios**: Solo entre 8:00 AM y 6:00 PM
- **Días**: No se atiende los domingos
- **Autenticación**: Rutas protegidas para usuarios autenticados
- **Permisos**: Los usuarios solo pueden ver/editar sus propias mascotas y citas

## Tecnologías Utilizadas

- **Backend**: Django 5.2+ (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Frameworks CSS**: Bootstrap 5.3
- **Base de datos**: SQLite (incluida con Django)
- **Fuentes**: Google Fonts (Poppins)
- **Iconos**: Bootstrap Icons

## Estructura del proyecto

- `app/` — Aplicación principal con vistas, modelos, forms y templates
- `static/` — Archivos estáticos (CSS, JS, imágenes)
- `templates/` — Archivos HTML de las vistas
- `management/commands/` — Comandos personalizados de Django

## Servicios Pre-configurados

Al ejecutar `python manage.py crear_servicios`, se crean automáticamente:

1. **Consulta General** - $45,000 (30 min)
2. **Vacunación** - $35,000 (15 min)
3. **Cirugía Menor** - $150,000 (60 min)
4. **Esterilización** - $200,000 (90 min)
5. **Exámenes de Laboratorio** - $80,000 (15 min)
6. **Radiografías** - $65,000 (20 min)
7. **Peluquería Completa** - $40,000 (60 min)
8. **Baño Medicado** - $50,000 (45 min)
9. **Hospitalización** - $120,000 (24 horas)
10. **Emergencia 24h** - $100,000 (45 min)
11. **Medicamentos** - $25,000 (10 min)
12. **Alimento Especializado** - $45,000 (5 min)

## Estado del Proyecto

✅ **COMPLETADO**: Sistema completamente funcional con:
- Modelos de datos implementados
- Sistema de autenticación completo
- CRUD completo para todos los modelos
- Validaciones de negocio
- Interfaz de usuario moderna
- Panel administrativo configurado
- Datos de prueba incluidos

## Próximas Mejoras

- 📧 Sistema de notificaciones por email
- 📱 API REST para aplicación móvil
- 📊 Dashboard con estadísticas y reportes
- 💳 Integración con pasarelas de pago
- 📄 Generación de PDF para historiales médicos
- 🔄 Sistema de recordatorios automáticos

---

Desarrollado por el equipo de Mascota Feliz.
**Usuario administrador por defecto**: admin / admin (cambiar en producción)
