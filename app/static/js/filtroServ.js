document.addEventListener('DOMContentLoaded', function () {
    const manicuristaSelect = document.getElementById('manicurista');
    const servicioSelect = document.getElementById('servicio');
    const opcionesServicios = Array.from(servicioSelect.options); // Guardar todas las opciones originales

    manicuristaSelect.addEventListener('change', function () {
        const manicuristaSeleccionado = this.value;

        // Limpiar el dropdown de servicios
        servicioSelect.innerHTML = '';

        // Filtrar servicios por manicurista seleccionado
        opcionesServicios.forEach(option => {
            if (option.dataset.manicurista === manicuristaSeleccionado) {
                servicioSelect.appendChild(option);
            }
        });

        // Si no hay servicios disponibles, agregar un mensaje
        if (servicioSelect.options.length === 0) {
            const noDisponible = document.createElement('option');
            noDisponible.textContent = 'No hay servicios disponibles';
            noDisponible.disabled = true;
            servicioSelect.appendChild(noDisponible);
        }
    });
});
