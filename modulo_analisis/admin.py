"""from django.utils.html import format_html
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
from django.utils import timezone
from django import forms
from django.contrib.admin import SimpleListFilter, ListFilter
from django.forms import DateField
from datetime import datetime, time
from django.template.loader import render_to_string
from zoneinfo import ZoneInfo 
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse"""
import io
import base64
from django.db.models.functions import Coalesce
import matplotlib
matplotlib.use('Agg')  # Establecer el backend no interactivo ANTES de importar pyplot
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
import seaborn as sns
from django.db.models import Sum
import plotly.graph_objects as go
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import (
    DateRangeFilterBuilder,
    #DateTimeRangeFilterBuilder,
    #NumericRangeFilterBuilder,
    #DateRangeQuickSelectListFilterBuilder,
)
from moduloLogin.admin import admin_site  # Importa el AdminSite personalizado de moduloLogin
from .models import EntradasFiesta, MejoresClientes, ProductosMasVendidos, ReservacionesFiesta
from django.db.models.functions import TruncMonth, TruncYear
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta


def generate_bar_chart_mejores(queryset, title, x_values, y_values, x_title, y_title, num_items=10):
    #Genera un gráfico de barras estilizado
    # Preparar datos
    data = list(queryset.values(*x_values, *y_values))[:num_items]
    x_data = [' '.join(str(row[x]) for x in x_values) for row in data]
    y_data = [float(row[y_values[0]]) for row in data]

    # Generar colores degradados
    colors = [
        f'rgb({int(255-(i*(255-147))/len(y_data))}, {int(0+(i*71)/len(y_data))}, {int(255-(i*(255-193))/len(y_data))})'
        for i in range(len(y_data))
    ]

    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            text=[f'${y:,.2f}' if 'monto' in y_values[0] else f'{y:,}' for y in y_data],
            textposition='auto',
            textfont=dict(
                color='black',     # Cambia el color del texto dentro de las barras a negro
                size=14,           # Aumenta el tamaño del texto
                family="Arial",    # Cambia la fuente a una más legible (opcional)
            ),
            marker=dict(color=colors, pattern_shape="/", pattern_solidity=0.1)
        )
    ])

    return style_plotly_chart(fig, title, x_title, y_title)


def generate_bar_chart(queryset, title, x_values, y_values, x_title, y_title, num_items=10):
    """
    Genera un gráfico de barras estilizado que puede mostrar una o dos métricas
    
    Args:
        queryset: QuerySet con los datos
        title: Título del gráfico
        x_values: Lista de campos para el eje X
        y_values: Lista de campos para el eje Y (uno o dos campos)
        x_title: Título del eje X
        y_title: Título del eje Y
        num_items: Número de items a mostrar
    """
    # Preparar datos
    data = list(queryset.values(*x_values, *y_values))[:num_items]
    x_data = [' '.join(str(row[x]) for x in x_values) for row in data]
    
    # Generar colores degradados para una o dos series
    colors = [
        f'rgb({int(255-(i*(255-147))/len(data))}, {int(0+(i*71)/len(data))}, {int(255-(i*(255-193))/len(data))})'
        for i in range(len(data))
    ]
    # Configurar las barras según el número de métricas
    bars = []
    if len(y_values) == 1:
        y_data = [float(row[y_values[0]]) for row in data]
        bars.append(
            go.Bar(
                name=y_values[0].replace('_', ' ').title(),
                x=x_data,
                y=y_data,
                text=[f'${y:,.2f}' if 'monto' in y_values[0] or 'ventas' in y_values[0] else f'{y:,}' for y in y_data],
                textposition='auto',
                textfont=dict(
                    color='white',     # Cambia el color del texto dentro de las barras a negro
                    size=14,           # Aumenta el tamaño del texto
                    family="Arial",    # Cambia la fuente a una más legible (opcional)
                ),
                marker=dict(color=colors, pattern_shape="/", pattern_solidity=0.1),
                showlegend=True  # Aseguramos que se muestre la leyenda
            )
        )
    else:
        # Caso de dos métricas
        base_colors = ['#FF00FF', '#00FFFF']  # Colores base para cada métrica
        for i, y_field in enumerate(y_values):
            y_data = [float(row[y_field]) for row in data]
            bars.append(
                go.Bar(
                    name=y_field.replace('_', ' ').title(),
                    x=x_data,
                    y=y_data,
                    text=[f'${y:,.2f}' if 'monto' in y_field or 'ventas' in y_field else f'{y:,}' for y in y_data],
                    textposition='auto',
                    textfont=dict(
                        color='white',     # Cambia el color del texto dentro de las barras a negro
                        size=14,           # Aumenta el tamaño del texto
                        family="Arial",    # Cambia la fuente a una más legible (opcional)
                    ),
                    marker=dict(
                        color=base_colors[i],
                        pattern_shape="/" if i == 0 else ".",
                        pattern_solidity=0.1
                    ),
                    showlegend=True,  # Aseguramos que se muestre la leyenda
                    visible=True  # Aseguramos que la barra sea visible por defecto
                )
            )
    
    fig = go.Figure(data=bars)
    
    # Ajustar el layout para barras múltiples y leyenda
    if len(y_values) > 1:
        fig.update_layout(
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1,
            # Configuración específica de la leyenda
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(255, 255, 255, 0.1)',
                bordercolor='rgba(255, 255, 255, 0.2)',
                borderwidth=1,
                font=dict(color='white')
            )
        )
    
    styled_fig = style_plotly_chart(fig, title, x_title, y_title)
    return styled_fig


