from django import forms
from .models import Fiesta, Entrada, Mesa, Entrada
from unfold.admin import UnfoldAdminIntegerFieldWidget

class FiestaForm(forms.ModelForm):

    class Meta:
        model = Fiesta
        fields = '__all__'
        widgets = {
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
        }
    
    
class MesaForm(forms.ModelForm):
    
    class Meta:
        model = Mesa
        fields = '__all__'
        widgets = {
            '_top': forms.HiddenInput(),
            '_left': forms.HiddenInput(),
        }

class EntradaInlineForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ['_categoria', '_precio_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es la primera instancia del inline, establecer categoría "Popular"
        if not self.instance.pk and self.prefix.endswith('-0'):
            self.fields['_categoria'].initial = 'Popular'
            self.fields['_categoria'].disabled = True
        # Si es la segunda instancia del inline, establecer categoría "VIP"
        elif not self.instance.pk and self.prefix.endswith('-1'):
            self.fields['_categoria'].initial = 'VIP'
            self.fields['_categoria'].disabled = True
        # Para las entradas existentes, deshabilitar el campo de categoría
        else:
            self.fields['_categoria'].disabled = True