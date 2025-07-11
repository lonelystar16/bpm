from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Mascota, Cita, Servicio
from django.utils import timezone
from datetime import datetime, timedelta

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nombres")
    last_name = forms.CharField(max_length=30, required=True, label="Apellidos")
    telefono = forms.CharField(max_length=15, required=True)
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de Nacimiento"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar labels y widgets
        self.fields['username'].label = "Nombre de usuario"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        
        # Añadir clases CSS
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Crear perfil de usuario
            PerfilUsuario.objects.create(
                user=user,
                telefono=self.cleaned_data['telefono'],
                direccion=self.cleaned_data['direccion'],
                fecha_nacimiento=self.cleaned_data.get('fecha_nacimiento')
            )
        return user

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'sexo', 'fecha_nacimiento', 'peso', 'color', 'observaciones']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
            'peso': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir clases CSS
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['mascota', 'servicio', 'fecha_hora', 'prioridad', 'motivo']
        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'motivo': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'mascota': forms.Select(attrs={'class': 'form-select'}),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filtrar mascotas solo del usuario actual
            self.fields['mascota'].queryset = Mascota.objects.filter(
                propietario=user, activa=True
            )
        
        # Filtrar servicios activos
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True)

    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data['fecha_hora']
        
        # Validar que la fecha no sea en el pasado
        if fecha_hora < timezone.now():
            raise forms.ValidationError("No puedes agendar una cita en el pasado.")
        
        # Validar horario de atención (ejemplo: 8:00 AM a 6:00 PM)
        hora = fecha_hora.time()
        if hora < datetime.strptime('08:00', '%H:%M').time() or hora > datetime.strptime('18:00', '%H:%M').time():
            raise forms.ValidationError("Las citas solo se pueden agendar entre 8:00 AM y 6:00 PM.")
        
        # Validar que no sea domingo
        if fecha_hora.weekday() == 6:  # 6 = domingo
            raise forms.ValidationError("No atendemos los domingos.")
        
        return fecha_hora

class EditarPerfilForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nombres")
    last_name = forms.CharField(max_length=30, required=True, label="Apellidos")
    email = forms.EmailField(required=True)

    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'direccion', 'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        
        # Añadir clases CSS
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        perfil = super().save(commit=False)
        if commit:
            # Actualizar datos del usuario
            user = perfil.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            perfil.save()
        return perfil
