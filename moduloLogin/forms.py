from django import forms
from .models import Empleado, Contratacion, Persona, User

class EmpleadoAdminForm(forms.ModelForm):
    email = forms.EmailField(label='Correo Electrónico', required=True)
    _annos_experiencia = forms.DecimalField(label="Años de experiencia", required=True)

    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            '_estado': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['_estado'].initial = "Inactivo"
        if self.instance.pk:
            # Cargar el email actual del usuario relacionado
            self.fields['email'].initial = self.instance.user.email
        # Filtrar los usuarios que ya están asociados a alguna persona
        #personas_asociadas = Persona.objects.values_list('_user', flat=True)
        #self.fields['_user'].queryset = User.objects.exclude(id__in=personas_asociadas)

    def save(self, commit=True):
        # Guardar el email en el objeto User relacionado
        user = self.instance.user
        user.email = self.cleaned_data['email']
        user.save()
        return super().save(commit=commit)
    

class ContratacionForm(forms.ModelForm):
    TIPO_CHOICES = [
        ('', 'Seleccione una opción'),
        ('Contratacion', 'Contratación'),
        ('Renovacion', 'Renovación'),
        ('Despido', 'Despido'),
    ]

    _tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=True)

    class Meta:
        model = Contratacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Obtener el valor de tipo ya sea del POST o de los datos iniciales del objeto
        tipo_seleccionado = self.data.get('_tipo') if '_tipo' in self.data else self.initial.get('_tipo')

        # Filtrar los empleados según el tipo seleccionado
        if tipo_seleccionado == 'Contratacion':
            self.fields['_empleado'].queryset = Empleado.objects.filter(_estado='Inactivo')
        elif tipo_seleccionado in ['Renovacion', 'Despido']:
            self.fields['_empleado'].queryset = Empleado.objects.filter(_estado='Activo')
        else:
            self.fields['_empleado'].queryset = Empleado.objects.none()  # Si no hay selección, vacío