def generate_pie_chart(queryset, title, labels, values):
    """Genera un gráfico de torta estilizado con etiquetas mejoradas"""
    data = list(queryset.values(labels, values))
    
    fig = go.Figure(data=[
        go.Pie(
            labels=[str(item[labels]) for item in data],
            values=[float(item[values]) for item in data],
            textinfo='percent+label',
            textfont=dict(size=14, color="white"),  # Aumenta el tamaño de la fuente y color
            marker=dict(
                colors=px.colors.sequential.Magma,
                line=dict(color='rgb(255, 255, 255)', width=2)  # Agrega bordes blancos para contraste
            ),
            pull=[0.05] * len(data),  # Desplaza ligeramente cada sección para mayor claridad
            insidetextorientation='radial'  # Orienta el texto hacia el centro
        )
    ])
    
    return style_plotly_chart(fig, title, '', '')


def generate_line_chart(queryset, title, x_values, y_values, x_title, y_title):
    """Genera un gráfico de líneas estilizado"""
    data = list(queryset.values(*x_values, *y_values))
    
    fig = go.Figure()
    
    for y_value in y_values:
        fig.add_trace(go.Scatter(
            x=[row[x_values[0]] for row in data],
            y=[float(row[y_value]) for row in data],
            name=y_value.replace('_', ' ').title(),
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=8)
        ))

    return style_plotly_chart(fig, title, x_title, y_title)

def generate_line_chart_mejores(queryset, title, x_values, y_values, x_title, y_title):
    """Genera un gráfico de líneas estilizado con valores detallados y totales diarios"""
    from itertools import groupby
    from datetime import datetime
    
    # Obtener datos detallados
    detailed_data = list(queryset.values(*x_values, *y_values))
    
    # Preparar datos detallados
    detailed_series = {
        'x': [row[x_values[0]] for row in detailed_data],
        'y': [float(row[y_values[0]]) for row in detailed_data],
    }
    
    # Preparar datos agregados por día
    # Convertir fechas a solo fecha (sin hora) para agrupar
    daily_data = []
    for row in detailed_data:
        date = row[x_values[0]]
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        daily_data.append({
            'date': date.date(),
            'value': float(row[y_values[0]])
        })
    
    # Ordenar por fecha para la agrupación
    daily_data.sort(key=lambda x: x['date'])
    
    # Agrupar y sumar por día
    daily_totals = {}
    for date, group in groupby(daily_data, key=lambda x: x['date']):
        daily_totals[date] = sum(item['value'] for item in group)
    
    # Convertir a listas ordenadas para el gráfico
    daily_x = list(daily_totals.keys())
    daily_y = list(daily_totals.values())
    
    fig = go.Figure()
    
    # Añadir línea de valores detallados
    fig.add_trace(go.Scatter(
        x=detailed_series['x'],
        y=detailed_series['y'],
        name='Valores Detallados',
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    ))
    
    # Añadir línea de totales diarios
    fig.add_trace(go.Scatter(
        x=daily_x,
        y=daily_y,
        name='Total Diario',
        mode='lines+markers',
        line=dict(width=3, dash='solid'),
        marker=dict(size=8, symbol='diamond'),
    ))
    
    return style_plotly_chart(fig, title, x_title, y_title)

