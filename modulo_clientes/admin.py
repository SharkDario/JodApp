from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from moduloLogin.admin import admin_site  # Importa el AdminSite personalizado de moduloLogin
from .models import Cliente, TicketEntrada, TicketArticulo
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

# Aca tengo q poner Inlines de tickets: entradas y bebidas
# Tambien Inline de mesa reservada
class TicketEntradaInline(TabularInline):
    model = TicketEntrada
    extra = 0
    readonly_fields = ['_cliente', '_entrada']
    fields = ['_cliente', '_entrada', '_cantidad']  # El campo _cantidad es editable

class TicketArticuloInline(TabularInline):
    model = TicketArticulo
    extra = 0
    readonly_fields = ['_cliente', '_articulo']
    fields = ['_cliente', '_articulo', '_cantidad']  # El campo _cantidad es editable

@admin.register(Cliente, site=admin_site)
class ClienteAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento')
    search_fields = ('_nombre', '_apellido', '_dni', '_cuil')
    #fields = ('_user', '_dni', '_cuil', '_nombre', '_apellido', '_fecha_nacimiento')
    inlines = [TicketArticuloInline, TicketEntradaInline]
    
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
        return [f.name for f in self.model._meta.fields]