from django.shortcuts import render

# Create your views here.

""" General """
def index(request):
    context = {}
    return render(request, "pages/index.html", context)

""" Residentes """
def listRes(request):
    context = {}
    return render(request, "pages/residentes/list_res.html", context)

""" Personal """

""" Emergencias """

""" Accesos """

""" Medicamentos """