document.addEventListener('DOMContentLoaded', function() {
    function updatePrecioTotal() {
        let total = 0;
        // Suma los subtotales de DetalleArticulo
        document.querySelectorAll('#detallearticulo_set-group input[id$="subtotal"]').forEach(function(input) {
            total += parseFloat(input.value) || 0;
        });
        // Suma los subtotales de DetalleEntrada
        document.querySelectorAll('#detalleentrada_set-group input[id$="subtotal"]').forEach(function(input) {
            total += parseFloat(input.value) || 0;
        });
        // Suma los subtotales de DetalleReservacion
        document.querySelectorAll('#detallereservacion_set-group input[id$="subtotal"]').forEach(function(input) {
            total += parseFloat(input.value) || 0;
        });
        // Actualiza el campo _precio_total
        let precioTotalInput = document.querySelector('#id__precio_total');
        if (precioTotalInput) {
            precioTotalInput.value = total.toFixed(2);
        } else {
            console.warn('No se encontró el campo de precio total');
        }
    }

    function updateSubtotal(row) {
        const cantidadInput = row.querySelector('input[id$="cantidad"]');
        const precioUnitarioInput = row.querySelector('input[id$="precio_unitario"]');
        const subtotalInput = row.querySelector('input[id$="subtotal"]');
        if (cantidadInput && precioUnitarioInput && subtotalInput) {
            const cantidad = parseFloat(cantidadInput.value) || 0;
            const precioUnitario = parseFloat(precioUnitarioInput.value) || 0;
            const subtotal = cantidad * precioUnitario;
            subtotalInput.value = subtotal.toFixed(2);
            updatePrecioTotal(); // Update total immediately after updating subtotal
        }
    }

    function addEventListeners() {
        const rows = document.querySelectorAll('.dynamic-detallearticulo_set, .dynamic-detalleentrada_set, .dynamic-detallereservacion_set');
        rows.forEach(row => {
            const inputs = row.querySelectorAll('input[id$="cantidad"], input[id$="precio_unitario"]');
            inputs.forEach(input => {
                input.addEventListener('input', function() {
                    updateSubtotal(row);
                });
            });
        });
    }

    // Initial event listeners
    addEventListeners();

    // Observe DOM changes for dynamically added rows
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                addEventListeners();
            }
        });
    });

    const config = { childList: true, subtree: true };
    const targetNode = document.querySelector('#factura-cliente-form');
    if (targetNode) {
        observer.observe(targetNode, config);
    } else {
        console.warn('No se encontró el elemento #factura-cliente-form');
    }

    // Update total when page loads
    updatePrecioTotal();

    // Add event listener for the add-row button
    document.querySelectorAll('.add-row a').forEach(button => {
        button.addEventListener('click', function() {
            setTimeout(addEventListeners, 100);
        });
    });
});
