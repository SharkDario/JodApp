# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import Mesa
import json

def mapa_mesas_view(request):
    return render(request, 'mapa_mesas.html')  # Nombre del archivo HTML

def save_mesa_position(request, mesa_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        top = data.get('top')
        left = data.get('left')
        print(f"Top: {top}, Left: {left}")  # Log para verificar valores

        try:
            mesa = Mesa.objects.get(id=mesa_id)
            mesa.top = top
            mesa.left = left
            mesa.save()
            return JsonResponse({'status': 'success'})
        except Mesa.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Mesa no encontrada'})

