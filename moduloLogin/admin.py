from django import forms
from django.contrib import admin

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Empleado, Mozo, Cajero, Auditor, Supervisor, Seguridad, Bartender, Administrador, Turno, Contratacion

class MyAdminSite(AdminSite):
    site_header = "Panel de Administración de ROXO"
    site_title = "Admin ROXO"
    index_title = "Bienvenido al Panel de Control"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(User, UserAdmin)
        self.register(Group, GroupAdmin)

admin_site = MyAdminSite(name='myadmin')

class EmpleadoAdminForm(forms.ModelForm):
    email = forms.EmailField(label='Correo Electrónico', required=True)
    _annos_experiencia = forms.DecimalField(label="Años de experiencia", required=True)

    class Meta:
        model = Empleado
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Cargar el email actual del usuario relacionado
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        # Guardar el email en el objeto User relacionado
        user = self.instance.user
        user.email = self.cleaned_data['email']
        user.save()
        return super().save(commit=commit)

@admin.register(Mozo, site=admin_site)
class MozoAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'zona_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'zona_asignada')

@admin.register(Cajero, site=admin_site)
class CajeroAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'caja_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'caja_asignada')

@admin.register(Auditor, site=admin_site)
class AuditorAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'frecuencia', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username',)

@admin.register(Supervisor, site=admin_site)
class SupervisorAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'frecuencia', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username',)

@admin.register(Seguridad, site=admin_site)
class SeguridadAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'entrada_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'entrada_asignada')

@admin.register(Bartender, site=admin_site)
class BartenderAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'barra_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'barra_asignada')

@admin.register(Administrador, site=admin_site)
class AdministradorAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'nombre', 'apellido', 'cantidad_empleados_contratados')
    search_fields = ('user__username',)

    def cantidad_empleados_contratados(self, obj):
        # Calcula la cantidad de empleados contratados para el administrador actual
        return obj.cantidad_empleados_contratados

    cantidad_empleados_contratados.short_description = 'Empleados contratados'  # Nombre de la columna en la lista

@admin.register(Turno, site=admin_site)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('hora_inicio', 'hora_fin')

@admin.register(Contratacion, site=admin_site)
class ContratacionAdmin(admin.ModelAdmin):
    list_display = ('administrador', 'empleado', 'fecha_contratacion')
    search_fields = ('administrador__user__username', 'empleado__user__username')
