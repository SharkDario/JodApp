from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
# Create your views here.
from .models import MejoresClientes

class ClienteDetailView(DetailView):
    model = MejoresClientes
    template_name = 'tu_app/cliente_detail.html'

    def get_object(self):
        id = self.kwargs.get('id')
        fecha = self.kwargs.get('fecha')
        return get_object_or_404(MejoresClientes, id=id, _fecha_emision=fecha)

cliente_detail_view = ClienteDetailView.as_view()