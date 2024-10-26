from django.shortcuts import render
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

""" Residentes """
def listRes(request):
    residentes = residente.objects.all()

    context = {
        "residentes": residentes
    }

    return render(request, "pages/residentes/list_res.html", context)

def verRes(request, pk):
    if pk != "":
        res = residente.objects.get(rut = pk)
        rec = receta.objects.get(residente = pk)
        det = detalleReceta.objects.filter(idReceta = rec)

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
        res = residente.objects.get(rut = pk)
        rec = receta.objects.get(residente = pk)
        det = detalleReceta.objects.filter(idReceta = rec)

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

        resObj = residente(
            rut = rRut,
            nombre = rNombre,
            apellido = rApellido,
            edad = rEdad,
            contactos = rContactos,
            nroEmergencia = rNroE
        )
        resObj.save()

        context = {
            "residente": resObj,
            "mensaje": "Modificación exitosa"
        }
        return render(request, "pages/residentes/upd_res.html", context)
        
def delRes(request, pk):
    try:
        res = residente.objects.get(rut = pk)
        res.delete()

        residentes = residente.objects.all()

        context = {
            "residentes": residentes
        }
        return render(request, "pages/residentes/list_res.html", context)
    except:
        res = residente.objects.get(rut = pk)
        rec = receta.objects.get(residente = pk)
        det = detalleReceta.objects.filter(idReceta = rec)

        context = {
            "residente": res,
            "receta": rec,
            "detalleR": det,
            "mensaje": "No se pudo eliminar al residente"
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

""" Medicamentos """