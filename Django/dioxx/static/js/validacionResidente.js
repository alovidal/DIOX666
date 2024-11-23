/* Formulario add_residente */
document.addEventListener("DOMContentLoaded", () => {
    const rut = document.getElementById("rut");
    const nombre = document.getElementById("nombre");
    const apellido = document.getElementById("apellido");
    const edad = document.getElementById("edad");
    const contactos = document.getElementById("contactos");
    const nroEmergencia = document.getElementById("nroEmergencia");
  
    const Mrut = document.getElementById("mrut");
    const Mnombre = document.getElementById("mnombre");
    const Mapellido = document.getElementById("mapellido");
    const rutvalido = /^\d{7,8}-[\dKk]{1}$/;
    const Medad = document.getElementById("medad");
    const edadvalida = /^\d{1,3}$/;
    const Mcontactos = document.getElementById("mcontactos");
    const contactovalido = /(?:\D*\d){9}/;
    const mnroemer = document.getElementById("mnroemer");

    /* ------------------------------------------------------------------------------ */

    rut.addEventListener("input", () => {
      const rutval = rut.value.trim();
      if (rutval.length != 0){
          if (!rutvalido.test(rutval)) {
              Mrut.textContent = "Ingrese un rut válido\nej: 12345678-9";
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
    /* ------------------------------------------------------------------------------ */
    
    nombre.addEventListener("input", () => {
      const nombrevalue = nombre.value.trim();
      if (nombrevalue.length < 4 && nombrevalue.length != 0) {
          Mnombre.textContent = "Ingrese un nombre válido";
          Mnombre.classList.add("mensaje_error");
          nombre.style.borderColor = "red";
      } else {
          Mnombre.textContent = "";
          Mnombre.classList.remove("mensaje_error");
          nombre.style.borderColor = "#ccc";
      }
    });
  
    nombre.dispatchEvent(new Event("input"));
    /* ------------------------------------------------------------------------------ */
  
    apellido.addEventListener("input", () => {
      const apellidovalue = apellido.value.trim();
      
      if (apellidovalue.length < 4 && apellidovalue.length != 0) {
          Mapellido.textContent = "Ingrese un apellido válido";
          Mapellido.classList.add("mensaje_error");
          apellido.style.borderColor = "red";
      } else {
          Mapellido.textContent = "";
          Mapellido.classList.remove("mensaje_error");
          apellido.style.borderColor = "#ccc";
      }
    });
  
    apellido.dispatchEvent(new Event("input"));
    /* ------------------------------------------------------------------------------ */
  
    edad.addEventListener("input", () => {
        const edadvalue = edad.value.trim();
        
        if (edadvalue.length > 3 || !edadvalida.test(edadvalue) && edadvalue.length != 0) {
            Medad.textContent = "Ingrese una edad válida";
            Medad.classList.add("mensaje_error");
            edad.style.borderColor = "red";
        } else {
            Medad.textContent = "";
            Medad.classList.remove("mensaje_error");
            edad.style.borderColor = "#ccc";
        }
      });
    
      edad.dispatchEvent(new Event("input"));
      /* ------------------------------------------------------------------------------ */
  
      contactos.addEventListener("input", () => {
        const contactosvalue = contactos.value.trim();
        
        if ((contactosvalue.length < 9 || !contactovalido.test(contactosvalue)) && contactosvalue.length != 0) {
            Mcontactos.textContent = "Ingrese un número de contacto válido";
            Mcontactos.classList.add("mensaje_error");
            contactos.style.borderColor = "red";
        } else {
            Mcontactos.textContent = "";
            Mcontactos.classList.remove("mensaje_error");
            contactos.style.borderColor = "#ccc";
        }
      });
    
      contactos.dispatchEvent(new Event("input"));
      /* ------------------------------------------------------------------------------ */
  
      nroEmergencia.addEventListener("input", () => {
        const emervalue = nroEmergencia.value.trim();
        
        if ((emervalue.length < 9 || !contactovalido.test(emervalue) || emervalue.length > 12) && emervalue.length != 0) {
            mnroemer.textContent = "Ingrese un número de contacto válido";
            mnroemer.classList.add("mensaje_error");
            nroEmergencia.style.borderColor = "red";
        } else {
            mnroemer.textContent = "";
            mnroemer.classList.remove("mensaje_error");
            nroEmergencia.style.borderColor = "#ccc";
        }
      });
    
      nroEmergencia.dispatchEvent(new Event("input"));
      /* ------------------------------------------------------------------------------ */
  
  });