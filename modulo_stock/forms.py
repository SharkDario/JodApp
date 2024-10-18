from django import forms
from .models import Trago, RemitoProveedor, Persona, Empleado
from unfold.admin import UnfoldAdminTextInputWidget

class TragoAdminForm(forms.ModelForm):

    class Meta:
        model = Trago
        fields = '__all__'
        widgets = {
            '_volumen': UnfoldAdminTextInputWidget(attrs={'readonly': 'readonly'}),
            '_stock': UnfoldAdminTextInputWidget(attrs={'readonly': 'readonly'}),
        }

class RemitoAdminForm(forms.ModelForm):

    class Meta:
        model = RemitoProveedor
        fields = '__all__'
        widgets = {
            '_empleado': UnfoldAdminTextInputWidget(attrs={'readonly': 'readonly'}),
        }
    
    def __init__(self, *args, **kwargs):
        # Obtén el request desde los kwargs
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        user = getattr(self.request, 'auth_user')
        try:
            persona = Persona.objects.get(_user=user)
            empleado = Empleado.objects.get(pk=persona.pk)  # Obtener el Empleado asociado
            self.fields['_empleado'].initial = empleado  # Asignar el empleado
        except (Persona.DoesNotExist, Empleado.DoesNotExist):
            pass  # Si no se encuentra la persona o el empleado, no hacer nada

        self.fields['_empleado'].disabled = True  # Hacer el campo solo lectura