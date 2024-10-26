from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(residente)
admin.site.register(receta)
admin.site.register(medicamento)
admin.site.register(detalleReceta)
admin.site.register(cargoPersonal)
admin.site.register(personal)
admin.site.register(emergencia)
admin.site.register(acceso)
admin.site.register(notificacion)
admin.site.register(evento)