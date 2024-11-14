from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, models
from moduloLogin.admin import admin_site  # Importa el AdminSite personalizado de moduloLogin
from .models import Cliente, TicketEntrada, TicketArticulo, FacturaCliente, Mesa, Fiesta, RachaClientes
from django.utils.html import format_html
from django.core.cache import cache
import random
import string
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
import json
from django.db import connection

class TicketEntradaInline(TabularInline):
    model = TicketEntrada
    extra = 0
    readonly_fields = ['_cliente', '_entrada']
    fields = ['_cliente', '_entrada', '_cantidad']  # El campo _cantidad es editable

    def has_add_permission(self, request, obj=None):
        return False

    def get_extra(self, request, obj=None, **kwargs):
        return 0

    class Media:
        css = {
            'all': ('css/admin_custom_1.css',)
        }
        js = ('js/admin_custom_1.js',)

class TicketArticuloInline(TabularInline):
    model = TicketArticulo
    extra = 0
    readonly_fields = ['_cliente', '_articulo']
    fields = ['_cliente', '_articulo', '_cantidad']  # El campo _cantidad es editable

    def has_add_permission(self, request, obj=None):
        return False

    def get_extra(self, request, obj=None, **kwargs):
        return 0

    class Media:
        css = {
            'all': ('css/admin_custom_1.css',)
        }
        js = ('js/admin_custom_1.js',)

@admin.register(Cliente, site=admin_site)
class ClienteAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento')
    search_fields = ('_nombre', '_apellido', '_dni', '_cuil')
    inlines = [TicketArticuloInline, TicketEntradaInline]
    
    fieldsets = (
        ('Cliente', {
            'fields': ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento')
        }),
        ('Reservaciones', {
            'fields': ('reservaciones_view',),
        }),
    )

    # Custom method to fetch reservation data from the view for the specific client
    def fetch_reservaciones_for_cliente(self, cliente_id):
        with connection.cursor() as cursor:
            # Query the SQL view and filter by the client ID
            cursor.execute("SELECT * FROM view_cliente_reservaciones WHERE _cliente_id = %s", [cliente_id])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Format the fetched reservation data as HTML for display in the admin
    def reservaciones_view(self, obj):
        # Get reservation data for this specific client
        reservaciones = self.fetch_reservaciones_for_cliente(obj.id)

        # Format the data into an HTML table for display
        if not reservaciones:
            return "Ninguna reservación encontrada."

        html = "<table class='border-spacing-none border-separate w-full' >"
        html += "<tr>" + "".join([f"<th style='border: 2px solid #1F2937; padding: 5px;'>{col}</th>" for col in ["Número de Mesa", "Nombre de Fiesta", "Fecha"] + [k for k in reservaciones[0].keys() if k not in ["mesa_id", "_cliente_id"]]]) + "</tr>"

        for row in reservaciones:
            mesa_id = row["mesa_id"]
            mesa = Mesa.objects.get(id=mesa_id)
            fiesta = mesa.fiesta

            html += "<tr>" + \
                f"<td class='original' style='border: 2px solid #1F2937; padding: 5px;'>{mesa.numero}</td>" + \
                f"<td class='original' style='border: 2px solid #1F2937; padding: 5px;'>{fiesta.nombre}</td>" + \
                f"<td class='original' style='border: 2px solid #1F2937; padding: 5px;'>{fiesta.fecha.strftime('%Y-%m-%d')}</td>" + \
                "".join([f"<td class='original' style='border: 2px solid #1F2937; padding: 5px;'>{row[k]}</td>" for k in row.keys() if k not in ["mesa_id", "_cliente_id"]]) + \
                "</tr>"

        html += "</table>"
        return format_html(html)

    # Set the custom reservation view as a readonly field
    reservaciones_view.short_description = "Reservaciones"

    # Deshabilitar la opción de agregar nuevos registros
    def has_add_permission(self, request):
        return False

    # Deshabilitar la opción de editar registros
    def has_change_permission(self, request, obj=None):
        return True

    # Deshabilitar la opción de eliminar registros
    def has_delete_permission(self, request, obj=None):
        return False

    # Deshabilitar la opción de editar en línea (inline)
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = [f.name for f in self.model._meta.fields]
        readonly_fields.append('reservaciones_view')  # Add the custom reservation view field to read-only fields
        return readonly_fields
        return [f.name for f in self.model._meta.fields]
    
@admin.register(RachaClientes, site=admin_site)
class RachaClientesAdmin(ModelAdmin):
    list_display = ('_cliente_id', 'nombre_cliente', 'apellido_cliente', 'ultima_compra', 'racha_actual', 'racha_vigente')
    search_fields = ('producto',)
    
    list_filter = (
        ('_cliente_id'),
        ('racha_actual'),
    )
    #list_display_links = None  # Esto desactiva todos los links en la vista de lista

    def get_ordering(self, request):
        return ['-racha_actual']  # Ordenar por racha_actual
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Racha de Clientes'  # Aquí pones el título que quieras
        return super().changelist_view(request, extra_context)