from django import forms
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    fecha_contratacion = forms.DateField(required=True, label="Fecha de Contratación", widget=forms.SelectDateWidget)

    class Meta:
        model = Empleado
        fields = ['dni', 'cuil', 'nombre', 'apellido', 'fecha_nacimiento', 'zona_asignada', 'sueldo', 'estado', 'telefono', 'seniority', 'annos_experiencia', 'fecha_inicio', 'rol', 'fecha_contratacion']
