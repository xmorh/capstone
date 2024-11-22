    document.addEventListener('DOMContentLoaded', function () {
        var calendarEl = document.getElementById('calendar');

        var disabledDays = ['2024-11-23', '2024-11-25'];

        function agregarDiasDeshabilitados(eventos) {
            eventos.forEach(evento => {
                const fechaEvento = new Date(evento.start).toISOString().split('T')[0];
                if (!evento.horasDisponibles) { // Suponiendo que "horasDisponibles" indica disponibilidad
                    disabledDays.push(fechaEvento);
                }
            });
        }

        var calendar = new FullCalendar.Calendar(calendarEl, {
            locale: 'es', // Configurar el idioma a español
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridDay'
            },
            initialDate: '2024-11-01', // Fecha inicial del calendario
            navLinks: true, // Habilita la navegación por día/semana al hacer clic
            businessHours: true, // Horarios laborales predeterminados
            editable: false, // Permitir mover eventos (opcional)
            selectable: true, // Permite seleccionar fechas/horarios
            
            // Función para obtener eventos desde el backend
            events: function (fetchInfo, successCallback, failureCallback) {
                fetch('/obtener_eventos/') // Cambia la URL si es necesario
                    .then(response => response.json())
                    .then(data => {
                        agregarDiasDeshabilitados(data); // Actualizar días deshabilitados
                        successCallback(data); // Pasar eventos al calendario
                    })
                    .catch(error => {
                        console.error('Error al obtener eventos:', error);
                        failureCallback(error); // Llamar a failureCallback en caso de error
                    });
            },

            // Al seleccionar un rango de tiempo en el calendario
            select: function (info) {
                const fechaInicioISO = info.startStr; // Fecha y hora de inicio
                const fechaFinISO = info.endStr; // Fecha y hora de fin
                const id_servicio = 12; // ID del servicio (puedes obtenerlo dinámicamente)
                const id_manicurista = 27; // ID del manicurista (puedes obtenerlo dinámicamente)

                const confirmar = confirm(`¿Deseas reservar este horario? (${fechaInicioISO} - ${fechaFinISO})`);
                if (confirmar) {
                    crearReserva(id_servicio, fechaInicioISO, fechaFinISO, id_manicurista);
                }

                calendar.unselect(); // Deshabilitar la selección de la zona del calendario después de hacer la reserva
            },

            // Clic en una fecha
            dateClick: function (info) {
                if (disabledDays.includes(info.dateStr)) {
                    console.log('Este día está deshabilitado:', info.dateStr);
                    return; // Salir si el día está deshabilitado
                }

                console.log('Fecha seleccionada:', info.dateStr);
            },

            datesSet: function (info) {
                console.log("Mostrando eventos para el rango:", info.startStr, "a", info.endStr);
                // Aplicar estilos a los días deshabilitados
                disabledDays.forEach(date => {
                    let dayCell = document.querySelector(`[data-date="${date}"]`);
                    if (dayCell) {
                        dayCell.classList.add('fc-disabled-day');
                    }
                });
            }
        });

        // Función para crear la reserva en el servidor
        function crearReserva(id_servicio, fechaInicio, fechaFin, id_manicurista) {
            fetch('/crear_reserva/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id_servicio: id_servicio,
                    fecha_inicio: fechaInicio,
                    fecha_fin: fechaFin,
                    id_manicurista: id_manicurista,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Reserva creada correctamente.');
                        calendar.refetchEvents(); // Recargar eventos después de guardar la reserva
                    } else {
                        alert('Error al crear la reserva: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error al crear la reserva:', error);
                    alert('Hubo un error al crear la reserva.');
                });
        }

        calendar.render(); // Renderiza el calendario en el DOM
    });
