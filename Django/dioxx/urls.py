from django.urls import path
from dioxx import views

urlpatterns = [
    # General
    path("", views.index, name="index"),

    # Residentes
    path("listRes/", views.listRes, name="listRes")

    # Personal

    # Emergencias

    # Accesos

    # Medicamentos

]
