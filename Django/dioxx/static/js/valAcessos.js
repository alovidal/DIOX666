/*  */

function validarFormulario() {
    const fecha = document.querySelector('input[name="fecha"]').value;
    const tipo = document.querySelector('select[name="tipo"]').value;
    const rut = document.querySelector('input[name="personaRut"]').value;
    const nombre = document.querySelector('input[name="personaNombre"]').value;
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

    // Validar fecha
    if (!fecha) {
        mostrarError("Debe seleccionar una fecha.");
    }

    // Validar tipo
    if (!tipo || tipo === "") {
        mostrarError("Debe seleccionar un tipo de acceso (Entrada o Salida).");
    }

    // Validar rut (debe tener un formato válido)
    if (!validarRut(rut)) {
        mostrarError("El rut ingresado no es válido. Use el formato sin puntos y con guion.");
    }

    // Validar nombre (mínimo 3 caracteres y sin números)
    if (nombre.length < 3 || !/^[a-zA-Z\s]+$/.test(nombre)) {
        mostrarError("El nombre debe contener al menos 3 caracteres y solo letras.");
    }

    return valido; 
}

// Validar rut
function validarRut(rut) {
    const regex = /^\d{7,8}-[kK\d]$/;
    return regex.test(rut);
}

document.querySelector('form').addEventListener('submit', function (event) {
    if (!validarFormulario()) {
        event.preventDefault(); 
    }
});

/* Modal de confirmación */
document.addEventListener("DOMContentLoaded", function () {
    const deleteButton = document.getElementById("delete-button");
    const confirmModal = document.getElementById("confirm-modal");
    const cancelButton = document.getElementById("cancel-button");
    const confirmButton = document.getElementById("confirm-button");
    const deleteForm = document.getElementById("delete-form");
  
    // Mostrar modal al hacer clic en "Eliminar"
    deleteButton.addEventListener("click", function () {
      confirmModal.style.display = "flex";
    });
  
    // Cerrar modal al hacer clic en "Cancelar"
    cancelButton.addEventListener("click", function () {
      confirmModal.style.display = "none";
    });
  
    // Confirmar eliminación y enviar el formulario
    confirmButton.addEventListener("click", function () {
      deleteForm.submit();
    });
  });
  