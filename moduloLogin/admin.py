from collections import OrderedDict
#from django import forms
from django.contrib.auth.views import LogoutView
from django.contrib import admin
#from django.utils.text import capfirst
from django.urls import path
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.sites.models import Site  # Para sites
from cities_light.models import City, Country, Region, SubRegion
from unfold.admin import ModelAdmin, TabularInline
from unfold.sites import UnfoldAdminSite
from modulo_evento.views import save_mesa_position
from modulo_ventas.views import ver_qr_pago
from modulo_analisis.views import cliente_detail_view
from modulo_clientes.views import registrar_cliente, login_view, actualizar_perfil, cambiar_password, refresh_data, reservar_mesa, comprar_entradas, comprar_carrito, confirmar_canje_cliente, obtener_tickets_cliente
from .models import Mozo, Cajero, Auditor, Supervisor, Seguridad, Bartender, Administrador, Turno, Contratacion, EmpleadoTieneTurno, Domicilio, Telefono
from .forms import ContratacionForm, EmpleadoAdminForm
# python manage.py runserver 0.0.0.0:8000
class MyAdminSite(UnfoldAdminSite):
    site_header = "Panel de Administración de ROXO"
    site_title = "Admin ROXO"
    
    index_title = "Bienvenido al Panel de Control"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('logout', LogoutView.as_view(), name='logout'),
            path('save_mesa_position/<int:mesa_id>/', save_mesa_position, name='save_mesa_position'),
            path('ver_qr_pago/<int:factura_id>/', ver_qr_pago, name='ver_qr_pago'),
            path('api/modulo_clientes/registrar/', registrar_cliente, name='registrar'),
            path('api/modulo_clientes/login/', login_view, name='login'),
            path('api/modulo_clientes/actualizar-perfil/', actualizar_perfil, name='actualizar_perfil'),
            path('api/modulo_clientes/cambiar-password/', cambiar_password, name='cambiar_password'),
            path('api/modulo_clientes/refresh-data/', refresh_data, name='refresh-data'),
            path('api/modulo_clientes/reservar-mesa/', reservar_mesa, name='reservar-mesa'),
            path('api/modulo_clientes/comprar-entradas/', comprar_entradas, name='comprar-entradas'),
            path('api/modulo_clientes/comprar-carrito/', comprar_carrito, name='comprar-carrito'),
            path('api/modulo_clientes/confirmar-canje-cliente', confirmar_canje_cliente, name='confirmar-canje-cliente'),
            path('api/modulo_clientes/obtener-tickets-cliente/<int:cliente_id>/', obtener_tickets_cliente, name='obtener-tickets-cliente'),
            #path('iniciar-canje/<int:ticket_id>/<str:tipo>/', iniciar_canje_view, name='iniciar_canje'),
            #path('confirmar-canje/<int:ticket_id>/<str:tipo>/', confirmar_canje_view, name='confirmar_canje'),
        ]
        return custom_urls + urls

    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request)
        
        # Define el orden de las aplicaciones como antes
        app_order = [
            'modulo_analisis',
            'modulo_clientes',
            'modulo_ventas',
            'modulo_evento',
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

admin_site = MyAdminSite(name='myadmin')

@admin.register(User, site=admin_site)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group, site=admin_site)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

class DomicilioInline(TabularInline):
    model = Domicilio
    search_fields = ('_ciudad',)
    extra = 1

class TelefonoInline(TabularInline):
    model = Telefono
    extra = 1

@admin.register(Mozo, site=admin_site)
class MozoAdmin(ModelAdmin):
    form = EmpleadoAdminForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_user', '_zona_asignada', '_sueldo', '_estado', '_fecha_inicio')
    search_fields = ('_user__username', '_zona_asignada')
    inlines = [DomicilioInline, TelefonoInline]
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
        ('Mozo', {
            'fields': ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento', '_zona_asignada', '_sueldo', '_estado', '_fecha_inicio', '_seniority', '_annos_experiencia', 'email')
        }),
    )

@admin.register(Cajero, site=admin_site)
class CajeroAdmin(ModelAdmin):
    form = EmpleadoAdminForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_user', '_caja_asignada', '_sueldo', '_estado', '_fecha_inicio')
    search_fields = ('_user__username', '_caja_asignada')
    inlines = [DomicilioInline, TelefonoInline]
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
        ('Cajero', {
            'fields': ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento', '_zona_asignada', '_sueldo', '_estado', '_fecha_inicio', '_seniority', '_annos_experiencia', '_caja_asignada', 'email')
        }),
    )

