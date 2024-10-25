from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(residente)
admin.site.register(receta)
admin.site.register(medicamento)
admin.site.register(detalleReceta)