def generate_heatmap(queryset, title, x_values, y_values, z_values):
    #Genera un mapa de calor estilizado
    data = list(queryset.values(*x_values, *y_values, z_values))
    
    # Crear matriz para el heatmap
    x_unique = sorted(list(set(str(row[x_values[0]]) for row in data)))
    y_unique = sorted(list(set(str(row[y_values[0]]) for row in data)))
    
    z_matrix = [[0 for _ in range(len(x_unique))] for _ in range(len(y_unique))]
    
    for row in data:
        x_idx = x_unique.index(str(row[x_values[0]]))
        y_idx = y_unique.index(str(row[y_values[0]]))
        z_matrix[y_idx][x_idx] = float(row[z_values])

    fig = go.Figure(data=go.Heatmap(
        z=z_matrix,
        x=x_unique,
        y=y_unique,
        colorscale='Magma',
        texttemplate="%{z:.1f}",
        textfont={"size": 10},
        hoverongaps=False
    ))

    return style_plotly_chart(fig, title, x_values[0].replace('_', ' ').title(), y_values[0].replace('_', ' ').title())

def generate_sales_heatmap(queryset, title="Ventas por Mes y Producto", num_products=10):
    """
    Genera un heatmap que muestra las ventas de productos a lo largo del tiempo.
    
    Args:
        queryset: QuerySet de ProductosMasVendidos
        title: Título del gráfico
        num_products: Número de productos top a mostrar
    
    Returns:
        str: HTML del gráfico generado
    """
    # Agregar campos de fecha truncados
    data = queryset.annotate(
        mes=TruncMonth('_fecha_emision'),
        year=TruncYear('_fecha_emision')
    ).values('mes', 'producto').annotate(
        total_ventas=Sum('monto_total_ventas')
    ).order_by('mes', '-total_ventas')

    # Obtener los top productos por ventas totales
    top_productos = queryset.values('producto').annotate(
        total_ventas=Sum('monto_total_ventas')
    ).order_by('-total_ventas')[:num_products]
    productos_list = [p['producto'] for p in top_productos]

    # Filtrar solo los top productos
    data = data.filter(producto__in=productos_list)

    # Crear listas únicas ordenadas de meses y productos
    meses = sorted(list(set(row['mes'].strftime('%Y-%m') for row in data)))
    productos = productos_list

    # Crear matriz de ventas
    matriz_ventas = [[0 for _ in range(len(meses))] for _ in range(len(productos))]
    
    # Llenar la matriz con los datos de ventas
    for row in data:
        mes_idx = meses.index(row['mes'].strftime('%Y-%m'))
        prod_idx = productos.index(row['producto'])
        matriz_ventas[prod_idx][mes_idx] = row['total_ventas']

    # Crear el heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matriz_ventas,
        x=meses,
        y=productos,
        colorscale='Blues',  # Usar escala de azules
        texttemplate="$%{z:,.0f}",
        textfont={"size": 10},
        hoverongaps=False
    ))

    # Aplicar estilo personalizado
    return style_plotly_chart(
        fig,
        title,
        'Mes',
        'Producto'
    )
