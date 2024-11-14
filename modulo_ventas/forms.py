from django import forms
from .models import DetalleArticulo, Articulo, DetalleEntrada, DetalleReservacion

class DetalleArticuloForm(forms.ModelForm):
    class Meta:
        model = DetalleArticulo
        fields = ['_articulo', '_precio_unitario', '_cantidad', '_subtotal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_subtotal'].disabled = True
        if '_articulo' in self.fields:
            # Personalizamos el widget para el campo 'articulo'
            self.fields['_articulo'].widget.attrs.update({'class': 'select-articulo'})

            # Modificar manualmente el 'widget.choices' para incluir 'data-precio'
            articulo_choices = []
            for articulo in self.fields['_articulo'].queryset:
                # Añadir el 'data-precio' a cada opción
                articulo_choices.append((articulo.id, f"{articulo.__str__()} (Precio: {articulo.precio_unitario})"))
            
            # Asignar las opciones personalizadas al widget
            self.fields['_articulo'].choices = articulo_choices

class DetalleEntradaForm(forms.ModelForm):
    class Meta:
        model = DetalleEntrada
        fields = ['_entrada', '_precio_unitario', '_cantidad', '_subtotal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_subtotal'].disabled = True
        if '_entrada' in self.fields:
            # Personalizamos el widget para el campo 'entrada'
            self.fields['_entrada'].widget.attrs.update({'class': 'select-entrada'})

            # Modificar manualmente el 'widget.choices' para incluir 'data-precio'
            entrada_choices = []
            for entrada in self.fields['_entrada'].queryset:
                # Añadir el 'data-precio' a cada opción
                entrada_choices.append((entrada.id, f"{entrada.__str__()} (Precio: {entrada.precio_unitario})"))
            
            # Asignar las opciones personalizadas al widget
            self.fields['_entrada'].choices = entrada_choices

class DetalleReservacionForm(forms.ModelForm):
    class Meta:
        model = DetalleReservacion
        fields = ['_reservacion', '_precio_unitario', '_cantidad', '_subtotal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_subtotal'].disabled = True
        self.fields['_cantidad'].disabled = True
        self.fields['_cantidad'].initial = 1

        if '_reservacion' in self.fields:
            # Personalizamos el widget para el campo 'reservacion'
            self.fields['_reservacion'].widget.attrs.update({'class': 'select-mesa'})

            # Modificar manualmente el 'widget.choices' para incluir 'data-precio'
            reservacion_choices = []
            for reservacion in self.fields['_reservacion'].queryset:
                # Añadir el 'data-precio' a cada opción
                #if(reservacion.disponibilidad=="Disponible"):
                reservacion_choices.append((reservacion.id, f"{reservacion.__str__()} (Precio: {reservacion.precio})"))
            
            # Asignar las opciones personalizadas al widget
            self.fields['_reservacion'].choices = reservacion_choices

"""class DetalleArticuloForm(forms.ModelForm):
    class Meta:
        model = DetalleArticulo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'articulo' in self.fields:
            # Añadir el precio unitario como atributo data-precio en cada opción del select
            self.fields['articulo'].queryset = Articulo.objects.all()
            for articulo in self.fields['articulo'].queryset:
                self.fields['articulo'].widget.choices.queryset = [
                    (articulo.id, f"{articulo.nombre} (Precio: {articulo.precio_unitario})", {'data-precio': articulo.precio_unitario})
                ]"""
