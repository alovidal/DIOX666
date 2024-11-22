function validarFormularioEventos() {
    const titulo = document.querySelector('input[name="titulo"]').value.trim();
    const fechaInicio = document.querySelector('input[name="fecha_inicio"]').value;
    const fechaFin = document.querySelector('input[name="fecha_fin"]').value;
    const descripcion = document.querySelector('textarea[name="descripcion"]').value.trim();
    const mensajeError = document.getElementById('mensaje-error');

    // Limpiar mensajes previos
    mensajeError.innerHTML = '';
    mensajeError.style.display = 'none';

    let valido = true;

    // Función para mostrar errores
    function mostrarError(mensaje) {
        const errorParrafo = document.createElement('p');
        errorParrafo.textContent = mensaje;
        errorParrafo.classList.add('error-text');
        mensajeError.appendChild(errorParrafo);
        mensajeError.style.display = 'block';
        valido = false;
    }

    // Validar título (mínimo 3 caracteres)
    if (titulo.length < 3) {
        mostrarError("El título debe contener al menos 3 caracteres.");
    }

    // Validar fechas
    if (!fechaInicio) {
        mostrarError("Debe seleccionar una fecha de inicio.");
    }
    if (!fechaFin) {
        mostrarError("Debe seleccionar una fecha de fin.");
    }
    if (fechaInicio && fechaFin) {
        const inicio = new Date(fechaInicio);
        const fin = new Date(fechaFin);
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);  // Aseguramos que solo compare las fechas sin horas

        // Validación de la fecha de inicio (debe ser igual o mayor a la fecha actual)
        if (inicio < hoy) {
            mostrarError("La fecha de inicio no puede ser menor a la fecha actual.");
        }

        // Validación de la fecha de fin (debe ser igual o mayor a la fecha actual)
        if (fin < hoy) {
            mostrarError("La fecha de término debe ser hoy o posterior.");
        }

        // Validar que la fecha de inicio sea anterior a la fecha de fin
        if (inicio >= fin) {
            mostrarError("La fecha de inicio debe ser anterior a la fecha de fin.");
        }
    }

    // Validar descripción (mínimo 10 caracteres)
    if (descripcion.length < 10) {
        mostrarError("La descripción debe contener al menos 10 caracteres.");
    }

    return valido;
}

document.querySelector('form').addEventListener('submit', function (event) {
    if (!validarFormularioEventos()) {
        event.preventDefault(); 
    }
});


// Modal de confirmación para eliminación
document.addEventListener("DOMContentLoaded", function () {
    const deleteButton = document.getElementById("delete-button");
    const confirmModal = document.getElementById("confirm-modal");
    const cancelButton = document.getElementById("cancel-button");
    const confirmButton = document.getElementById("confirm-button");
    const deleteForm = document.getElementById("delete-form");

    // Mostrar el modal al hacer clic en "Eliminar Evento"
    deleteButton.addEventListener("click", function () {
        confirmModal.style.display = "flex";
    });

    // Cerrar el modal al hacer clic en "Cancelar"
    cancelButton.addEventListener("click", function () {
        confirmModal.style.display = "none";
    });

    // Confirmar eliminación y enviar el formulario
    confirmButton.addEventListener("click", function () {
        deleteForm.submit();
    });
});