"""
def generate_gantt_chart(queryset, title="Calendario de Eventos"):
    
    #Genera un diagrama de Gantt para visualizar la programación de eventos/fiestas
    
    #Args:
    #    queryset: QuerySet con los datos de EntradasFiesta
    #    title: Título del gráfico
    
    from datetime import timedelta, datetime
    import plotly.graph_objects as go
    import plotly.express as px
    
    # Preparar los datos
    data = list(queryset.order_by('fecha').values('nombre_evento', 'fecha', 'categoria'))
    
    # Crear las barras para cada evento
    tasks = []
    colors = px.colors.qualitative.Set3
    color_map = {}
    event_names = []
    
    for idx, event in enumerate(data):
        # Asignar color por categoría
        if event['categoria'] not in color_map:
            color_map[event['categoria']] = colors[len(color_map) % len(colors)]
        
        # Convertir fecha a datetime si es necesario
        if isinstance(event['fecha'], str):
            start_date = datetime.strptime(event['fecha'], '%Y-%m-%d').date()
        else:
            start_date = event['fecha']
        
        # La fecha de fin es el mismo día a las 23:59
        end_date = start_date + timedelta(days=1)
        
        event_names.append(event['nombre_evento'])
        
        tasks.append(dict(
            Task=event['nombre_evento'],
            Start=start_date,
            Finish=end_date,
            Resource=event['categoria']
        ))
    
    # Crear figura
    fig = go.Figure()
    
    # Agregar una barra por cada evento
    for idx, task in enumerate(tasks):
        fig.add_trace(go.Bar(
            name=task['Task'],
            x=[70],  # Ancho de un día completo
            y=[idx],
            orientation='h',
            base=task['Start'],  # Fecha de inicio
            marker=dict(
                color=color_map[task['Resource']],
                pattern_shape="/",
                pattern_solidity=0.1,
                line=dict(color='rgb(255, 255, 255)', width=1)
            ),
            hovertemplate=(
                f"<b>{task['Task']}</b><br>"
                f"Fecha: {task['Start'].strftime('%Y-%m-%d')}<br>"
                f"Categoría: {task['Resource']}<br>"
                "<extra></extra>"
            )
        ))
    
    # Obtener el rango de fechas para el eje X
    all_dates = [task['Start'] for task in tasks]
    min_date = min(all_dates)
    max_date = max(all_dates)
    
    # Configuración básica del layout
    fig.update_layout(
        barmode='overlay',
        height=400 + (len(tasks) * 30),
        margin=dict(l=200, r=20, t=70, b=70),
        yaxis=dict(
            ticktext=event_names,
            tickvals=list(range(len(event_names))),
            autorange="reversed"
        ),
        xaxis=dict(
            type='date',
            range=[
                min_date - timedelta(days=1),  # Un día antes
                max_date + timedelta(days=2)   # Dos días después para mostrar el día completo
            ]
        )
    )
    
    # Aplicar el estilo común
    return style_plotly_chart(fig, title, 'Fecha', 'Eventos')
"""

def style_plotly_chart(fig, title, x_title, y_title):
    """Aplica un estilo consistente a los gráficos de Plotly"""
    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24, color='white')
        },
        paper_bgcolor='rgb(17, 24, 39)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={
            'tickangle': -45,
            'gridcolor': 'rgba(255,255,255,0.1)',
            'showgrid': False,
            'tickfont': {'color': 'white'},
            'title': {'text': x_title, 'font': {'color': 'white'}}
        },
        yaxis={
            'gridcolor': 'rgba(255,255,255,0.1)',
            'showgrid': True,
            'tickfont': {'color': 'white'},
            'title': {'text': y_title, 'font': {'color': 'white'}}
        },
        hoverlabel=dict(
            bgcolor="rgb(17, 24, 39)",
            font_size=16,
            font_family="Roboto",
            font_color="white"
        ),
        margin=dict(t=100, l=70, r=40, b=100),
        height=600,
        showlegend=True,
        legend=dict(
            font=dict(color='white'),
            bgcolor='rgba(0,0,0,0)'
        )
    )
    
    return fig.to_html(
        full_html=False,
        include_plotlyjs='cdn',
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
            'responsive': True
        }
    )


