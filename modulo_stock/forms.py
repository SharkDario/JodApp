from django import forms
from .models import Trago
from unfold.admin import UnfoldAdminTextInputWidget

class TragoAdminForm(forms.ModelForm):

    class Meta:
        model = Trago
        fields = '__all__'
        widgets = {
            '_volumen': UnfoldAdminTextInputWidget(attrs={'readonly': 'readonly'}),
            '_stock': UnfoldAdminTextInputWidget(attrs={'readonly': 'readonly'}),
        }