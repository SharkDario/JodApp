// static/admin/js/date_filter.js

window.addEventListener('load', function() {
    const dateInputs = document.querySelectorAll('.rangefilter-wrapper input[type="date"]');
    
    dateInputs.forEach(input => {
        input.style.backgroundColor = "#f0f0f0";  // Cambia el color de fondo
        input.style.border = "1px solid #ccc";   // Cambia el borde
    });

    const calendarButtons = document.querySelectorAll('.rangefilter-datepicker');
    
    calendarButtons.forEach(button => {
        button.style.backgroundColor = "#007bff"; // Ajusta el color de los botones de calendario
        button.style.border = "none";
        button.style.color = "white";
    });
});

/*document.addEventListener('DOMContentLoaded', function() {
    const startDate = document.getElementById('start_date');
    const endDate = document.getElementById('end_date');

    if (startDate && endDate) {
        startDate.addEventListener('change', function() {
            endDate.min = this.value;
        });

        endDate.addEventListener('change', function() {
            startDate.max = this.value;
        });
    }
});*/