@admin.register(MejoresClientes, site=admin_site)
class MejoresClientesAdmin(ModelAdmin):
    list_display = ('id', '_nombre', '_apellido', 'numero_compras', 'monto_total_gastado', '_fecha_emision')
    search_fields = ('_nombre', '_apellido')
    list_display_links = None
    change_list_template = 'admin/mejores_clientes/change_list.html'

    list_per_page = 10  # Muestra 10 registros por página

    class Media:
        css = {
            'all': ('admin/css/date_filter.css',)
        }
        js = ('admin/js/date_filter.js',)

    list_filter = (
        ('_fecha_emision', DateRangeFilterBuilder()),
        ('id'),
    )
    def get_ordering(self, request):
        return ['-monto_total_gastado']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_changelist(self, request, **kwargs):
        from django.contrib.admin.views.main import ChangeList
        class CustomChangeList(ChangeList):
            def get_filters_params(self, params=None):
                """Excluir num_clients de los parámetros de filtro"""
                params = super().get_filters_params(params)
                if 'num_clients' in params:
                    del params['num_clients']
                return params
        return CustomChangeList

    def generate_charts(self, queryset, num_clients=10):
        # Primero agregamos los totales por cliente
        clientes_totales = queryset.values('id', '_nombre', '_apellido').annotate(
            total_gastado=Sum('monto_total_gastado'),
            total_compras=Sum('numero_compras')
        ).order_by('-total_gastado')
        
        # Gráfico de barras con totales
        bar_chart = generate_bar_chart_mejores(
            clientes_totales, 
            f'Top {num_clients} Clientes',
            ['_nombre', '_apellido'],
            ['total_gastado'],  # Mostramos ambas métricas
            'Clientes',
            'Cantidad de Compras / Monto Total ($)',
            num_clients
        )
            
        # Gráfico de torta también con totales
        pie_chart = generate_pie_chart(
            clientes_totales[:num_clients],
            'Distribución de Gastos por Cliente',
            '_nombre',
            'total_gastado'
        )
        
        
        # Para el gráfico de líneas mantenemos el queryset original
        # ya que queremos ver la evolución en el tiempo
        line_chart = generate_line_chart_mejores(
            queryset.order_by('_fecha_emision'),
            'Evolución de Compras por Cliente',
            ['_fecha_emision'],
            ['monto_total_gastado'],
            'Fecha',
            'Monto de Compra ($)'
        )
        
        return bar_chart, pie_chart, line_chart

    def changelist_view(self, request, extra_context=None):
        try:
            num_clients = int(request.GET.get('num_clients', 10))
            num_clients = max(1, min(num_clients, 50))
        except (ValueError, TypeError):
            num_clients = 10

        list_display = self.get_changelist_instance(request)
        queryset = list_display.get_queryset(request)
        
        bar_chart, pie_chart, line_chart = self.generate_charts(queryset, num_clients)
        
        extra_context = extra_context or {}
        extra_context.update({
            'title': 'Lista de Compras de Clientes por Fecha',
            'bar_chart': bar_chart,
            'pie_chart': pie_chart,
            'line_chart': line_chart,
            'num_clients': num_clients,
        })
        
        return super().changelist_view(request, extra_context)


@admin.register(ProductosMasVendidos, site=admin_site)
class ProductosMasVendidosAdmin(ModelAdmin):
    list_display = ('id', 'producto', 'cantidad_total_vendida', 'monto_total_ventas', '_fecha_emision')
    search_fields = ('producto',)
    change_list_template = 'admin/productos_mas_vendidos/change_list.html'
    
    list_per_page = 10
    class Media:
        css = {
            'all': ('admin/css/date_filter.css',)
        }
        js = ('admin/js/date_filter.js',)

    list_filter = (
        ('_fecha_emision', DateRangeFilterBuilder()),
        ('producto'),
    )
    list_display_links = None  # Esto desactiva todos los links en la vista de lista

    def get_ordering(self, request):
        return ['-monto_total_ventas']  # Ordenar por fecha más reciente por defecto
    
    def get_changelist(self, request, **kwargs):
        from django.contrib.admin.views.main import ChangeList
        class CustomChangeList(ChangeList):
            def get_filters_params(self, params=None):
                """Excluir num_products de los parámetros de filtro"""
                params = super().get_filters_params(params)
                if 'num_products' in params:
                    del params['num_products']
                return params
        return CustomChangeList

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def generate_charts(self, queryset, num_products=10):
        # Primero agregamos los totales por producto
        productos_totales = queryset.values('producto').annotate(
            total_vendido=Sum('cantidad_total_vendida'),
            total_ventas=Sum('monto_total_ventas')
        ).order_by('-total_ventas')
        
        # Gráfico de barras con totales agregados
        bar_chart = generate_bar_chart(
            productos_totales,
            f'Top {num_products} Productos Más Vendidos',
            ['producto'],
            ['total_vendido', 'total_ventas'],  # Cantidad y monto
            'Productos',
            'Cantidad Vendida / Monto Total ($)',
            num_products
        )
            
        # Gráfico de torta también con totales agregados
        pie_chart = generate_pie_chart(
            productos_totales[:num_products],
            'Distribución de Ventas por Producto',
            'producto',
            'total_ventas'
        )

        # Para el gráfico de líneas mantenemos el queryset original
        # ya que queremos ver la evolución en el tiempo
        line_chart = generate_line_chart_mejores(
            queryset.order_by('_fecha_emision'),
            'Evolución de Compras por Producto',
            ['_fecha_emision'],
            ['monto_total_ventas'],
            'Fecha',
            'Monto de Venta ($)'
        )
        
        # Para el heatmap, necesitamos agrupar por producto y fecha
        heatmap_data = queryset.values('producto', '_fecha_emision').annotate(
            ventas_dia=Sum('cantidad_total_vendida')
        ).order_by('-_fecha_emision')
        
        # Asegurar que tenemos los productos más vendidos para el heatmap
        top_productos = list(productos_totales[:num_products].values_list('producto', flat=True))
        heatmap_data = heatmap_data.filter(producto__in=top_productos)
        
        heatmap = generate_heatmap(
            heatmap_data,
            'Tendencias de Ventas por Producto y Fecha',
            ['producto'],
            ['_fecha_emision'],
            'ventas_dia'
        )
        
        return bar_chart, pie_chart, heatmap, line_chart

    def changelist_view(self, request, extra_context=None):
        try:
            num_products = int(request.GET.get('num_products', 10))
            num_products = max(1, min(num_products, 50))
        except (ValueError, TypeError):
            num_products = 10

        list_display = self.get_changelist_instance(request)
        queryset = list_display.get_queryset(request)
        
        bar_chart, pie_chart, heatmap, line_chart = self.generate_charts(queryset, num_products)
        
        extra_context = extra_context or {}
        extra_context.update({
            'title': 'Productos Más Vendidos',
            'bar_chart': bar_chart,
            'pie_chart': pie_chart,
            'heatmap': heatmap,
            'line_chart': line_chart,
            'num_products': num_products,
        })
        
        return super().changelist_view(request, extra_context)

