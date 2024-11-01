// static/js/ticket_canje.js
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    const canjeButtons = document.querySelectorAll('.canjear-ticket');

    canjeButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const ticketId = this.dataset.ticketId;
            const tipo = this.dataset.tipo;
            const maxCantidad = parseInt(this.dataset.maxCantidad);

            const cantidad = prompt(`Ingrese cantidad a canjear (máximo ${maxCantidad}):`, '1');
            if (!cantidad) return;

            const cantidadNum = parseInt(cantidad);
            if (isNaN(cantidadNum) || cantidadNum <= 0 || cantidadNum > maxCantidad) {
                alert('Cantidad inválida');
                return;
            }

            try {
                // Crear el FormData para enviar los datos
                const formData = new FormData();
                formData.append('cantidad', cantidadNum);

                // Iniciar proceso de canje
                const response = await fetch(`../../iniciar-canje/${ticketId}/${tipo}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json',  // Añadir esta línea
                    },
                    body: JSON.stringify({ cantidad: cantidadNum })
                });

                if (!response.ok) {
                    const contentType = response.headers.get('content-type');
                    if (contentType && contentType.includes('application/json')) {
                        const data = await response.json();
                        throw new Error(data.error || 'Error en el proceso de canje');
                    } else {
                        throw new Error('Error en la respuesta del servidor');
                    }
                }

                const data = await response.json();

                if (data.success) {
                    alert(`Código de verificación: ${data.codigo}\nPida al cliente que confirme este código en su app`);

                    // Esperar la confirmación del código
                    const codigoConfirmacion = prompt('Ingrese el código que el cliente ve en su app:');
                    if (!codigoConfirmacion) return;

                    // Enviar confirmación
                    const confirmFormData = new FormData();
                    confirmFormData.append('codigo', codigoConfirmacion);

                    const confirmResponse = await fetch(`../../confirmar-canje/${ticketId}/${tipo}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                            'Content-Type': 'application/json',  // Añadir esta línea
                        },
                        body: JSON.stringify({ codigo: codigoConfirmacion })  // Cambiar esto
                    });

                    if (!confirmResponse.ok) {
                        const confirmData = await confirmResponse.json();
                        throw new Error(confirmData.error || 'Error en la confirmación del canje');
                    }

                    const confirmData = await confirmResponse.json();

                    if (confirmData.success) {
                        alert('¡Canje confirmado exitosamente!');
                        location.reload();
                    } else {
                        alert(confirmData.error || 'Error en la confirmación del canje');
                    }
                }
            } catch (error) {
                alert(error.message || 'Error al procesar el canje');
                console.error('Error:', error);
            }
        });
    });
});

/*
document.addEventListener('DOMContentLoaded', function() {
    const canjeButtons = document.querySelectorAll('.canjear-ticket');
    
    canjeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const ticketId = this.dataset.ticketId;
            const tipo = this.dataset.tipo;
            const maxCantidad = parseInt(this.dataset.maxCantidad);
            
            // Mostrar modal de canje
            const cantidad = prompt(`Ingrese cantidad a canjear (máximo ${maxCantidad}):`, '1');
            if (!cantidad) return;
            
            // Validar cantidad
            const cantidadNum = parseInt(cantidad);
            if (isNaN(cantidadNum) || cantidadNum <= 0 || cantidadNum > maxCantidad) {
                alert('Cantidad inválida');
                return;
            }
            
            // Iniciar proceso de canje
            fetch(`/admin/iniciar-canje/${ticketId}/${tipo}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ cantidad: cantidadNum })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Mostrar código al empleado
                    alert(`Código de verificación: ${data.codigo}\nPida al cliente que confirme este código en su app`);
                    
                    // Esperar confirmación del cliente
                    const interval = setInterval(() => {
                        fetch(`/admin/verificar-estado-canje/${ticketId}/${tipo}/`)
                        .then(response => response.json())
                        .then(statusData => {
                            if (statusData.confirmado) {
                                clearInterval(interval);
                                alert('¡Canje confirmado exitosamente!');
                                location.reload();  // Recargar para actualizar cantidades
                            }
                        });
                    }, 5000);  // Verificar cada 5 segundos
                } else {
                    alert(data.error);
                }
            })
            .catch(error => {
                alert('Error al procesar el canje');
                console.error(error);
            });
        });
    });
});*/