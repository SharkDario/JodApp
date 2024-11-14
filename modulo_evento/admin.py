from django.contrib import admin
from django.utils.html import format_html
from django.db import connection
from django.utils import timezone
from unfold.admin import ModelAdmin, TabularInline
from moduloLogin.admin import admin_site  # Importa el AdminSite personalizado de moduloLogin
from .forms import FiestaForm, MesaForm, EntradaInlineForm, MesaForm_2
from .models import Fiesta, Entrada, Mesa, MesaTieneArticulo, MovimientoFiesta, Administrador

class EntradaInline(TabularInline):
    model = Entrada
    form = EntradaInlineForm
    extra = 0  # No agregar entradas extras por defecto
    max_num = 2  # Máximo de 2 entradas permitidas
    min_num = 2  # Mínimo de 2 entradas requeridas
    can_delete = False

class MesaTieneArticuloInline(TabularInline):
    model = MesaTieneArticulo
    extra = 1

class MesaInline(TabularInline):
    form = MesaForm_2
    model = Mesa
    extra = 0

def set_admin_session(admin_id):
    with connection.cursor() as cursor:
        cursor.execute(f"SET @admin_id = {admin_id};")

@admin.register(Fiesta, site=admin_site)
class FiestaAdmin(ModelAdmin):
    form = FiestaForm
    change_form_template = 'admin/fiesta/change_form.html'
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_nombre', '_descripcion', '_edad_minima', '_edad_maxima', '_fecha')
    search_fields = ('_nombre', '_descripcion', '_categoria', '_vestimenta')
    
    inlines = [EntradaInline, MesaInline]
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
        ('Fiesta', {
            'fields': ('_nombre', '_descripcion', '_edad_minima', '_edad_maxima', '_fecha','_vestimenta','_categoria','_cantidad_entrada_popular', '_cantidad_entrada_vip', 'latitud', 'longitud')
        }),
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        fiesta = self.get_object(request, object_id)  # Obtén la instancia de Fiesta
        extra_context = extra_context or {}
        extra_context['mesas'] = fiesta.mesa_set.all()  # Pasa las mesas al contexto
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )
    
    def save_model(self, request, obj, form, change):
        # Obtén el ID del usuario autenticado (el administrador que está creando o editando)
        admin_id = request.user.id
        
        # Establece la variable de sesión en la base de datos
        set_admin_session(admin_id)
        
        # Guarda el modelo normalmente
        super().save_model(request, obj, form, change)
    
    class Media:
        js = ('https://www.bing.com/api/maps/mapcontrol?key=AqF8_BsEjsHhq8t5joDysX5hR6IgQILterGBHZdqRkIDA46XaKr-estp9FIa3v3b',  # Incluye el API de Bing
              'js/admin_map.js',# Archivo JS personalizado
              'js/mesas.js')  # Script para manejar la creación dinámica de mesas

    
@admin.register(Mesa, site=admin_site)
class MesaAdmin(ModelAdmin):
    form = MesaForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_fiesta', 'numero', '_categoria', '_capacidad', '_precio', '_disponibilidad')
    search_fields = ('_fiesta___nombre', '_categoria', '_capacidad', '_precio')

    fieldsets = (
        ('Mesa', {
            'fields': ('_fiesta', 'numero', '_categoria', '_capacidad', '_precio', '_disponibilidad')
        }),
    )

    inlines = [MesaTieneArticuloInline]

@admin.register(MovimientoFiesta, site=admin_site)
class MovimientoFiestaAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('_administrador', '_descripcion', '_fiesta', '_fecha')
    search_fields = ('_administrador___nombre', '_fiesta___nombre', '_fecha', '_descripcion')

    fieldsets = (
        ('Movimiento de Fiesta', {
            'fields': ('_fecha', '_administrador', '_fiesta', '_descripcion')
        }),
    )
    
    # Deshabilitar la opción de agregar nuevos registros
    def has_add_permission(self, request):
        return False

    # Deshabilitar la opción de editar registros
    def has_change_permission(self, request, obj=None):
        return False

    # Deshabilitar la opción de eliminar registros
    def has_delete_permission(self, request, obj=None):
        return False

    # Deshabilitar la opción de editar en línea (inline)
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
    
    