"""    
    def generate_charts(self, queryset, num_products=10):
        # Gráfico de barras de productos más vendidos
        bar_chart = generate_bar_chart(
            queryset,
            f'Top {num_products} Productos Más Vendidos',
            ['producto'],
            ['cantidad_total_vendida'],
            'Productos',
            'Cantidad Vendida',
            num_products
        )
        
        # Gráfico de torta por porcentaje de ventas
        pie_chart = generate_pie_chart(
            queryset[:num_products],
            'Distribución de Ventas por Producto',
            'producto',
            'monto_total_ventas'
        )
        
        # Mapa de calor de ventas por producto y fecha
        heatmap = generate_heatmap(
            queryset,
            'Tendencias de Ventas por Producto',
            ['producto'],
            ['_fecha_emision'],
            'cantidad_total_vendida'
        )
        
        return bar_chart, pie_chart, heatmap

    def changelist_view(self, request, extra_context=None):
        try:
            num_products = int(request.GET.get('num_products', 10))
            num_products = max(1, min(num_products, 50))
        except (ValueError, TypeError):
            num_products = 10

        list_display = self.get_changelist_instance(request)
        queryset = list_display.get_queryset(request)
        
        bar_chart, pie_chart, heatmap = self.generate_charts(queryset, num_products)
        
        extra_context = extra_context or {}
        extra_context.update({
            'title': 'Productos Más Vendidos',
            'bar_chart': bar_chart,
            'pie_chart': pie_chart,
            'heatmap': heatmap,
            'num_products': num_products,
        })
        
        return super().changelist_view(request, extra_context)
    
"""

