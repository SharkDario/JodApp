// detalle_articulo.js

// Espera a que el documento esté completamente cargado

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

    // Función para actualizar el subtotal basado en cantidad y precio unitario
    function updateSubtotal(inputElement) {
        const row = inputElement.closest('.form-row'); // Encuentra la fila del formulario actual
        const cantidadInput = row.querySelector('input[id$="cantidad"]');
        const precioUnitarioInput = row.querySelector('input[id$="precio_unitario"]');
        const subtotalInput = row.querySelector('input[id$="subtotal"]');

        const cantidad = parseFloat(cantidadInput.value) || 0;
        const precioUnitario = parseFloat(precioUnitarioInput.value) || 0;

        // Calcular el subtotal
        const subtotal = cantidad * precioUnitario;

        // Actualizar el campo subtotal
        subtotalInput.value = subtotal.toFixed(2);
        updatePrecioTotal();
    }

    function addEventListeners() {
        document.querySelectorAll('.select-articulo, input[id$="cantidad"], input[id$="precio_unitario"]').forEach(element => {
            element.removeEventListener('change', updateEventHandler); // Avoid duplicate listeners
            element.addEventListener('change', updateEventHandler);
        });
        document.querySelectorAll('input[id$="cantidad"], input[id$="precio_unitario"]').forEach(element => {
            element.removeEventListener('input', updateSubtotalEvent); // Evitar duplicar listeners
            element.addEventListener('input', updateSubtotalEvent);
            element.removeEventListener('change', updateSubtotalEvent);
            element.addEventListener('change', updateSubtotalEvent);
        });
    }

    function updateSubtotalEvent(event) {
        updateSubtotal(event.target);
    }

    function updateEventHandler(event) {
        updatePrecioUnitario(event.target);
        updateSubtotal(event.target);
    }

    addEventListeners();

    document.addEventListener('click', function(event) {
        if (event.target && event.target.matches('.add-row a')) {
            setTimeout(addEventListeners, 0); // Delay to ensure DOM updates
        }
    });

    // Función para actualizar el precio unitario basado en el artículo seleccionado
    function updatePrecioUnitario(selectElement) {
        const row = selectElement.closest('.form-row'); // Encuentra la fila del formulario actual
        const precioUnitarioInput = row.querySelector('input[id$="precio_unitario"]');
        const articuloTexto = selectElement.options[selectElement.selectedIndex].text; // Obtener el texto del artículo seleccionado

        // Extraer el precio usando una expresión regular
        const precioMatch = articuloTexto.match(/\(Precio: (\d+(\.\d{1,2})?)\)/);

        if (precioMatch) {
            // Si la expresión regular encuentra el precio, lo extraemos
            const precio = parseFloat(precioMatch[1]);
            // Actualizar el precio unitario
            precioUnitarioInput.value = precio.toFixed(2);
            updateSubtotal(precioUnitarioInput); // Actualizar el subtotal automáticamente
        } else {
            console.warn('No se pudo extraer el precio del texto:', articuloTexto);
        }
    }

    // Capturar cambios en los selects de artículos y actualizar el precio unitario
    document.querySelectorAll('select[id$="articulo"]').forEach(function(selectElement) {
        selectElement.addEventListener('change', function() {
            updatePrecioUnitario(this);
        });
    });

    // Agregar los listeners para actualizar el subtotal cuando cambien cantidad o precio unitario
    addEventListeners();
});