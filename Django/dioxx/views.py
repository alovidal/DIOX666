from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from datetime import datetime, timedelta
from django.utils.timezone import localtime, now, make_aware
import re
from django.http import Http404

# Create your views here.

""" 
    Superuser:
        user: dioxx
        password: dioxx_666
    
    Testing:
        user: testing
        password: dioxx_666
"""

""" General """
def index(request):
    context = {}
    return render(request, "pages/index.html", context)

@login_required
def notificaciones(request):
    # Obtener la fecha y hora local actual
    today = localtime(now()).date()
    # Calcular la fecha de mañana
    tomorrow = today + timedelta(days=1)

    # Filtrar eventos que ocurren mañana
    eventos = evento.objects.filter(
        fecha_inicio__date=tomorrow
    )

    # Depuración: Imprimir las fechas de los eventos
    for evt in eventos:
        print(f"Evento: {evt.descripcion}, Fecha inicio: {evt.fecha_inicio}")

    context = {
        'eventos': eventos,
        'tomorrow': tomorrow,
    }
    return render(request, "pages/notificaciones.html", context)

def conectar(request):
    # Si el usuario no está logeado puede logearse
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            # Verificar las credenciales
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Iniciar sesión
                return redirect('listRes')  # Redirige a la lista de residentes
            else:
                context = {
                    "mensaje": "Usuario o contraseña incorrecta.",
                    "design": "error"  # Puedes usar esta clase para estilizar tu mensaje
                }
                return render(request, "pages/index.html", context)
        else:
            return render(request, "pages/index.html")
    else:
        return redirect('listRes')  # Si ya está logueado, redirige a la lista de residentes

def desconectar(request):
    if request.user.is_authenticated:
        logout(request)  # Cerrar sesión
        return redirect('index')  # Redirigir al índice después de cerrar sesión
    return redirect('index')  # Redirigir al índice si no está autenticado

""" Residentes """
@login_required
def listRes(request):
    residentes = residente.objects.all()

    context = {
        "residentes": residentes
    }

    return render(request, "pages/residentes/list_res.html", context)

@login_required
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

