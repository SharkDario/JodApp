from django import forms
from django.contrib import admin
from django.utils.text import capfirst
from collections import OrderedDict
from django.urls import path, include
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Mozo, Cajero, Auditor, Supervisor, Seguridad, Bartender, Administrador, Turno, Contratacion, EmpleadoTieneTurno, Domicilio, Telefono
from .forms import ContratacionForm, EmpleadoAdminForm
from modulo_evento.views import crear_evento

class MyAdminSite(AdminSite):
    site_header = "Panel de Administración de ROXO"
    site_title = "Admin ROXO"
    index_title = "Bienvenido al Panel de Control"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(User, UserAdmin)
        self.register(Group, GroupAdmin)
    
    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request)
        
        # Define el orden de las aplicaciones como antes
        app_order = [
            'modulo_stock',
            'moduloLogin',
            'auth',
            # etc.
        ]

        # Si app_label está definido, filtra solo la app correspondiente
        if app_label is not None:
            app_dict = {k: v for k, v in app_dict.items() if k == app_label}


        # Ordenar el diccionario de aplicaciones
        ordered_app_list = OrderedDict()
        for app_name in app_order:
            if app_name in app_dict:
                ordered_app_list[app_name] = app_dict.pop(app_name)

        # Agregar las aplicaciones restantes (las que no están en el orden manual)
        ordered_app_list.update(app_dict)

        # Ordenar los modelos dentro de cada app
        for app in ordered_app_list.values():
            if app['app_label'] == 'modulo_stock':  # Especificar el orden de los modelos en 'modulo_stock'
                model_order = ['Producto', 'Trago', 'Fabricacion', 'MovimientoStock', 'Proveedor', 'RemitoProveedor', 'EstadoProducto', 'DetalleRemitoProveedor'] 
                app['models'].sort(key=lambda x: model_order.index(x['object_name']) if x['object_name'] in model_order else 999)
            if app['app_label'] == 'moduloLogin':  # Especificar el orden de los modelos en 'modulo_stock'
                model_order = ['Administrador', 'Auditor', 'Supervisor', 'Cajero', 'Seguridad', 'Bartender', 'Mozo', 'Contratacion', 'Turno', 'EmpleadoTieneTurno'] 
                app['models'].sort(key=lambda x: model_order.index(x['object_name']) if x['object_name'] in model_order else 999)

        return list(ordered_app_list.values())
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('modulo_evento/fiesta/add/', crear_evento, name='crear_evento'),
        ]
        return custom_urls + urls


admin_site = MyAdminSite(name='myadmin')

class DomicilioInline(admin.TabularInline):
    model = Domicilio
    search_fields = ('_ciudad',)
    extra = 1

class TelefonoInline(admin.TabularInline):
    model = Telefono
    extra = 1

@admin.register(Mozo, site=admin_site)
class MozoAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'zona_asignada', 'sueldo', 'estado', 'fecha_inicio')
    search_fields = ('_user__username', '_zona_asignada')
    inlines = [DomicilioInline, TelefonoInline]

@admin.register(Cajero, site=admin_site)
class CajeroAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'caja_asignada', 'sueldo', 'estado', 'fecha_inicio')
    search_fields = ('_user__username', '_caja_asignada')
    inlines = [DomicilioInline, TelefonoInline]

@admin.register(Auditor, site=admin_site)
class AuditorAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'frecuencia', 'sueldo', 'estado', 'fecha_inicio')
    search_fields = ('_user__username',)
    inlines = [DomicilioInline, TelefonoInline]

@admin.register(Supervisor, site=admin_site)
class SupervisorAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'frecuencia', 'sueldo', 'estado', 'fecha_inicio')
    search_fields = ('_user__username',)
    inlines = [DomicilioInline, TelefonoInline]

@admin.register(Seguridad, site=admin_site)
class SeguridadAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'entrada_asignada', 'sueldo', 'estado', 'fecha_inicio')
    search_fields = ('_user__username', '_entrada_asignada')
    inlines = [DomicilioInline, TelefonoInline]

@admin.register(Bartender, site=admin_site)
class BartenderAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'barra_asignada', 'sueldo', 'estado', 'fecha_inicio')
    search_fields = ('_user__username', '_barra_asignada')
    inlines = [DomicilioInline, TelefonoInline]

@admin.register(Administrador, site=admin_site)
class AdministradorAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ('user', 'nombre', 'apellido', 'cantidad_empleados_contratados')
    search_fields = ('_user__username',)
    inlines = [DomicilioInline, TelefonoInline]

    def cantidad_empleados_contratados(self, obj):
        # Calcula la cantidad de empleados contratados para el administrador actual
        return obj.cantidad_empleados_contratados

    cantidad_empleados_contratados.short_description = 'Empleados contratados'  # Nombre de la columna en la lista

@admin.register(Turno, site=admin_site)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('hora_inicio', 'hora_fin')
    search_fields = ('_hora_inicio', '_hora_fin')

@admin.register(EmpleadoTieneTurno, site=admin_site)
class EmpleadoTieneTurnoAdmin(admin.ModelAdmin):
    list_display = ('turno', 'empleado')
    search_fields = ('_turno___hora_inicio', '_turno___hora_fin', '_empleado___user__username', '_empleado___nombre')

@admin.register(Contratacion, site=admin_site)
class ContratacionAdmin(admin.ModelAdmin):
    form = ContratacionForm
    list_display = ('tipo', 'administrador', 'empleado', 'fecha_contratacion')
    search_fields = ('_administrador___nombre', '_empleado___nombre')
    class Media:
        js = ('js/reload_form.js',)
