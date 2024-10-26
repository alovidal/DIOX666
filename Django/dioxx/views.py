from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *

# Create your views here.

""" 
    Superuser:
        user: dioxx
        password: dioxx_666
    
"""

""" General """
def index(request):
    context = {}
    return render(request, "pages/index.html", context)

def notificaciones(request):
    noti = notificacion.objects.all()

    context = {
        "notificaciones": noti 
    }
    return render(request, "pages/notificaciones.html", context)

""" Residentes """
def listRes(request):
    residentes = residente.objects.all()

    context = {
        "residentes": residentes
    }

    return render(request, "pages/residentes/list_res.html", context)

def verRes(request, pk):
    if pk != "":
        res = get_object_or_404(residente, rut=pk)
        try:
            rec = receta.objects.get(residente=pk)
            det = detalleReceta.objects.filter(idReceta=rec)
        except receta.DoesNotExist:
            rec = None
            det = []

        context = {
            "residente": res,
            "receta": rec,
            "detalleR": det
        }
        return render(request, "pages/residentes/ver_res.html", context)

def addRes(request):
    if request.method == "POST": 
        # Crear el residente
        rut = request.POST["rut"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        edad = request.POST["edad"]
        contactos = request.POST["contactos"]
        nroEmergencia = request.POST["nroEmergencia"]

        nuevo_residente = residente(
            rut=rut, 
            nombre=nombre, 
            apellido=apellido,  
            edad=edad, 
            contactos=contactos, 
            nroEmergencia=nroEmergencia
        )
        nuevo_residente.save()

        # Crear el medicamento
        medicamento_nombre = request.POST["nombre_medicamento"]
        nuevo_medicamento = medicamento(nombre=medicamento_nombre)
        nuevo_medicamento.save()

        # Crear la receta
        nueva_receta = receta(residente=nuevo_residente)
        nueva_receta.save()

        # Crear el detalle de la receta
        cantidad_dosis = request.POST["cantDosis"]
        horario = request.POST["horario"]
        nuevo_detalle = detalleReceta(
            idReceta=nueva_receta,
            idMedicamento=nuevo_medicamento,
            cantDosis=cantidad_dosis,
            horario=horario,
        )
        nuevo_detalle.save()

        ress = residente.objects.all()
        context = {
            "residentes": ress,
        }
        return render(request, "pages/residentes/list_res.html", context)
    
    # Respuesta para el caso GET
    return render(request, "pages/residentes/add_res.html")
    
def findRes(request, pk):
    if pk != "":
        res = get_object_or_404(residente, rut=pk)
        try:
            rec = receta.objects.get(residente=pk)
            det = detalleReceta.objects.filter(idReceta=rec)
        except receta.DoesNotExist:
            rec = None
            det = []

        context = {
            "residente": res,
            "receta": rec,
            "detalleR": det
        }
        return render(request, "pages/residentes/upd_res.html", context)

def updRes(request):
    if request.method == "POST": 
        rRut = request.POST["rut"]
        rNombre = request.POST["nombre"]
        rApellido = request.POST["apellido"]
        rEdad = request.POST["edad"]
        rContactos = request.POST["contactos"]
        rNroE = request.POST["nroEmergencia"]

        # Intentamos obtener el residente
        res = get_object_or_404(residente, rut=rRut)

        # Actualizamos los campos del residente
        res.nombre = rNombre
        res.apellido = rApellido
        res.edad = rEdad
        res.contactos = rContactos
        res.nroEmergencia = rNroE
        res.save()

        # Manejamos la actualización de la receta si existe
        try:
            rec = receta.objects.get(residente=res)
            # Aquí podrías tener lógica para actualizar la receta si es necesario.
        except receta.DoesNotExist:
            rec = None
        
        context = {
            "residente": res,
            "receta": rec,
            "mensaje": "Modificación exitosa"
        }
        return render(request, "pages/residentes/upd_res.html", context)
       
def delRes(request, pk):
    try:
        res = get_object_or_404(residente, rut=pk)
        rec = receta.objects.get(residente=pk)
        rec.delete()  # Elimina la receta asociada si existe
        res.delete()  # Luego, elimina al residente

        residentes = residente.objects.all()
        context = {
            "residentes": residentes,
            "mensaje": "Residente eliminado con éxito."
        }
        return render(request, "pages/residentes/list_res.html", context)
    except receta.DoesNotExist:
        # Si la receta no existe, solo eliminamos al residente
        res = get_object_or_404(residente, rut=pk)
        res.delete()

        residentes = residente.objects.all()
        context = {
            "residentes": residentes,
            "mensaje": "Residente eliminado con éxito."
        }
        return render(request, "pages/residentes/list_res.html", context)
    except Exception as e:
        # Manejo de errores en caso de que haya un problema al eliminar
        context = {
            "residente": res,
            "mensaje": "No se pudo eliminar al residente."
        }
        return render(request, "pages/residentes/upd_res.html", context)

""" Personal """
def listPer(request):
    personas = personal.objects.all()

    context = {
        "personal": personas
    }

    return render(request, "pages/personal/list_per.html", context)

def verPer(request, pk):
    if pk != "":
        per = personal.objects.get(rut = pk)

        context = {
            "persona": per,
        }
        return render(request, "pages/personal/ver_per.html", context)
    
def addPer(request):
    if request.method == "POST":
        pRut = request.POST["rut"]
        pNombre = request.POST["nombre"]
        pApellido = request.POST["apellido"]
        pCargo = request.POST["cargo"]

        cargoPer = cargoPersonal.objects.get(idCargo = pCargo)

        perObj = personal(
            rut = pRut,
            nombre = pNombre,
            apellido = pApellido,
            cargo = cargoPer
        )
        perObj.save()

        cargos = cargoPersonal.objects.all()

        personas = personal.objects.all()

        context = {
            "personal": personas,
            "cargos": cargos,
        }
        return render(request, "pages/personal/list_per.html", context)
    
    # Respuesta para el caso GET
    cargos = cargoPersonal.objects.all()  # Obtener todos los cargos
    return render(request, "pages/personal/add_per.html", {"cargos": cargos})

def findPer(request, pk):
    if pk != "":
        per = personal.objects.get(rut = pk)
        cargos = cargoPersonal.objects.all()

        context = {
            "persona": per,
            "cargos": cargos
        }
        return render(request, "pages/personal/upd_per.html", context)

def updPer(request):
    if request.method == "POST":
        pRut = request.POST["rut"]
        pNombre = request.POST["nombre"]
        pApellido = request.POST["apellido"]
        pCargo = request.POST["cargo"]

        cargoPer = cargoPersonal.objects.get(idCargo = pCargo)

        perObj = personal(
            rut = pRut,
            nombre = pNombre,
            apellido = pApellido,
            cargo = cargoPer
        )
        perObj.save()

        cargos = cargoPersonal.objects.all()

        context = {
            "persona": perObj,
            "cargos": cargos,
            "mensaje": "Modificación exitosa"
        }
        return render(request, "pages/personal/upd_per.html", context)

def delPer(request, pk):
    try:
        per = personal.objects.get(rut = pk)
        per.delete()

        personas = personal.objects.all()

        context = {
            "persona": personas
        }
        return render(request, "pages/personal/list_per.html", context)
    except:
        per = personal.objects.get(rut = pk)

        context = {
            "persona": per,
            "mensaje": "No se pudo eliminar al personal"
        }
        return render(request, "pages/personal/upd_per.html", context)

""" Emergencias """
def listErm(request):
    emergencias = emergencia.objects.all()

    context = {
        "emergencias": emergencias
    }
    return render(request, "pages/emergencias/list_erm.html", context)

def addErm(request):
    if request.method == "POST":
        res = request.POST["residente"]
        fecha = request.POST["fecha"]
        descripcion = request.POST["descripcion"]

        residente_obj = residente.objects.get(rut=res)

        nueva_emergencia = emergencia(
            residente=residente_obj,
            fecha=fecha,
            descripcion=descripcion
        )
        nueva_emergencia.save()

        emergencias = emergencia.objects.all()
        context = {
            "emergencias": emergencias,
        }
        return render(request, "pages/emergencias/list_erm.html", context) 

    # Respuesta para el caso GET
    residentes = residente.objects.all()
    context = {
        "residentes": residentes,
    }
    return render(request, "pages/emergencias/add_erm.html", context)

def verErm(request, pk):
    if pk != "":
        erm = emergencia.objects.get(idEmergencia = pk)

        context = {
            "emergencia": erm
        }
        return render(request, "pages/emergencias/ver_erm.html", context)

def findErm(request, pk):
    if pk != "":
        erm = emergencia.objects.get(idEmergencia = pk)
        res = residente.objects.all()

        context = {
            "emergencia": erm,
            "residentes": res
        }
        return render(request, "pages/emergencias/upd_erm.html", context)
        
def updErm(request, pk):
    if pk != "": 
        if request.method == "POST":
            res = request.POST["residente"]
            fecha = request.POST["fecha"]
            descripcion = request.POST["descripcion"]

            residente_obj = residente.objects.get(rut=res)

            erm = emergencia(
                idEmergencia = pk,
                residente=residente_obj,
                fecha=fecha,
                descripcion=descripcion
            )
            erm.save()

            res = residente.objects.all()
            context = {
                "emergencia": erm,
                "residentes": res,
                "mensaje": "Modificacion exitosa"
            }
            return render(request, "pages/emergencias/upd_erm.html", context) 
        else:
            ermm = emergencia.objects.get(idEmergencia = pk)
            ress = residente.objects.all()
            context = {
                "emergencia": ermm,
                "residentes": ress,
                "mensaje": "Error al modificar la emergencia"
            }
            return render(request, "pages/emergencias/upd_erm.html", context) 
    
    else:
        ermm = emergencia.objects.get(idEmergencia = pk)
        ress = residente.objects.all()
        context = {
            "emergencia": ermm,
            "residentes": ress,
            "mensaje": "Error al modificar la emergencia"
        }
        return render(request, "pages/emergencias/upd_erm.html", context) 

def delErm(request, pk):
    try:
        erm = emergencia.objects.get(idEmergencia = pk)
        erm.delete()

        emergencias = emergencia.objects.all()

        context = {
            "emergencias": emergencias
        }
        return render(request, "pages/emergencias/list_erm.html", context)
    except:
        erm = emergencia.objects.get(idEmergencia = pk)

        context = {
            "emergencias": erm,
            "mensaje": "No se pudo eliminar la emergencia"
        }
        return render(request, "pages/emergencias/upd_erm.html", context)

""" Accesos """
def listAcc(request):
    accesos = acceso.objects.all()
    
    context = {
        "accesos": accesos
    }
    return render(request, "pages/accesos/list_acc.html", context)

def addAcc(request):
    if request.method == "POST":
        # Obtener datos del formulario
        fecha = request.POST["fecha"]
        tipo = request.POST["tipo"]
        personaRut = request.POST["personaRut"]
        personaNombre = request.POST["personaNombre"]

        # Crear una nueva instancia de acceso
        nuevo_acceso = acceso(
            fecha=fecha,
            tipo=tipo,
            personaRut=personaRut,
            personaNombre=personaNombre
        )
        
        # Guardar el nuevo acceso en la base de datos
        nuevo_acceso.save()

        # Obtener la lista actualizada de accesos
        accesos = acceso.objects.all()
        context = {
            "accesos": accesos,
            "mensaje": "Acceso agregado exitosamente"
        }
        return render(request, "pages/accesos/list_acc.html", context)

    # Si no es POST, mostrar el formulario vacío
    return render(request, "pages/accesos/add_acc.html")

def verAcc(request, pk):
    if pk != "":
        acc = acceso.objects.get(idAcceso = pk)
    
        context = {
            "acceso": acc
        }
        return render(request, "pages/accesos/ver_acc.html", context)

def findAcc(request, pk):
    if pk != "":
        acc = acceso.objects.get(idAcceso = pk)

        context = {
            "acceso": acc
        }
        return render(request, "pages/accesos/upd_acc.html", context)

def updAcc(request, pk):
    if pk != "": 
        if request.method == "POST":
            fecha = request.POST["fecha"]
            tipo = request.POST["tipo"]
            personaRut = request.POST["personaRut"]
            personaNombre = request.POST["personaNombre"]

            # Busca el acceso por su id
            try:
                acc = acceso(
                    idAcceso = pk,
                    fecha = fecha,
                    tipo = tipo,
                    personaRut = personaRut,
                    personaNombre = personaNombre
                )
                
                acc.save()

                mensaje = "Modificación exitosa"
            except acceso.DoesNotExist:
                acc = None
                mensaje = "Acceso no encontrado"
            
            context = {
                "acceso": acc,
                "mensaje": mensaje
            }
            return render(request, "pages/accesos/upd_acc.html", context) 
        else:
            try:
                acc = acceso.objects.get(idAcceso=pk)
                mensaje = ""
            except acceso.DoesNotExist:
                acc = None
                mensaje = "Acceso no encontrado"
            
            context = {
                "acceso": acc,
                "mensaje": mensaje
            }
            return render(request, "pages/accesos/upd_acc.html", context) 
    
    else:
        mensaje = "ID de acceso no válido"
        context = {
            "acceso": None,
            "mensaje": mensaje
        }
        return render(request, "pages/accesos/upd_acc.html", context)

def delAcc(request, pk):
    try:
        # Intenta obtener el objeto Acceso y eliminarlo
        acc = acceso.objects.get(idAcceso=pk)
        acc.delete()

        # Obtiene todos los accesos restantes
        accs = acceso.objects.all()

        # Renderiza la lista de accesos actualizada
        context = {
            "accesos": accs
        }
        return render(request, "pages/accesos/list_acc.html", context)

    except acceso.DoesNotExist:
        # En caso de error, prepara el contexto con un mensaje de error
        context = {
            "mensaje": "No se pudo eliminar el acceso"
        }
        return render(request, "pages/accesos/upd_acc.html", context)

""" Eventos """
def listEvt(request):
    evts = evento.objects.all()

    context = {
        "eventos": evts 
    }
    return render(request, "pages/eventos/list_evt.html", context)

def addEvt(request):
    if request.method == "POST":
        # Obtener datos del formulario
        titulo = request.POST["titulo"]
        fecha_inicio = request.POST["fecha_inicio"]
        fecha_fin = request.POST["fecha_fin"]
        descripcion = request.POST["descripcion"]

        # Crear una nueva instancia de evento
        nuevo_evento = evento(
            titulo=titulo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            descripcion=descripcion
        )
        
        # Guardar el nuevo evento en la base de datos
        nuevo_evento.save()

        # Obtener la lista actualizada de eventos
        eventos = evento.objects.all()
        context = {
            "eventos": eventos,
            "mensaje": "Evento agregado exitosamente"
        }
        return render(request, "pages/eventos/list_evt.html", context)
    
    # Si no es POST, mostrar el formulario vacío
    return render(request, "pages/eventos/add_evt.html")

def verEvt(request, pk):
    if pk:
        evento_obj = evento.objects.get(idEvento=pk)
        
        context = {
            "evento": evento_obj
        }
        return render(request, "pages/eventos/ver_evt.html", context)

def findEvt(request, pk):
    if pk:
        evento_obj = evento.objects.get(idEvento=pk)

        context = {
            "evento": evento_obj
        }
        return render(request, "pages/eventos/upd_evt.html", context)

def updEvt(request, pk):
    if pk: 
        if request.method == "POST":
            titulo = request.POST["titulo"]
            fecha_inicio = request.POST["fecha_inicio"]
            fecha_fin = request.POST["fecha_fin"]
            descripcion = request.POST["descripcion"]

            # Busca el evento por su id
            try:
                evento_obj = evento.objects.get(idEvento=pk)
                evento_obj.titulo = titulo
                evento_obj.fecha_inicio = fecha_inicio
                evento_obj.fecha_fin = fecha_fin
                evento_obj.descripcion = descripcion
                evento_obj.save()

                mensaje = "Modificación exitosa"
            except evento.DoesNotExist:
                evento_obj = None
                mensaje = "Evento no encontrado"
            
            context = {
                "evento": evento_obj,
                "mensaje": mensaje
            }
            return render(request, "pages/eventos/upd_evt.html", context) 
        else:
            try:
                evento_obj = evento.objects.get(idEvento=pk)
                mensaje = ""
            except evento.DoesNotExist:
                evento_obj = None
                mensaje = "Evento no encontrado"
            
            context = {
                "evento": evento_obj,
                "mensaje": mensaje
            }
            return render(request, "pages/eventos/upd_evt.html", context) 
    
    else:
        mensaje = "ID de evento no válido"
        context = {
            "evento": None,
            "mensaje": mensaje
        }
        return render(request, "pages/eventos/upd_evento.html", context)

def delEvt(request, pk):
    try:
        # Intenta obtener el objeto Evento y eliminarlo
        evento_obj = evento.objects.get(idEvento=pk)
        evento_obj.delete()

        # Obtiene todos los eventos restantes
        eventos = evento.objects.all()

        # Renderiza la lista de eventos actualizada
        context = {
            "eventos": eventos
        }
        return render(request, "pages/eventos/list_evt.html", context)

    except evento.DoesNotExist:
        # En caso de error, prepara el contexto con un mensaje de error
        context = {
            "mensaje": "No se pudo eliminar el evento"
        }
        return render(request, "pages/eventos/upd_evt.html", context)

def calendario_eventos(request):
    eventos = evento.objects.all()
    return render(request, 'pages/eventos/calendario_eventos.html', {'eventos': eventos})

""" Medicamentos """
def opcMed(request):
    context = {}
    return render(request, "pages/medicamentos/opc_med.html", context)

def listMed(request):
    meds = medicamento.objects.all()

    context = {
        "medicamentos": meds 
    }
    return render(request, "pages/medicamentos/list_med.html", context)

def addMed(request):
    mensaje = ""
    if request.method == "POST":
        nombre = request.POST["nombre"]

        # Crea un nuevo medicamento
        medicamento_obj = medicamento(nombre=nombre)
        medicamento_obj.save()
        
        mensaje = "Medicamento agregado exitosamente"
    
    context = {
        "mensaje": mensaje
    }
    return render(request, "pages/medicamentos/add_med.html", context)

def verMed(request, pk):
    if pk:
        medicamento_obj = medicamento.objects.get(idMedicamento=pk)
        
        context = {
            "medicamento": medicamento_obj
        }
        return render(request, "pages/medicamentos/ver_med.html", context)

def findMed(request, pk):
    if pk != "":
        med = medicamento.objects.get(idMedicamento = pk)

        context = {
            "medicamento": med
        }
        return render(request, "pages/medicamentos/upd_med.html", context)

def updMed(request, pk):
    if pk: 
        if request.method == "POST":
            nombre = request.POST["nombre"]

            # Busca el medicamento por su id
            try:
                medicamento_obj = medicamento.objects.get(idMedicamento=pk)
                medicamento_obj.nombre = nombre
                medicamento_obj.save()

                mensaje = "Modificación exitosa"
            except medicamento.DoesNotExist:
                medicamento_obj = None
                mensaje = "Medicamento no encontrado"
            
            context = {
                "medicamento": medicamento_obj,
                "mensaje": mensaje
            }
            return render(request, "pages/medicamentos/upd_med.html", context)
    else:
        mensaje = "ID de medicamento no válido"
        context = {
            "medicamento": None,
            "mensaje": mensaje
        }
        return render(request, "pages/medicamentos/upd_med.html", context)

def delMed(request, pk):
    try:
        # Intenta obtener el objeto Medicamento y eliminarlo
        medicamento_obj = medicamento.objects.get(idMedicamento=pk)
        medicamento_obj.delete()

        # Renderiza la lista de medicamentos actualizada
        medicamentos = medicamento.objects.all()
        context = {
            "medicamentos": medicamentos,
            "mensaje": "Medicamento eliminado exitosamente"
        }
        return render(request, "pages/medicamentos/list_med.html", context)

    except medicamento.DoesNotExist:
        # En caso de error, prepara el contexto con un mensaje de error
        context = {
            "mensaje": "No se pudo eliminar el medicamento"
        }
        return render(request, "pages/medicamentos/upd_med.html", context)

def listResMedicamentos(request):
    residentes = residente.objects.all()
    datos_residentes = []

    for res in residentes:
        try:
            rec = receta.objects.get(residente=res)
            detalles = detalleReceta.objects.filter(idReceta=rec)
            medicamentos = []
            for detalle in detalles:
                medicamento_info = {
                    'nombre': detalle.idMedicamento.nombre,
                    'dosis_m': detalle.cantDosis if not detalle.horario.endswith('t') else 'No',
                    'dosis_t': detalle.cantDosis if detalle.horario.endswith('t') else 'No',
                    'dosis_n': detalle.cantDosis if detalle.horario.endswith('n') else 'No',
                }
                medicamentos.append(medicamento_info)

            datos_residentes.append({
                'residente': res,
                'medicamentos': medicamentos
            })
        except receta.DoesNotExist:
            datos_residentes.append({
                'residente': res,
                'medicamentos': []
            })

    context = {
        'datos_residentes': datos_residentes
    }
    return render(request, "pages/medicamentos/list_res_medicamentos.html", context)