@login_required
def addRes(request):
    if request.method == "POST": 
        # Crear el residente
        rut = request.POST["rut"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        edad = request.POST["edad"]
        contactos = request.POST["contactos"]
        nroEmergencia = request.POST["nroEmergencia"]

        """ Test del rut """
        dresidentes = residente.objects.all()
        ruttest = True

        # Rut repetido en la base de datos
        for per in dresidentes:
            if per.rut == rut:
                ruttest = False
        # Largo del rut
        if len(rut) < 9 or len(rut) > 10:
            ruttest = False
        # Primeros 8 caracteres = dígitos
        elif not rut[:-2].isdigit():
            ruttest = False
        # Penúltimo carácter = '-'
        elif rut[-2] != '-':
            ruttest = False
        # Último carácter = dígito, 'K' o 'k'
        elif not (rut[-1].isdigit() or rut[-1].lower() == 'k'):
            ruttest = False
        """ ----------------------------------------------------- """

        """ Test de los contactos """
        nrotest = True
        # Al menos 9 dígitos
        if not re.match(r'^\d{9,}$', contactos):  
            nrotest = False
        elif not re.match(r'^\d{9,}$', nroEmergencia):  
            nrotest = False
        elif len(contactos) < 9 or len(nroEmergencia) < 9 or len(nroEmergencia) > 12:
            nrotest = False
        """ ----------------------------------------------------- """

        if (ruttest and len(nombre) > 3 and len(apellido) > 3 and len(edad) < 3 and nrotest):
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
        else:
            context = {
                "mensaje":"Datos inválidos o rut ya existe",
                "rut":rut,
                "nombre":nombre,
                "apellido":apellido,
                "edad":edad,
                "contactos":contactos,
                "nroEmergencia":nroEmergencia,
            }
            return render(request, "pages/residentes/add_res.html", context)

    # Respuesta para el caso GET
    return render(request, "pages/residentes/add_res.html")

@login_required    
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

@login_required
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

@login_required       
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
@login_required 
def listPer(request):
    personas = personal.objects.all()

    context = {
        "personal": personas
    }

    return render(request, "pages/personal/list_per.html", context)

@login_required 
def verPer(request, pk):
    if pk != "":
        per = personal.objects.get(rut = pk)

        context = {
            "persona": per,
        }
        return render(request, "pages/personal/ver_per.html", context)

@login_required
def addPer(request):
    if request.method == "POST":
        pRut = request.POST["rut"]
        pNombre = request.POST["nombre"]
        pApellido = request.POST["apellido"]
        pCargo = request.POST["cargo"]

        cargoPer = cargoPersonal.objects.get(idCargo = pCargo)
        
        """ Test del rut """
        dpersonal = personal.objects.all()
        ruttest = True

        # Rut repetido en la base de datos
        for per in dpersonal:
            if per.rut == pRut:
                ruttest = False
        # Largo del rut
        if len(pRut) < 9 or len(pRut) > 10:
            ruttest = False
        # Primeros 8 caracteres = dígitos
        elif not pRut[:-2].isdigit():
            ruttest = False
        # Penúltimo carácter = '-'
        elif pRut[-2] != '-':
            ruttest = False
        # Último carácter = dígito, 'K' o 'k'
        elif not (pRut[-1].isdigit() or pRut[-1].lower() == 'k'):
            ruttest = False
        """ ----------------------------------------------------- """

        if (ruttest and len(pNombre) > 3 and len(pApellido) > 3):
            perObj = personal(
                rut = pRut,
                nombre = pNombre,
                apellido = pApellido,
                cargo = cargoPer
            )
            perObj.save()

            """ objetos para el render """
            cargos = cargoPersonal.objects.all()
            personas = personal.objects.all()

            context = {
                "personal": personas,
                "cargos": cargos,
            }
            return render(request, "pages/personal/list_per.html", context)
        else:
            cargos = cargoPersonal.objects.all()
            context = {
                "mensaje":"Datos inválidos o rut ya existe",
                "cargos": cargos,
                "rut": pRut,
                "nombre": pNombre,
                "apellido": pApellido,
                "idcargo": pCargo
            }
            return render(request, "pages/personal/add_per.html", context)
    
    # Respuesta para el caso GET
    cargos = cargoPersonal.objects.all()  # Obtener todos los cargos
    return render(request, "pages/personal/add_per.html", {"cargos": cargos})

@login_required 
def findPer(request, pk):
    if pk != "":
        per = personal.objects.get(rut = pk)
        cargos = cargoPersonal.objects.all()

        context = {
            "persona": per,
            "cargos": cargos
        }
        return render(request, "pages/personal/upd_per.html", context)

@login_required 
def updPer(request):
    if request.method == "POST":
        pRut = request.POST["rutdata"]
        pNombre = request.POST["nombre"]
        pApellido = request.POST["apellido"]
        pCargo = request.POST["cargo"]

        cargoPer = cargoPersonal.objects.get(idCargo = pCargo)

        """ Test del rut """
        ruttest = True

        # Largo del rut
        if len(pRut) < 9 or len(pRut) > 10:
            ruttest = False
        # Primeros 8 caracteres = dígitos
        elif not pRut[:-2].isdigit():
            ruttest = False
        # Penúltimo carácter = '-'
        elif pRut[-2] != '-':
            ruttest = False
        # Último carácter = dígito, 'K' o 'k'
        elif not (pRut[-1].isdigit() or pRut[-1].lower() == 'k'):
            ruttest = False
        """ ----------------------------------------------------- """

        if (ruttest and len(pNombre) > 3 and len(pApellido) > 3):
            perObj = personal(
                rut = pRut,
                nombre = pNombre,
                apellido = pApellido,
                cargo = cargoPer
            )
            perObj.save()

            """ objetos para el render """
            cargos = cargoPersonal.objects.all()

            context = {
                "persona": perObj,
                "cargos": cargos,
                "mensaje": "Modificación exitosa"
            }
            return render(request, "pages/personal/upd_per.html", context)
        else:
            cargos = cargoPersonal.objects.all()
            dpersonal = personal.objects.get(rut = pRut)
            context = {
                "mensaje":"Datos inválidos o rut ya existe",
                "cargos": cargos,
                "rut": pRut,
                "nombre": pNombre,
                "apellido": pApellido,
                "idcargo": pCargo,
                "persona":dpersonal
            }
            return render(request, "pages/personal/upd_per.html", context)

@login_required 
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
@login_required 
def listErm(request):
    emergencias = emergencia.objects.all()

    context = {
        "emergencias": emergencias
    }
    return render(request, "pages/emergencias/list_erm.html", context)

@login_required 
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

@login_required 
def verErm(request, pk):
    if pk != "":
        erm = emergencia.objects.get(idEmergencia = pk)

        context = {
            "emergencia": erm
        }
        return render(request, "pages/emergencias/ver_erm.html", context)

@login_required 
def findErm(request, pk):
    if pk != "":
        erm = emergencia.objects.get(idEmergencia = pk)
        res = residente.objects.all()

        context = {
            "emergencia": erm,
            "residentes": res
        }
        return render(request, "pages/emergencias/upd_erm.html", context)

@login_required         
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

@login_required 
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
@login_required 
def listAcc(request):
    accesos = acceso.objects.all()
    
    context = {
        "accesos": accesos
    }
    return render(request, "pages/accesos/list_acc.html", context)

@login_required 
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

@login_required 
def verAcc(request, pk):
    if pk != "":
        acc = acceso.objects.get(idAcceso = pk)
    
        context = {
            "acceso": acc
        }
        return render(request, "pages/accesos/ver_acc.html", context)

@login_required 
def findAcc(request, pk):
    if pk != "":
        acc = acceso.objects.get(idAcceso = pk)

        context = {
            "acceso": acc
        }
        return render(request, "pages/accesos/upd_acc.html", context)

@login_required 
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

@login_required 
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
@login_required 
def listEvt(request):
    evts = evento.objects.all()

    context = {
        "eventos": evts 
    }
    return render(request, "pages/eventos/list_evt.html", context)

@login_required 
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

@login_required 
def verEvt(request, pk):
    if pk:
        evento_obj = evento.objects.get(idEvento=pk)
        
        context = {
            "evento": evento_obj
        }
        return render(request, "pages/eventos/ver_evt.html", context)

@login_required 
def findEvt(request, pk):
    if pk:
        evento_obj = evento.objects.get(idEvento=pk)

        context = {
            "evento": evento_obj
        }
        return render(request, "pages/eventos/upd_evt.html", context)

@login_required 
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

@login_required 
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

@login_required 
def calendario_eventos(request):
    eventos = evento.objects.all()
    return render(request, 'pages/eventos/calendario_eventos.html', {'eventos': eventos})

""" Medicamentos """
@login_required 
def opcMed(request):
    context = {}
    return render(request, "pages/medicamentos/opc_med.html", context)

@login_required 
def listMed(request):
    meds = medicamento.objects.all()

    context = {
        "medicamentos": meds 
    }
    return render(request, "pages/medicamentos/list_med.html", context)

@login_required 
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

@login_required 
def verMed(request, pk):
    if pk:
        medicamento_obj = medicamento.objects.get(idMedicamento=pk)
        
        context = {
            "medicamento": medicamento_obj
        }
        return render(request, "pages/medicamentos/ver_med.html", context)

@login_required 
def findMed(request, pk):
    if pk != "":
        med = medicamento.objects.get(idMedicamento = pk)

        context = {
            "medicamento": med
        }
        return render(request, "pages/medicamentos/upd_med.html", context)

@login_required 
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

@login_required 
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

@login_required 
def listResMedicamentos(request):
    # Inicializar listas vacías para residentes, detalles, recetas y medicamentos
    residentes = []  # Puedes mantener la consulta a la base de datos si decides utilizarla más adelante
    datos_residentes = []

    # Si decides mantener la consulta a residentes:
    # residentes = residente.objects.all()

    # Agregar la lógica para agregar residentes vacíos a datos_residentes
    for res in residentes:
        datos_residentes.append({
            'residente': res,
            'medicamentos': []  # Array vacío para medicamentos
        })

    context = {
        'datos_residentes': datos_residentes  # Mantener datos_residentes como está
    }
    return render(request, "pages/medicamentos/list_res_medicamentos.html", context)

@login_required
def dosis(request):
    # Obtener todos los residentes
    residentes = list(residente.objects.all())

    # Obtener el índice del residente actual desde la URL o inicializar en 0
    residente_index = int(request.GET.get("residente_index", 0))
    if residente_index < 0 or residente_index >= len(residentes):
        raise Http404("Residente no encontrado")

    # Obtener al residente actual
    residente_actual = residentes[residente_index]

    # Obtener medicamentos del residente actual a través de sus recetas
    recetas = receta.objects.filter(residente=residente_actual)
    detalles = detalleReceta.objects.filter(idReceta__in=recetas)
    medicamentos = []

    for detalle in detalles:
        horario = int(detalle.horario)  # Convertir horario a entero (cada cuántas horas)
        horas = []
        current_time = 6  # Inicia a las 6:00 AM

        while current_time < 24:
            horas.append(f"{current_time:02}:00")  # Formatear la hora
            current_time += horario

        # Categorizar las horas en bloques (mañana, tarde, noche)
        bloques = {
            "mañana": [h for h in horas if 6 <= int(h.split(":")[0]) < 12],
            "tarde": [h for h in horas if 12 <= int(h.split(":")[0]) < 18],
            "noche": [h for h in horas if 18 <= int(h.split(":")[0]) < 24],
        }

        medicamentos.append({
            "nombre": detalle.idMedicamento.nombre,
            "tipoDosis": detalle.idMedicamento.tipoDosis,
            "descripcion": detalle.idMedicamento.descripcion,
            "cantDosis": detalle.cantDosis,
            "bloques": bloques,
        })

    # Contexto para renderizar la página
    context = {
        "residente_actual": residente_actual,
        "medicamentos": medicamentos,
        "residente_index": residente_index,
        "total_residentes": len(residentes),
    }

    return render(request, "pages/medicamentos/dosis.html", context)

