document.addEventListener('DOMContentLoaded', () => {
    let startX = 0, startY = 0, newX = 0, newY = 0, activeMesa = null;

    const container = document.getElementById('container');

    document.querySelectorAll('.mesa-card').forEach(card => {
        card.addEventListener('mousedown', (e) => {
            activeMesa = card;
            startX = e.clientX;
            startY = e.clientY;
            document.addEventListener('mousemove', mouseMove);
            document.addEventListener('mouseup', mouseUp);
        });
    });

    function mouseMove(e) {
        if (!activeMesa) return;

        newX = startX - e.clientX;
        newY = startY - e.clientY;

        startX = e.clientX;
        startY = e.clientY;

        let newTop = activeMesa.offsetTop - newY;
        let newLeft = activeMesa.offsetLeft - newX;

        const containerRect = container.getBoundingClientRect();
        const mesaRect = activeMesa.getBoundingClientRect();

        if (newTop < 0) newTop = 0;
        if (newLeft < 0) newLeft = 0;
        if (newTop + mesaRect.height > containerRect.height) {
            newTop = containerRect.height - mesaRect.height;
        }
        if (newLeft + mesaRect.width > containerRect.width) {
            newLeft = containerRect.width - mesaRect.width;
        }

        activeMesa.style.top = newTop + 'px';
        activeMesa.style.left = newLeft + 'px';
    }

    function mouseUp(e) {
        if (activeMesa) {
            savePosition(activeMesa.dataset.id, activeMesa.style.top, activeMesa.style.left);
        }
        document.removeEventListener('mousemove', mouseMove);
        activeMesa = null;
    }
    function savePosition(mesaId, top, left) {
        console.log(`Saving position for mesa ${mesaId}: Top: ${top}, Left: ${left}`);
        fetch(`/save_mesa_position/${mesaId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ top: parseInt(top), left: parseInt(left) })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Posición guardada');
            } else {
                console.error('Error al guardar la posición');
            }
        })
        .catch(error => console.error('Error en la solicitud:', error));
    }
    
});
