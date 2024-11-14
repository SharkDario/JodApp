from datetime import datetime, timedelta
import re
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.core.cache import cache
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from modulo_ventas.models import generar_qr_mercado_pago
from .models import Cliente, Persona, Fiesta, Producto, Trago, Mesa, Entrada, MesaTieneArticulo, FacturaCliente, DetalleReservacion, TipoFactura, MedioDePago, TransaccionPago, DetalleEntrada, DetalleArticulo, Articulo, TicketArticulo, TicketEntrada
from django.core.cache import cache
import random
import string
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.db import connection

def get_cliente_stats(cliente_id):
    # Para las reservaciones (contar ocurrencias del cliente_id)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(DISTINCT mesa_id) as total_reservaciones
            FROM view_cliente_reservaciones
            WHERE _cliente_id = %s
        """, [cliente_id])
        reservaciones = cursor.fetchone()[0] or 0

    # Para la racha actual
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT racha_actual
            FROM view_cliente_racha
            WHERE _cliente_id = %s
        """, [cliente_id])
        result = cursor.fetchone()
        racha = result[0] if result else 0

    # Para el total de productos comprados
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COALESCE(SUM(Cantidad), 0) as total_productos
            FROM view_cliente_productos
            WHERE _cliente_id = %s
        """, [cliente_id])
        total_productos = cursor.fetchone()[0] or 0

    # Para el total de entradas compradas
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COALESCE(SUM(Cantidad), 0) as total_entradas
            FROM view_cliente_entradas
            WHERE _cliente_id = %s
        """, [cliente_id])
        total_entradas = cursor.fetchone()[0] or 0

    return {
        'total_reservaciones': reservaciones,
        'racha_actual': racha,
        'total_productos': total_productos,
        'total_entradas': total_entradas
    }

User = get_user_model()

