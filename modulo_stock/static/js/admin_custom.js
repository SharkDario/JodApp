document.addEventListener('DOMContentLoaded', function() {
    // Selecciona todos los campos de stock
    const quantityFields = document.querySelectorAll('.field-_stock input[type="number"]');
  
    quantityFields.forEach(function(field) {
      // Crea el contenedor de los botones
      const buttonGroup = document.createElement('div');
      buttonGroup.classList.add('button-group');
  
      // Crea el botón de disminuir
      const decreaseButton = document.createElement('button');
      decreaseButton.textContent = '-';
      decreaseButton.type = 'button'; // Previene el envío del formulario
      decreaseButton.classList.add('quantity-btn');
      decreaseButton.addEventListener('click', function(e) {
        e.preventDefault(); // Previene cualquier acción por defecto
        const currentValue = parseInt(field.value) || 0;
        field.value = Math.max(currentValue - 1, 0);
      });
  
      // Crea el botón de aumentar
      const increaseButton = document.createElement('button');
      increaseButton.textContent = '+';
      increaseButton.type = 'button'; // Previene el envío del formulario
      increaseButton.classList.add('quantity-btn');
      increaseButton.addEventListener('click', function(e) {
        e.preventDefault(); // Previene cualquier acción por defecto
        const currentValue = parseInt(field.value) || 0;
        field.value = currentValue + 1;
      });
  
      // Agrega los botones al grupo
      buttonGroup.appendChild(decreaseButton);
      buttonGroup.appendChild(increaseButton);
  
      // Agrega el grupo de botones después del campo de entrada
      field.parentNode.insertBefore(buttonGroup, field.nextSibling);
    });
  });