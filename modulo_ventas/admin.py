
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from moduloLogin.admin import admin_site # Importa el AdminSite personalizado de moduloLogin
from .models import DetalleReservacion, DetalleEntrada, DetalleArticulo, MedioDePago, TipoFactura, FacturaCliente, TransaccionPago, generar_qr_mercado_pago
from .forms import DetalleArticuloForm, DetalleEntradaForm, DetalleReservacionForm

class DetalleReservacionInline(TabularInline):
    model = DetalleReservacion
    form = DetalleReservacionForm
    extra = 0

    class Media:
        js = ('js/detalle_reservacion.js',)

class DetalleEntradaInline(TabularInline):
    model = DetalleEntrada
    form = DetalleEntradaForm
    extra = 0

    class Media:
        js = ('js/detalle_entrada.js',)

class DetalleArticuloInline(TabularInline):
    model = DetalleArticulo
    form = DetalleArticuloForm
    extra = 0

    class Media:
        js = ('js/detalle_articulo.js',)

@admin.register(FacturaCliente, site=admin_site)
class FacturaClienteAdmin(ModelAdmin):
    list_display = ('_numero_factura', '_tipo_factura', '_fecha_emision', '_medio_de_pago', '_precio_total', '_cliente', '_empleado', '_pagado', 'ver_qr')
    search_fields = ('_numero_factura', '_fecha_emision', '_tipo_factura', '_precio_total')
    inlines = [DetalleArticuloInline, DetalleEntradaInline, DetalleReservacionInline]
    actions = ['generar_qr_mercado_pago']

    class Media:
        js = ('js/factura_cliente.js',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['_precio_total'].widget.attrs['readonly'] = True
        return form

    def generar_qr_mercado_pago(self, request, queryset):
        for factura in queryset:
            transaccion, created = TransaccionPago.objects.get_or_create(_factura=factura)
            if not transaccion.qr_url:
                qr_url, qr_image = generar_qr_mercado_pago(factura)
                transaccion.qr_url = qr_url
                transaccion.qr_image = qr_image
                transaccion.save()
        self.message_user(request, "QR generado correctamente.")

    generar_qr_mercado_pago.short_description = "Generar QR de Mercado Pago"

    """def generar_qr_mercado_pago(self, request, queryset):
        for factura in queryset:
            # Verificar si la transacción de pago ya existe
            transaccion, created = TransaccionPago.objects.get_or_create(_factura=factura)
            if not transaccion.qr_url:
                # Generar el QR si aún no está creado
                transaccion.qr_url = generar_qr_mercado_pago(factura)
                transaccion.save()
        self.message_user(request, "QR generado correctamente.")

    generar_qr_mercado_pago.short_description = "Generar QR de Mercado Pago" """

    """@admin.display(description='Ver QR')
    def ver_qr(self, obj):
        if hasattr(obj, 'transaccion_pago') and obj.transaccion_pago.qr_url:
            url = reverse('ver_qr_pago', args=[obj.id])
            return format_html(f'<a href="{url}" target="_blank">Ver QR</a>')
        return "No disponible" """
    
    @admin.display(description='Ver QR')
    def ver_qr(self, obj):
        if hasattr(obj, 'transaccion_pago') and obj.transaccion_pago.qr_image:
            url = reverse('ver_qr_pago', args=[obj.id])
            return format_html(f'<a href="{url}" target="_blank">Ver QR</a>')
        return "No disponible"
    
    ver_qr.short_description = "Ver QR"


@admin.register(TipoFactura, site=admin_site)
class TipoFacturaAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('descripcion', )
    search_fields = ('_descripcion', )

@admin.register(MedioDePago, site=admin_site)
class MedioDePAgoAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ('descripcion', )
    search_fields = ('_descripcion', )
