# Create your views here.
from django.shortcuts import render, redirect
from .models import Contratacion, Empleado
from .forms import EmpleadoForm

def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            # Obtener el administrador que está creando el empleado
            administrador = request.user.empleado.administrador

            # Guardar el empleado
            empleado = form.save(commit=False)
            empleado.save()

            # Crear la contratación
            Contratacion.objects.create(
                administrador=administrador,
                empleado=empleado,
                fecha_contratacion=form.cleaned_data['fecha_contratacion']
            )

            return redirect('empleado_detalle', pk=empleado.pk)
    else:
        form = EmpleadoForm()

    return render(request, 'empleado_form.html', {'form': form})
