from django import forms
from .models import Fiesta, Entrada, Mesa
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