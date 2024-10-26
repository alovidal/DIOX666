from django.urls import path
from dioxx import views

urlpatterns = [
    # General
    path("", views.index, name="index"),
    path("notificaciones", views.notificaciones, name="notificaciones"),

    # Residentes
    path("listRes/", views.listRes, name="listRes"),
    path("verRes/<str:pk>", views.verRes, name="verRes"),
    path("findRes/<str:pk>", views.findRes, name="findRes"),
    path("addRes/", views.addRes, name="addRes"),
    path("updRes/", views.updRes, name="updRes"),
    path("delRes/<str:pk>", views.delRes, name="delRes"),

    # Personal
    path("listPer/", views.listPer, name="listPer"),
    path("verPer/<str:pk>", views.verPer, name="verPer"),
    path("findPer/<str:pk>", views.findPer, name="findPer"),
    path("addPer/", views.addPer, name="addPer"),
    path("updPer/", views.updPer, name="updPer"),
    path("delPer/<str:pk>", views.delPer, name="delPer"),

    # Emergencias
    path("listErm/", views.listErm, name="listErm"),
    path("addErm/", views.addErm, name="addErm"),
    path("verErm/<str:pk>", views.verErm, name="verErm"),
    path("findErm/<str:pk>", views.findErm, name="findErm"),
    path("updErm/<str:pk>", views.updErm, name="updErm"),
    path("delErm/<str:pk>", views.delErm, name="delErm"),

    # Accesos
    path("listAcc/", views.listAcc, name="listAcc"),
    path("addAcc/", views.addAcc, name="addAcc"),
    path("verAcc/<str:pk>", views.verAcc, name="verAcc"),
    path("findAcc/<str:pk>", views.findAcc, name="findAcc"),
    path("updAcc/<str:pk>", views.updAcc, name="updAcc"),
    path("delAcc/<str:pk>", views.delAcc, name="delAcc"),

    # Eventos
    path("listEvt/", views.listEvt, name="listEvt"),
    path("addEvt/", views.addEvt, name="addEvt"),
    path("verEvt/<str:pk>", views.verEvt, name="verEvt"),
    path("findEvt/<str:pk>", views.findEvt, name="findEvt"),
    path("updEvt/<str:pk>", views.updEvt, name="updEvt"),
    path("delEvt/<str:pk>", views.delEvt, name="delEvt"),
    path('calendario/', views.calendario_eventos, name='calendario_eventos'),

    # Medicamentos
    path("opcMed/", views.opcMed, name="opcMed"),
    path('listMed/', views.listMed, name='listMed'),
    path("addMed/", views.addMed, name="addMed"),
    path("verMed/<str:pk>", views.verMed, name="verMed"),
    path("findMed/<str:pk>", views.findMed, name="findMed"),
    path("updMed/<str:pk>", views.updMed, name="updMed"),
    path("delMed/<str:pk>", views.delMed, name="delMed"),
    path("listResMedicamentos/", views.listResMedicamentos, name="listResMedicamentos"),

]