def generar_url_mercado_pago(factura):
    transaccion, created = TransaccionPago.objects.get_or_create(_factura=factura)
    if not transaccion.qr_url:
        qr_url, qr_image = generar_qr_mercado_pago(factura)
        transaccion.qr_url = qr_url
        transaccion.qr_image = qr_image
        transaccion.save()
    return qr_url

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirmar_canje_cliente(request):
    """
    View para que el cliente confirme un canje desde la app
    """
    try:
        codigo = request.data.get('codigo')
        ticket_id = request.data.get('ticket_id')
        tipo = request.data.get('tipo')
        cliente_id = request.data.get('cliente_id')

        if not all([codigo, ticket_id, tipo]):
            return Response({
                'error': 'Faltan datos requeridos'
            }, status=400)

        # Verificar que el código coincida con el almacenado
        cache_key = f'canje_{ticket_id}_{tipo}'  # Corregido para coincidir con el formato del admin
        datos_canje = cache.get(cache_key)

        if not datos_canje:
            return Response({
                'error': 'Solicitud de canje no encontrada o expirada'
            }, status=400)

        if codigo != datos_canje['codigo']:
            return Response({
                'error': 'Código incorrecto'
            }, status=400)

        # Verificar que el ticket pertenezca al cliente
        if tipo == 'articulo':
            ticket = TicketArticulo.objects.get(id=ticket_id, _cliente_id=cliente_id)
        else:
            ticket = TicketEntrada.objects.get(id=ticket_id, _cliente_id=cliente_id)

        # Actualizar estado en cache
        datos_canje['confirmado'] = True
        datos_canje['cliente_id'] = cliente_id
        cache.set(cache_key, datos_canje, timeout=300)

        return Response({
            'success': True,
            'mensaje': 'Canje confirmado exitosamente'
        })

    except (TicketArticulo.DoesNotExist, TicketEntrada.DoesNotExist):
        return Response({
            'error': 'Ticket no encontrado o no autorizado'
        }, status=404)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_tickets_cliente(request, cliente_id):
    """
    View para obtener los tickets disponibles del cliente
    """
    if not cliente_id:
        return Response({
            'error': 'ID de cliente no proporcionado'
        }, status=400)

    tickets_articulos = TicketArticulo.objects.filter(
        _cliente_id=cliente_id,
        _cantidad__gt=0
    ).select_related('_articulo')

    tickets_entradas = TicketEntrada.objects.filter(
        _cliente_id=cliente_id,
        _cantidad__gt=0
    ).select_related('_entrada')

    return Response({
        'articulos': [{
            'id': t.id,
            'tipo': 'articulo',
            'nombre': t.articulo.nombre,
            'cantidad': t.cantidad
        } for t in tickets_articulos],
        'entradas': [{
            'id': t.id,
            'tipo': 'entrada',
            'fiesta': t.entrada.fiesta.nombre,
            'categoria': t.entrada.categoria,
            'cantidad': t.cantidad
        } for t in tickets_entradas]
    })

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def comprar_entradas(request):
    try:
        with transaction.atomic():
            # Obtener datos del request
            entrada_id = request.data.get('entrada_id')
            cantidad = request.data.get('cantidad')
            cliente_id = request.data.get('cliente_id')
            fiesta_id = request.data.get('fiesta_id')
            
            # Validar que la entrada existe y está disponible
            try:
                entrada = Entrada.objects.select_for_update().get(id=entrada_id)
                fiesta = Fiesta.objects.select_for_update().get(id=fiesta_id)
                if (fiesta.cantidad_entrada_popular<cantidad) & (entrada.categoria=="Popular"):
                    return Response({
                        'error': 'La cantidad de entradas no están disponibles'
                    }, status=status.HTTP_400_BAD_REQUEST)
                if (fiesta.cantidad_entrada_vip<cantidad) & (entrada.categoria=="VIP"):
                    return Response({
                        'error': 'La cantidad de entradas no están disponibles'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({
                    'error': 'Entrada no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)
            
            tipo_factura = TipoFactura.objects.filter_by_descripcion("B")
            medio_de_pago = MedioDePago.objects.filter_by_descripcion("Mercado Pago")
            
            # Crear factura
            factura = FacturaCliente(
                _cliente_id=cliente_id,
                _tipo_factura = tipo_factura[0],
                _medio_de_pago = medio_de_pago[0],
                _precio_total= (entrada.precio_unitario*cantidad),
            )
            factura.save()

            # Crear detalle de reservación
            detalle = DetalleEntrada(
                _factura=factura,
                _cantidad=cantidad,
                _precio_unitario= entrada.precio_unitario,
                _subtotal= (entrada.precio_unitario*cantidad),
                _entrada=entrada
            )
            detalle.save()

            # Crear o actualizar ticket de entrada 
            # CHANGE
            
            try:
                ticket = TicketEntrada.objects.select_for_update().get(
                    _cliente_id=cliente_id,
                    _entrada_id=entrada_id
                )
                # Si existe, actualizar cantidad
                ticket.cantidad = ticket.cantidad + cantidad
                ticket.save()
            except TicketEntrada.DoesNotExist:
                # Si no existe, crear nuevo ticket
                ticket = TicketEntrada(
                    _cliente_id=cliente_id,
                    _entrada_id=entrada_id,
                    _cantidad=cantidad
                )
                ticket.save()
            
            # Temporal en la fase beta: 
            # Como no se puede manejar notificaciones de pagos (Webhooks para mercado pago) sin subir el proyecto backend a un servidor
            # Se reduce la cantidad de entradas populares o vip de las cantidades de la fiesta
            # Y ademas se cambia el estado de la factura a pagado, ya que no podemos verificar el pago sin utilizar webhooks 
            if (entrada.categoria=="Popular"):
                fiesta.cantidad_entrada_popular = fiesta.cantidad_entrada_popular - cantidad
            if (entrada.categoria=="VIP"):
                fiesta.cantidad_entrada_vip = fiesta.cantidad_entrada_vip - cantidad
            
            

            # Actualizar pago
            factura.pagado = True
            factura.save()

            pago_url = generar_url_mercado_pago(factura)
            #fiesta.save()
            return Response({
                'success': True,
                'message': 'Entradas compradas exitosamente',
                'factura_id': factura.pk,
                'pago_url': pago_url
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def comprar_carrito(request):
    try:
        with transaction.atomic():
            # Obtener datos del request
            items = request.data.get('items', [])
            cliente_id = request.data.get('cliente_id')
            
            if not items or not cliente_id:
                return Response({
                    'error': 'Datos incompletos'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validar stock de cada artículo
            total_amount = 0
            for item in items:
                articulo_id = item.get('id')
                cantidad = item.get('cantidad')
                tipo = item.get('tipo')  # 'trago' o 'producto'

                try:
                    articulo = Articulo.objects.select_for_update().get(id=articulo_id)
                    if articulo.stock < cantidad:
                        return Response({
                            'error': f'Stock insuficiente para {articulo.nombre}'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    total_amount += articulo.precio_unitario * cantidad
                except Articulo.DoesNotExist:
                    return Response({
                        'error': f'Artículo no encontrado: {articulo_id}'
                    }, status=status.HTTP_404_NOT_FOUND)

            # Crear factura
            tipo_factura = TipoFactura.objects.filter_by_descripcion("B")[0]
            medio_de_pago = MedioDePago.objects.filter_by_descripcion("Mercado Pago")[0]

            factura = FacturaCliente(
                _cliente_id=cliente_id,
                _tipo_factura=tipo_factura,
                _medio_de_pago=medio_de_pago,
                _precio_total=total_amount,
            )
            factura.save()

            # Crear detalles de artículos y actualizar stock
            for item in items:
                articulo_id = item['id']
                cantidad = item['cantidad']
                
                articulo = Articulo.objects.get(id=articulo_id)
                
                # Crear detalle de artículo
                detalle = DetalleArticulo(
                    _factura=factura,
                    _articulo=articulo,
                    _cantidad=cantidad,
                    _precio_unitario=articulo.precio_unitario,
                    _subtotal=(articulo.precio_unitario * cantidad)
                )
                detalle.save()

                # Crear o actualizar ticket de artículo
                # CHANGE
                
                try:
                    ticket = TicketArticulo.objects.select_for_update().get(
                        _cliente_id=cliente_id,
                        _articulo_id=articulo_id
                    )
                    # Si existe, actualizar cantidad
                    ticket.cantidad = ticket.cantidad + cantidad
                    ticket.save()
                except TicketArticulo.DoesNotExist:
                    # Si no existe, crear nuevo ticket
                    ticket = TicketArticulo(
                        _cliente_id=cliente_id,
                        _articulo_id=articulo_id,
                        _cantidad=cantidad
                    )
                    ticket.save()
                
            # Temporal en la fase beta:
            # Actualizar estado de pago directamente
            factura.pagado = True
            factura.save()

            # Generar URL de pago
            pago_url = generar_url_mercado_pago(factura)

            return Response({
                'success': True,
                'message': 'Carrito comprado exitosamente',
                'factura_id': factura.pk,
                'pago_url': pago_url
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reservar_mesa(request):
    try:
        with transaction.atomic():
            # Obtener datos del request
            mesa_id = request.data.get('mesa_id')
            cliente_id = request.data.get('cliente_id')
            
            # Validar que la mesa existe y está disponible
            try:
                mesa = Mesa.objects.select_for_update().get(id=mesa_id)
                if not mesa.disponibilidad:
                    return Response({
                        'error': 'La mesa no está disponible'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({
                    'error': 'Mesa no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)
            
            tipo_factura = TipoFactura.objects.filter_by_descripcion("B")
            medio_de_pago = MedioDePago.objects.filter_by_descripcion("Mercado Pago")
            
            # Crear factura
            factura = FacturaCliente(
                _cliente_id=cliente_id,
                _tipo_factura = tipo_factura[0],
                _medio_de_pago = medio_de_pago[0],
                _precio_total=mesa.precio
            )
            factura.save()

            # Crear detalle de reservación
            detalle = DetalleReservacion(
                _factura=factura,
                _cantidad=1,
                _precio_unitario=mesa.precio,
                _subtotal=mesa.precio,
                _reservacion=mesa
            )
            detalle.save()

            # Temporal en la fase beta: 
            # Como no se puede manejar notificaciones de pagos (Webhooks para mercado pago) sin subir el proyecto backend a un servidor
            # Se establece la disponibilidad de la mesa como falsa
            # Y ademas se cambia el estado de la factura a pagado, ya que no podemos verificar el pago sin utilizar webhooks 
            # Actualizar disponibilidad de la mesa
            mesa.disponibilidad = False
            mesa.save()
            # Actualizar pago
            factura.pagado = True
            factura.save()

            pago_url = generar_url_mercado_pago(factura)

            return Response({
                'success': True,
                'message': 'Mesa reservada exitosamente',
                'factura_id': factura.pk,
                'pago_url': pago_url
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def actualizar_perfil(request):
    try:
        # Actualizar datos del usuario
        user = request.user
        email = request.data.get('email', user.email)
        # Validar existencia del email
        if User.objects.filter(email=email).exists():
            if (email!='') & (user.email!=email):
                return Response({
                    'error': 'El correo electrónico ya está en uso.'
                }, status=400)

        user.email = request.data.get('email', user.email)
        user.save()

        # Actualizar datos del cliente
        cliente = Cliente.objects.get(_user=user)
        cliente.nombre = request.data.get('nombre', cliente.nombre)
        cliente.apellido = request.data.get('apellido', cliente.apellido)
        dni = request.data.get('dni', cliente.dni)
        cuil = request.data.get('cuil', cliente.cuil)
        cliente.fecha_nacimiento = request.data.get('fecha_nacimiento', cliente.fecha_nacimiento)

        error = ""

        # Validar existencia del DNI y CUIL
        if(cliente.dni!=dni) & (Persona.objects.filter_by_dni(dni).exists()):
            error += 'El DNI ya está registrado.\n'

        if(cliente.cuil!=cuil) & (Persona.objects.filter_by_cuil(cuil).exists()):
            error += 'El CUIL ya está registrado.\n'
        
        # Validar que el CUIL contenga el DNI
        if dni not in cuil:
            error += 'El CUIL debe contener el DNI.\n'

        # Validar edad mayor o igual a 18
        try:
            fecha_nacimiento = datetime.strptime(cliente.fecha_nacimiento, '%Y-%m-%d').date()
            edad = (datetime.today().date() - fecha_nacimiento).days // 365
            if edad < 18:
                error += 'Debe ser mayor de 18 años.\n'
        except ValueError:
            error += 'Formato de fecha de nacimiento inválido. Debe ser YYYY-MM-DD.\n'

        if(error!=""):
            return Response({
            'error': error
        }, status=400)

        cliente.dni = request.data.get('dni', cliente.dni)
        cliente.cuil = request.data.get('cuil', cliente.cuil)
        cliente.save()

        # Serializar y devolver los datos actualizados
        return Response({
            'message': 'Perfil actualizado correctamente',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'cliente': {
                'id': cliente.id,
                'nombre': cliente.nombre,
                'apellido': cliente.apellido,
                'dni': cliente.dni,
                'cuil': cliente.cuil,
                'fecha_nacimiento': cliente.fecha_nacimiento,
                #'embedding': cliente.embedding,
                #'foto': cliente.foto,
            }
        })
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=400)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cambiar_password(request):
    try:
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Verificar que se proporcionaron las contraseñas
        if not old_password or not new_password:
            return Response({
                'error': 'Debe proporcionar la contraseña actual y la nueva'
            }, status=400)

        # Verificar que la contraseña actual es correcta
        if not check_password(old_password, user.password):
            return Response({
                'error': 'La contraseña actual es incorrecta'
            }, status=400)

        # Validar contraseña (al menos 8 caracteres, una mayuscula y un numero)        
        if len(new_password) < 8 or not re.search(r'[A-Z]', new_password) or not re.search(r'[0-9]', new_password):
            return Response({
                'error': 'La contraseña nueva debe tener al menos 8 caracteres, una letra mayúscula y un número.'
            }, status=400)

        # Cambiar la contraseña
        user.set_password(new_password)
        user.save()

        return Response({
            'message': 'Contraseña actualizada correctamente'
        })
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=400)

@api_view(['POST'])
def registrar_cliente(request):
    data = request.data
    error = ""
    # Validar campos obligatorios
    required_fields = ['username', 'password', 'email', 'dni', 'cuil', 'nombre', 'apellido', 'fecha_nacimiento']
    for field in required_fields:
        if not data.get(field):
            error += f'El campo {field} es obligatorio.\n'

    # Crear usuario con contraseña encriptada
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Validar contraseña (al menos 8 caracteres, una mayuscula y un numero)        
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
        error += 'La contraseña debe tener al menos 8 caracteres, una letra mayúscula y un número.\n'
   
    # Validar existencia del username
    if User.objects.filter(username=username).exists():
        error += 'El nombre de usuario ya está en uso.\n'
    
    # Validar existencia del email
    if User.objects.filter(email=email).exists():
        if email!='':
            error += 'El correo electrónico ya está en uso.\n'
        
    # Crear la instancia de Persona
    dni = data.get('dni')
        
    cuil = data.get('cuil')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fecha_nacimiento_str = data.get('fecha_nacimiento')
        
    # Validar existencia del DNI y CUIL
    if Persona.objects.filter_by_dni(dni).exists():
        error += 'El DNI ya está registrado.\n'

    if Persona.objects.filter_by_cuil(cuil).exists():
        error += 'El CUIL ya está registrado.\n'
    
    # Validar que el CUIL contenga el DNI
    if dni not in cuil:
        error += 'El CUIL debe contener el DNI.\n'

    # Validar edad mayor o igual a 18
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        edad = (datetime.today().date() - fecha_nacimiento).days // 365
        if edad < 18:
            error += 'Debe ser mayor de 18 años para registrarse.\n'
    except ValueError:
        error += 'Formato de fecha de nacimiento inválido. Debe ser YYYY-MM-DD.\n'

    if(error!=""):
        return JsonResponse({'error': error}, status=400)

    try:
        # Crear el usuario
        user = User.objects.create(
            username=username,
            password=make_password(password),  # Hash de la contraseña
            email=email
        )
        # Crear la instancia de Cliente extendiendo la Persona
        cliente = Cliente.objects.create(
            _user=user,
            _dni=dni,
            _cuil=cuil,
            _nombre=nombre,
            _apellido=apellido,
            _fecha_nacimiento=fecha_nacimiento,
        )
        return JsonResponse({'message': '¡Ha registrado su Usuario!.'}, status=201)
    except Exception as e:
        # Captura de cualquier excepción y respuesta de error
        return JsonResponse({'error': str(e)}, status=400)

# Función para obtener el próximo día de la semana
def obtener_proximo_dia(fecha_actual, dia_semana):
    dias_hasta_dia_semana = (dia_semana - fecha_actual.weekday()) % 7
    proximo_dia = fecha_actual + timedelta(days=dias_hasta_dia_semana)
    return proximo_dia

def obtener_fiestas_por_dia(fecha, dia):
    """
    Función para obtener las fiestas de un día específico y agregar las mesas y entradas relacionadas.
    """
    # Obtener el próximo día solicitado
    fecha_dia = obtener_proximo_dia(fecha, dia)

    # Obtener fiestas para la fecha especificada
    fiestas = Fiesta.objects.filter_by_fecha(fecha_dia)

    # Estructura de datos para almacenar la información de cada fiesta, incluyendo mesas y entradas
    fiestas_con_detalles = []
    
    for fiesta in fiestas:
        # Obtener mesas y entradas asociadas a la fiesta actual
        mesas = Mesa.objects.filter_by_fiesta(fiesta)
        entradas = Entrada.objects.filter_by_fiesta(fiesta)
        
        # Formatear las mesas y entradas para la respuesta
        mesas_detalles = []
        for mesa in mesas:
            mesa_tiene_articulo = MesaTieneArticulo.objects.filter_by_mesa(mesa)

            bebidas = "Incluye:"
            for instancia in mesa_tiene_articulo:
                bebidas += f"\n{instancia.cantidad} {instancia.articulo}"

            mesas_detalles.append({
                'id': mesa.pk,
                'categoria': mesa.categoria,
                'capacidad': mesa.capacidad,
                'precio': mesa.precio,
                'disponibilidad': mesa.disponibilidad,
                'posicion': {'top': mesa.top, 'left': mesa.left},
                'color': mesa.color,
                'numero': mesa.numero,
                'bebidas': bebidas
            })

        entradas_detalles = [
            {
                'id': entrada.pk,
                'categoria': entrada.categoria,
                'precio_unitario': entrada.precio_unitario
            }
            for entrada in entradas
        ]

        # Agregar la fiesta junto con sus mesas y entradas a la lista de detalles
        fiestas_con_detalles.append({
            'id': fiesta.pk, 
            'fecha': fiesta.fecha,
            'nombre': fiesta.nombre,
            'descripcion': fiesta.descripcion,
            'edad_minima': fiesta.edad_minima,
            'edad_maxima': fiesta.edad_maxima,
            'latitud': fiesta.latitud,
            'longitud': fiesta.longitud,
            'cantidad_entrada_vip': fiesta.cantidad_entrada_vip,
            'cantidad_entrada_popular': fiesta.cantidad_entrada_popular,
            'categoria': fiesta.categoria,
            'vestimenta': fiesta.vestimenta,
            'mesas': mesas_detalles,
            'entradas': entradas_detalles
        })
    
    return fiestas_con_detalles

def obtener_productos_y_tragos_con_stock():
    # Filtrar productos y tragos con stock mayor a 0
    productos = Producto.objects.filter_by_stock_positive()
    tragos = Trago.objects.filter_by_stock_positive()

    productos_json = [
        {
            'id': producto.pk,
            'nombre': producto.nombre, 
            'volumen': producto.volumen, 
            'precio_unitario': producto.precio_unitario, 
            'stock': producto.stock, 
            'marca': producto.marca.nombre,
        }
        for producto in productos
    ]

    tragos_json = [
        {
            'id': trago.pk,
            'nombre': trago.nombre, 
            'volumen': trago.volumen, 
            'precio_unitario': trago.precio_unitario, 
            'stock': trago.stock, 
            'tipo': trago.tipo,
        }
        for trago in tragos
    ]

    return {
        'productos': productos_json,
        'tragos': tragos_json
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        try:
            persona = Cliente.objects.filter_by_user(user).first()
            fecha_actual = datetime.today()

            # Obtener estadísticas del cliente
            stats = get_cliente_stats(persona.pk)
            
            # Obtener las fiestas de viernes y sábado
            fiestas_viernes = obtener_fiestas_por_dia(fecha_actual, 4) #viernes
            fiestas_sabado = obtener_fiestas_por_dia(fecha_actual, 5) #sabado

            # Obtener productos y tragos con stock mayor a 0
            stock_data = obtener_productos_y_tragos_con_stock()

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': f'{persona.nombre} {persona.apellido} ({username})',
                'user': {
                    'id': user.pk,
                    'username': user.username,
                    'email': user.email,
                },
                'cliente': {
                    'id': persona.pk,
                    'nombre': persona.nombre,
                    'apellido': persona.apellido,
                    'dni': persona.dni,
                    'cuil': persona.cuil,
                    'fecha_nacimiento': persona.fecha_nacimiento,
                    # Agregar las estadísticas al objeto cliente
                    'total_reservaciones': stats['total_reservaciones'],
                    'racha_actual': stats['racha_actual'],
                    'total_productos': stats['total_productos'],
                    'total_entradas': stats['total_entradas']
                },
                'fiestas_viernes': fiestas_viernes,
                'fiestas_sabado': fiestas_sabado,
                'productos': stock_data['productos'],
                'tragos': stock_data['tragos'],
            })
        except Exception:
            return Response({'error': 'Credenciales no válidas'}, status=400)
    else:
        return Response({'error': 'Credenciales no válidas'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def refresh_data(request):
    user = request.user
    cliente = Cliente.objects.get(_user=user)
    fecha_actual = datetime.today()
    
    # Obtener las fiestas de viernes y sábado
    fiestas_viernes = obtener_fiestas_por_dia(fecha_actual, 4) #viernes
    fiestas_sabado = obtener_fiestas_por_dia(fecha_actual, 5) #sabado

    # Obtener estadísticas del cliente
    stats = get_cliente_stats(cliente.id)

    # Obtener productos y tragos con stock mayor a 0
    stock_data = obtener_productos_y_tragos_con_stock()

    try:
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'cliente': {
                'id': cliente.id,
                'nombre': cliente.nombre,
                'apellido': cliente.apellido,
                'dni': cliente.dni,
                'cuil': cliente.cuil,
                'fecha_nacimiento': cliente.fecha_nacimiento,
                # Agregar las estadísticas al objeto cliente
                'total_reservaciones': stats['total_reservaciones'],
                'racha_actual': stats['racha_actual'],
                'total_productos': stats['total_productos'],
                'total_entradas': stats['total_entradas']
            },
            'fiestas_viernes': fiestas_viernes,
            'fiestas_sabado': fiestas_sabado,
            'productos': stock_data['productos'],
            'tragos': stock_data['tragos'],
        })
    except Exception:
        return Response({'error': 'Vuelva a iniciar sesión'}, status=400)

