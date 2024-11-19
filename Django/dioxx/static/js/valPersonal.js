/* Formulario add_personal */

function validarAddPersonal() {
    // campos
    const rut = document.getElementById("rut").textContent;
    const nombre = document.getElementById("nombre").textContent;
    const apellido = document.getElementById("apellido").textContent;
    const selectCargo = document.getElementById("cargo").textContent;
    
    const cargo = selectCargo.value;

    console.log(cargo)
}