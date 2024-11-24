function validarFormulario() {
    const fecha = document.querySelector('input[name="fecha"]').value;
    const residente = document.querySelector('select[name="residente"]').value;
    const descripcion = document.querySelector('textarea[name="descripcion"]').value;
    const mensajeError = document.getElementById('mensaje-error');

    // Limpiar mensajes previos
    if (mensajeError) {
        mensajeError.innerHTML = '';
        mensajeError.style.display = 'none';
    }

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

    // Validar residente
    if (!residente) {
        mostrarError("Debe seleccionar un residente.");
    }

    // Validar descripción
    if (descripcion.length < 10) {
        mostrarError("La descripción debe contener al menos 10 caracteres.");
    }

    return valido; 
}

document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function (event) {
        if (!validarFormulario()) {
            event.preventDefault(); 
        }
    });
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
  