@admin.register(EntradasFiesta, site=admin_site)
class EntradasFiestaAdmin(ModelAdmin):
    list_display = ('evento_id', 'nombre_evento', 'fecha', 'total_entradas_vendidas', 'categoria', 'monto_total_ventas')
    search_fields = ('nombre_evento',)
    list_per_page = 10
    change_list_template = 'admin/entradas_fiesta/change_list.html'

    class Media:
        css = {
            'all': ('admin/css/date_filter.css',)
        }
        js = ('admin/js/date_filter.js',)

    list_filter = (
        ('fecha', DateRangeFilterBuilder()),
    )
    def get_ordering(self, request):
        return ['-monto_total_ventas']  # Ordenar por fecha más reciente por defecto
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def generate_charts(self, queryset):
        # Gráfico de barras de ventas por evento
        bar_chart = generate_bar_chart(
            queryset,
            'Ventas de Entradas por Evento',
            ['nombre_evento'],
            ['total_entradas_vendidas', 'monto_total_ventas'],
            'Eventos',
            'Entradas Vendidas'
        )
        
        # Gráfico de líneas de ventas en el tiempo
        line_chart = generate_line_chart(
            queryset.order_by('fecha'),
            'Evolución de Ventas de Entradas',
            ['fecha'],
            ['total_entradas_vendidas', 'monto_total_ventas'],
            'Fecha',
            'Cantidad / Monto'
        )
        
        # Gráfico de torta por categoría
        pie_chart = generate_pie_chart(
            queryset,
            'Distribución de Ventas por Categoría',
            'categoria',
            'total_entradas_vendidas'
        )
        
        heatmap = generate_heatmap(
            queryset,
            'Tendencias de Ventas de Entradas por Fiesta y Fecha',
            ['nombre_evento'],
            ['fecha'],
            'total_entradas_vendidas'
        )

        return bar_chart, line_chart, pie_chart, heatmap

    def changelist_view(self, request, extra_context=None):
        list_display = self.get_changelist_instance(request)
        queryset = list_display.get_queryset(request)
        
        bar_chart, line_chart, pie_chart, heatmap = self.generate_charts(queryset)
        
        extra_context = extra_context or {}
        extra_context.update({
            'bar_chart': bar_chart,
            'line_chart': line_chart,
            'pie_chart': pie_chart,
            'heatmap': heatmap,
        })
        
        return super().changelist_view(request, extra_context)

@admin.register(ReservacionesFiesta, site=admin_site)
class ReservacionesFiestaAdmin(ModelAdmin):
    list_display = ('id', 'nombre_evento', 'fecha', 'total_reservaciones', 'categoria', 'monto_total_ventas')
    search_fields = ('nombre_evento',)
    list_per_page = 10
    change_list_template = 'admin/reservaciones_fiesta/change_list.html'
    class Media:
        css = {
            'all': ('admin/css/date_filter.css',)
        }
        js = ('admin/js/date_filter.js',)

    list_filter = (
        ('fecha', DateRangeFilterBuilder()),
    )
    def get_ordering(self, request):
        return ['-monto_total_ventas']  # Ordenar por fecha más reciente por defecto
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def generate_charts(self, queryset):
        # Gráfico de barras de ventas por evento
        bar_chart = generate_bar_chart(
            queryset,
            'Reservaciones por Evento',
            ['nombre_evento'],
            ['total_reservaciones', 'monto_total_ventas'],
            'Eventos',
            'Reservaciones'
        )
        
        # Gráfico de líneas de ventas en el tiempo
        line_chart = generate_line_chart(
            queryset.order_by('fecha'),
            'Evolución de Reservaciones',
            ['fecha'],
            ['total_reservaciones', 'monto_total_ventas'],
            'Fecha',
            'Cantidad / Monto'
        )
        
        # Gráfico de torta por categoría
        pie_chart = generate_pie_chart(
            queryset,
            'Distribución de Reservaciones por Categoría',
            'categoria',
            'total_reservaciones'
        )
        
        return bar_chart, line_chart, pie_chart

    def changelist_view(self, request, extra_context=None):
        list_display = self.get_changelist_instance(request)
        queryset = list_display.get_queryset(request)
        
        bar_chart, line_chart, pie_chart = self.generate_charts(queryset)
        
        extra_context = extra_context or {}
        extra_context.update({
            'bar_chart': bar_chart,
            'line_chart': line_chart,
            'pie_chart': pie_chart,
        })
        
        return super().changelist_view(request, extra_context)


