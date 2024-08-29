"""
from django.contrib import admin
from .models import Mozo, Cajero, Auditor, Supervisor, Seguridad, Bartender, Administrador, Turno, Contratacion

@admin.register(Mozo)
class MozoAdmin(admin.ModelAdmin):
    list_display = ('user', 'zona_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'zona_asignada')

@admin.register(Cajero)
class CajeroAdmin(admin.ModelAdmin):
    list_display = ('user', 'caja_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'caja_asignada')

@admin.register(Auditor)
class AuditorAdmin(admin.ModelAdmin):
    list_display = ('user', 'frecuencia', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username',)

@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('user', 'frecuencia', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username',)

@admin.register(Seguridad)
class SeguridadAdmin(admin.ModelAdmin):
    list_display = ('user', 'entrada_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'entrada_asignada')

@admin.register(Bartender)
class BartenderAdmin(admin.ModelAdmin):
    list_display = ('user', 'barra_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'barra_asignada')

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('user', 'cantidad_empleados_contratados', 'cantidad_fiestas_organizadas')
    search_fields = ('user__username',)

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('hora_inicio', 'hora_fin')

@admin.register(Contratacion)
class ContratacionAdmin(admin.ModelAdmin):
    list_display = ('administrador', 'empleado', 'fecha_contratacion')
    search_fields = ('administrador__user__username', 'empleado__user__username')

##
"""

from django.contrib import admin

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Mozo, Cajero, Auditor, Supervisor, Seguridad, Bartender, Administrador, Turno, Contratacion

class MyAdminSite(AdminSite):
    site_header = "Panel de Administración de ROXO"
    site_title = "Admin ROXO"
    index_title = "Bienvenido al Panel de Control"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(User, UserAdmin)
        self.register(Group, GroupAdmin)

admin_site = MyAdminSite(name='myadmin')


@admin.register(Mozo, site=admin_site)
class MozoAdmin(admin.ModelAdmin):
    list_display = ('user', 'zona_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'zona_asignada')

@admin.register(Cajero, site=admin_site)
class CajeroAdmin(admin.ModelAdmin):
    list_display = ('user', 'caja_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'caja_asignada')

@admin.register(Auditor, site=admin_site)
class AuditorAdmin(admin.ModelAdmin):
    list_display = ('user', 'frecuencia', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username',)

@admin.register(Supervisor, site=admin_site)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('user', 'frecuencia', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username',)

@admin.register(Seguridad, site=admin_site)
class SeguridadAdmin(admin.ModelAdmin):
    list_display = ('user', 'entrada_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'entrada_asignada')

@admin.register(Bartender, site=admin_site)
class BartenderAdmin(admin.ModelAdmin):
    list_display = ('user', 'barra_asignada', 'sueldo', 'estado', 'fecha_inicio', 'telefono')
    search_fields = ('user__username', 'barra_asignada')

#@admin.register(Administrador, site=admin_site)
#class AdministradorAdmin(admin.ModelAdmin):
#    list_display = ('user',)
#    search_fields = ('user__username',)

@admin.register(Administrador, site=admin_site)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre', 'apellido', 'cantidad_empleados_contratados')  # Agrega 'cantidad_empleados_contratados' aquí
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

"""
# Registrar tus modelos con el nuevo AdminSite
admin_site.register(Mozo, MozoAdmin)
admin_site.register(Cajero, CajeroAdmin)
admin_site.register(Auditor, AuditorAdmin)
admin_site.register(Supervisor, SupervisorAdmin)
admin_site.register(Seguridad, SeguridadAdmin)
admin_site.register(Bartender, BartenderAdmin)
admin_site.register(Administrador, AdministradorAdmin)
admin_site.register(Turno, TurnoAdmin)
admin_site.register(Contratacion, ContratacionAdmin)
"""