from django.urls import path
from dioxx import views

urlpatterns = [
    # General
    path("", views.index, name="index"),

    # Residentes
    path("listRes/", views.listRes, name="listRes"),
    path("verRes/<str:pk>", views.verRes, name="verRes"),
    path("findRes/<str:pk>", views.findRes, name="findRes"),
    path("addRes/", views.addRes, name="addRes"),
    path("updRes/", views.updRes, name="updRes"),
    path("delRes/<str:pk>", views.delRes, name="delRes"),

    # Personal

    # Emergencias

    # Accesos

    # Medicamentos

]
