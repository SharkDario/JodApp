from django import forms
from .models import Trago

class TragoAdminForm(forms.ModelForm):

    class Meta:
        model = Trago
        fields = '__all__'
        widgets = {
            '_volumen': forms.TextInput(attrs={'readonly': 'readonly'}),
            '_stock': forms.TextInput(attrs={'readonly': 'readonly'}),
        }