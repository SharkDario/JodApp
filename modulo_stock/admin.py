from django.contrib import admin
from django.utils import timezone
from moduloLogin.admin import admin_site  # Importa el AdminSite personalizado de moduloLogin
from unfold.admin import ModelAdmin, TabularInline
from .models import Proveedor, RemitoProveedor, MovimientoStock, Empleado, Producto, EstadoProducto, DetalleRemitoProveedor, Fabricacion, Marca, Trago
from .forms import TragoAdminForm

@admin.register(Proveedor, site=admin_site)
class ProveedorAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('nombre', 'condicion_iva', 'dni', 'cuil')
    search_fields = ('_nombre', '_dni', '_cuil')

class DetalleRemitoProveedorInline(TabularInline):
    model = DetalleRemitoProveedor
    extra = 1

@admin.register(RemitoProveedor, site=admin_site)
class RemitoProveedorAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('numero_remito', 'fecha_emision_remito', 'proveedor')
    search_fields = ('_numero_remito', '_proveedor___nombre')
    inlines = [DetalleRemitoProveedorInline]


@admin.register(Producto, site=admin_site)
class ProductoAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('nombre', 'marca', 'precio_unitario', 'stock')
    search_fields = ('_nombre', '_marca')
    def save_model(self, request, obj, form, change):
        #Sobreescribir el método save_model para registrar los cambios de stock realizados por un empleado.
        if change:  # Verifica si es un cambio y no una creación
            # Obtener el stock anterior antes de los cambios
            producto_anterior = Producto.objects.get(pk=obj.pk)
            cambio_stock = obj._stock - producto_anterior._stock

            if cambio_stock != 0:
                # Obtener el empleado relacionado con el usuario que hizo el cambio
                empleado = Empleado.objects.get(_user=request.user)

                # Registrar el movimiento de stock
                MovimientoStock.objects.create(
                    _empleado=empleado,
                    _producto=obj,
                    _cantidad=cambio_stock,
                    _fecha_movimiento=timezone.now()
                )

        # Guardar los cambios normalmente
        super().save_model(request, obj, form, change)


@admin.register(EstadoProducto, site=admin_site)
class EstadoProductoAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('descripcion',)
    search_fields = ('_descripcion',)

@admin.register(Marca, site=admin_site)
class MarcaAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('nombre',)
    search_fields = ('nombre',)

class FabricacionInline(TabularInline):
    model = Fabricacion
    extra = 1

@admin.register(Trago, site=admin_site)
class TragoAdmin(ModelAdmin):
    form = TragoAdminForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('nombre', 'precio_unitario', 'stock', 'volumen')
    search_fields = ('_nombre',)
    inlines = [FabricacionInline]

@admin.register(MovimientoStock, site=admin_site)
class MovimientoStockAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('empleado', 'producto', 'cantidad', 'fecha_movimiento')
    search_fields = ('_empleado__nombre', '_producto__nombre')
    
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