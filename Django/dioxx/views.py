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

""" Emergencias """

""" Accesos """

""" Medicamentos """