/* Formulario add_personal */

document.addEventListener("DOMContentLoaded", () => {
  const rut = document.getElementById("rut");
  const nombre = document.getElementById("nombre");
  const apellido = document.getElementById("apellido");

  const Mrut = document.getElementById("mrut");
  const Mnombre = document.getElementById("mnombre");
  const Mapellido = document.getElementById("mapellido");
  const rutvalido = /^\d{7,8}-[\dKk]{1}$/;

  rut.addEventListener("input", () => {
    const rutval = rut.value.trim();
    if (rutval.length != 0){
      if (!rutvalido.test(rutval)) {
          Mrut.textContent = "ingrese un rut válido\nej: 12345678-9";
          Mrut.classList.add("mensaje_error");
          rut.style.borderColor = "red";
      } else {
          Mrut.textContent = "";
          Mrut.classList.remove("mensaje_error");
          rut.style.borderColor = "#ccc";
      }
    }
  });

  rut.dispatchEvent(new Event("input"));
  
  nombre.addEventListener("input", () => {
    const nombrevalue = nombre.value.trim();
    if (nombrevalue.length < 4 && nombrevalue.length != 0) {
        Mnombre.textContent = "ingrese un nombre válido";
        Mnombre.classList.add("mensaje_error");
        nombre.style.borderColor = "red";
    } else {
        Mnombre.textContent = "";
        Mnombre.classList.remove("mensaje_error");
        nombre.style.borderColor = "#ccc";
    }
  });

  nombre.dispatchEvent(new Event("input"));

  apellido.addEventListener("input", () => {
    const apellidovalue = apellido.value.trim();
    
    if (apellidovalue.length < 4 && apellidovalue.length != 0) {
        Mapellido.textContent = "ingrese un apellido válido";
        Mapellido.classList.add("mensaje_error");
        apellido.style.borderColor = "red";
    } else {
        Mapellido.textContent = "";
        Mapellido.classList.remove("mensaje_error");
        apellido.style.borderColor = "#ccc";
    }
  });

  apellido.dispatchEvent(new Event("input"));

});