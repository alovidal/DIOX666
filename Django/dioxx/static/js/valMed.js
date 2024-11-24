function validarFormulario() {
    const nombre = document.querySelector('input[name="nombre"]').value;
    const tipoDosis = document.querySelector('input[name="tipoDosis"]').value;
    const descripcion = document.querySelector('input[name="descripcion"]').value;
    const mensajeError = document.getElementById('mensaje-error');

    // Limpiar mensajes previos
    if (mensajeError) {
        mensajeError.innerHTML = '';
        mensajeError.style.display = 'none';
    }

    let valido = true;

    // Función para mostrar errores
    function mostrarError(mensaje) {
        if (mensajeError) {
            const errorParrafo = document.createElement('p');
            errorParrafo.textContent = mensaje;
            errorParrafo.classList.add('error-text'); 
            mensajeError.appendChild(errorParrafo);
            mensajeError.style.display = 'block';
        }
        valido = false;
    }

    // Validar nombre (mínimo 3 caracteres)
    if (nombre.length < 3) {
        mostrarError("El nombre debe contener al menos 3 caracteres.");
    }

    // Validar tipo de dosis (mínimo 3 caracteres)
    if (tipoDosis.length < 3) {
        mostrarError("El tipo de dosis debe contener al menos 3 caracteres.");
    }

    // Validar descripción (mínimo 3 caracteres)
    if (descripcion.length < 3) {
        mostrarError("La descripción debe contener al menos 3 caracteres.");
    }

    return valido; 
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
  