"""

@admin.register(ProductosMasVendidos, site=admin_site)
class ProductosMasVendidosAdmin(ModelAdmin):
    # ... (mantener configuración existente) ...

    def generate_charts(self, queryset, num_products=10):
        # Gráfico de barras de productos más vendidos
        bar_chart = generate_bar_chart(
            queryset,
            f'Top {num_products} Productos Más Vendidos',
            ['producto'],
            ['cantidad_total_vendida'],
            'Productos',
            'Cantidad Vendida',
            num_products
        )
        
        # Gráfico de torta por porcentaje de ventas
        pie_chart = generate_pie_chart(
            queryset[:num_products],
            'Distribución de Ventas por Producto',
            'producto',
            'monto_total_ventas'
        )
        
        # Mapa de calor de ventas por producto y fecha
        heatmap = generate_heatmap(
            queryset,
            'Tendencias de Ventas por Producto',
            ['producto'],
            ['_fecha_emision'],
            'cantidad_total_vendida'
        )
        
        return bar_chart, pie_chart, heatmap

    def changelist_view(self, request, extra_context=None):
        try:
            num_products = int(request.GET.get('num_products', 10))
            num_products = max(1, min(num_products, 50))
        except (ValueError, TypeError):
            num_products = 10

        list_display = self.get_changelist_instance(request)
        queryset = list_display.get_queryset(request)
        
        bar_chart, pie_chart, heatmap = self.generate_charts(queryset, num_products)
        
        extra_context = extra_context or {}
        extra_context.update({
            'title': 'Productos Más Vendidos',
            'bar_chart': bar_chart,
            'pie_chart': pie_chart,
            'heatmap': heatmap,
            'num_products': num_products,
        })
        
        return super().changelist_view(request, extra_context)

@admin.register(EntradasFiesta, site=admin_site)
class EntradasFiestaAdmin(ModelAdmin):
    # ... (mantener configuración existente) ...

    def generate_charts(self, queryset):
        # Gráfico de barras de ventas por evento
        bar_chart = generate_bar_chart(
            queryset,
            'Ventas de Entradas por Evento',
            ['nombre_evento'],
            ['total_entradas_vendidas'],
            'Eventos',
            'Entradas Vendidas'
        )
        
        # Gráfico de líneas de ventas en el tiempo
        line_chart = generate_line_chart(
            queryset,
            'Evolución de Ventas de Entradas',
            ['fecha'],
            ['total_entradas_vendidas', 'monto_total_ventas'],
            'Fecha',
            'Cantidad / Monto'
        )
        
        # Gráfico de torta por categoría
        pie_chart = generate_pie_chart(
            queryset,
            'Distribución de Ventas por Categoría',
            'categoria',
            'total_entradas_vendidas'
        )
        
        return bar_chart, line_chart, pie_chart

    def changelist_view(self, request, extra_context=None):
        list_display = self.get_changelist_instance(request)
        queryset = list_display.get_queryset(request)
        
        bar_chart, line_chart, pie_chart = self.generate_charts(queryset)
        
        extra_context = extra_context or {}
        extra_context.update({
            'bar_chart': bar_chart,
            'line_chart': line_chart,
            'pie_chart': pie_chart,
        })
        
        return super().changelist_view(request, extra_context)



    <!--

{% block content %}
{{ block.super }}
    <div class="chart-controls" style="margin: 20px; padding: 20px; background-color: #A1067D; border-color: #FF00FF; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.3);">
        <label for="num_clients" style="color: white; font-size: 16px;">Gráfico de Barras</label>
    </div>
    <div class="chart-controls" style="margin: 20px; padding: 20px; background-color: #1F2937; border-color: #FF00FF; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.3);">
        <form method="get" style="display: flex; align-items: center; gap: 10px;">
            <label for="num_clients" style="color: white; font-size: 16px;">Cantidad del Top:</label>
            <input 
                type="number" 
                id="num_clients" 
                name="num_clients" 
                value="{{ num_clients }}" 
                min="1" 
                max="50" 
                style="
                    padding: 8px;
                    border-radius: 4px;
                    border: 1px solid #A1067D;
                    background-color: rgb(31, 41, 55);
                    color: white;
                    width: 80px;
                "
            >
            <button 
                type="submit" 
                style="
                    padding: 8px 16px;
                    background-color: #A1067D;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                "
                onmouseover="this.style.backgroundColor='#FF00FF'"
                onmouseout="this.style.backgroundColor='#A1067D'"
            >
                Actualizar
            </button>
            {% for key, value in request.GET.items %}
                {% if key != 'num_clients' %}
                    <input type="hidden" name="{{ key }}" value="{{ value }}">
                {% endif %}
            {% endfor %}
        </form>
    </div>

    <div class="chart-container" style="margin: 0 20px 20px; padding: 20px; background-color: rgb(17, 24, 39); border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.3);">
        <div style="width: 100%; max-width: 1200px; margin: 0 auto;">
            {{ plot_html|safe }}
        </div>
    </div>
{% endblock %}

{% extends "admin/change_list.html" %}
{% load static %}

-->
"""