@admin.register(Auditor, site=admin_site)
class AuditorAdmin(ModelAdmin):
    form = EmpleadoAdminForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_user', '_frecuencia', '_sueldo', '_estado', '_fecha_inicio')
    search_fields = ('_user__username',)
    inlines = [DomicilioInline, TelefonoInline]
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
        ('Auditor', {
            'fields': ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento', '_zona_asignada', '_sueldo', '_estado', '_fecha_inicio', '_seniority', '_annos_experiencia', '_frecuencia', 'email')
        }),
    )

@admin.register(Supervisor, site=admin_site)
class SupervisorAdmin(ModelAdmin):
    form = EmpleadoAdminForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_user', '_frecuencia', '_sueldo', '_estado', '_fecha_inicio')
    search_fields = ('_user__username',)
    inlines = [DomicilioInline, TelefonoInline]
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
        ('Supervisor', {
            'fields': ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento', '_zona_asignada', '_sueldo', '_estado', '_fecha_inicio', '_seniority', '_annos_experiencia', '_frecuencia', 'email')
        }),
    )

@admin.register(Seguridad, site=admin_site)
class SeguridadAdmin(ModelAdmin):
    form = EmpleadoAdminForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_user', '_entrada_asignada', '_sueldo', '_estado', '_fecha_inicio')
    search_fields = ('_user__username', '_entrada_asignada')
    inlines = [DomicilioInline, TelefonoInline]
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
        ('Guardia de Seguridad', {
            'fields': ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento', '_zona_asignada', '_sueldo', '_estado', '_fecha_inicio', '_seniority', '_annos_experiencia', '_entrada_asignada', 'email')
        }),
    )

@admin.register(Bartender, site=admin_site)
class BartenderAdmin(ModelAdmin):
    form = EmpleadoAdminForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_user', '_barra_asignada', '_sueldo', '_estado', '_fecha_inicio')
    search_fields = ('_user__username', '_barra_asignada')
    inlines = [DomicilioInline, TelefonoInline]
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
        ('Bartender', {
            'fields': ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento', '_zona_asignada', '_sueldo', '_estado', '_fecha_inicio', '_seniority', '_annos_experiencia', '_barra_asignada', 'email')
        }),
    )

@admin.register(Administrador, site=admin_site)
class AdministradorAdmin(ModelAdmin):
    form = EmpleadoAdminForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_user', '_nombre', '_apellido', 'cantidad_empleados_contratados')
    search_fields = ('_user__username',)
    inlines = [DomicilioInline, TelefonoInline]
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
        ('Administrador', {
            'fields': ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento', '_zona_asignada', '_sueldo', '_estado', '_fecha_inicio', '_seniority', '_annos_experiencia', 'email')
        }),
    )

    def cantidad_empleados_contratados(self, obj):
        # Calcula la cantidad de empleados contratados para el administrador actual
        return obj.cantidad_empleados_contratados

    cantidad_empleados_contratados.short_description = 'Empleados contratados'  # Nombre de la columna en la lista

@admin.register(Turno, site=admin_site)
class TurnoAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_hora_inicio', '_hora_fin')
    search_fields = ('_hora_inicio', '_hora_fin')
    
    fieldsets = (
        ('Turno', {
            'fields': ('_hora_inicio', '_hora_fin')
        }),
    )

@admin.register(EmpleadoTieneTurno, site=admin_site)
class EmpleadoTieneTurnoAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_turno', '_empleado')
    search_fields = ('_turno___hora_inicio', '_turno___hora_fin', '_empleado___user__username', '_empleado___nombre')
    fieldsets = (
        ('Asignación de Turno', {
            'fields': ('_turno', '_empleado')
        }),
    )

@admin.register(Contratacion, site=admin_site)
class ContratacionAdmin(ModelAdmin):
    form = ContratacionForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_tipo', '_administrador', '_empleado', '_fecha_contratacion')
    search_fields = ('_administrador___nombre', '_empleado___nombre')
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
        ('Gestión de Contratación', {
            'fields': ('_tipo', '_administrador', '_empleado', '_fecha_contratacion')
        }),
    )

    class Media:
        js = ('js/reload_form.js',)
