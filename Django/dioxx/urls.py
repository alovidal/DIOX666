from django.urls import path
from dioxx import views

urlpatterns = [
    path("", views.index, name="index"),
]
