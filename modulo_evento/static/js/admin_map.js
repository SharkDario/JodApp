document.addEventListener('DOMContentLoaded', function() {
    var latField = document.getElementById('id_latitud');
    var lngField = document.getElementById('id_longitud');

    // Inicializar el mapa
    var map = new Microsoft.Maps.Map('#map', {
        center: new Microsoft.Maps.Location(latField.value || -26.1855, lngField.value || -58.1739),
        zoom: 10
    });

    // Agregar un marcador en la posición inicial
    var marker = new Microsoft.Maps.Pushpin(map.getCenter(), { draggable: true });
    map.entities.push(marker);

    // Actualizar las coordenadas al mover el marcador
    Microsoft.Maps.Events.addHandler(marker, 'dragend', function(e) {
        var location = marker.getLocation();
        latField.value = location.latitude.toFixed(4);
        lngField.value = location.longitude.toFixed(4);
    });

    // Actualizar la posición del marcador al hacer clic en el mapa
    Microsoft.Maps.Events.addHandler(map, 'click', function(e) {
        if (e.location) {
            marker.setLocation(e.location);
            latField.value = e.location.latitude.toFixed(4);
            lngField.value = e.location.longitude.toFixed(4);
        }
    });

    // Mover las Cards
    document.addEventListener('DOMContentLoaded', () => {
        let newX = 0, newY = 0, startX = 0, startY = 0;
  
        const card = document.getElementById('card');
  
        card.addEventListener('mousedown', mouseDown);
  
        function mouseDown(e) {
            startX = e.clientX;
            startY = e.clientY;
  
            document.addEventListener('mousemove', mouseMove);
            document.addEventListener('mouseup', mouseUp);
        }
  
        function mouseMove(e) {
            newX = startX - e.clientX;
            newY = startY - e.clientY;
            
            startX = e.clientX;
            startY = e.clientY;
  
            card.style.top = (card.offsetTop - newY) + 'px';
            card.style.left = (card.offsetLeft - newX) + 'px';
        }
  
        function mouseUp(e) {
            document.removeEventListener('mousemove', mouseMove);
        }
      });

    // Draggable mesas (assuming you have elements with class 'mesa')
  document.querySelectorAll('.mesa').forEach(mesa => {
    mesa.setAttribute('draggable', true);

    mesa.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', e.target.id);
    });

    document.getElementById('map_mesas').addEventListener('dragover', (e) => {
      e.preventDefault();
    });

    document.getElementById('map_mesas').addEventListener('drop', (e) => {
      e.preventDefault();
      const id = e.dataTransfer.getData('text');
      const mesa = document.getElementById(id);
      const rect = e.target.getBoundingClientRect();
      mesa.style.top = `${e.clientY - rect.top - mesa.offsetHeight / 2}px`;
      mesa.style.left = `${e.clientX - rect.left - mesa.offsetWidth / 2}px`;

      // Update position in hidden form (replace with your actual logic)
      document.getElementById(`id_${id}_top`).value = parseInt(mesa.style.top);
      document.getElementById(`id_${id}_left`).value = parseInt(mesa.style.left);
    });
  });
});