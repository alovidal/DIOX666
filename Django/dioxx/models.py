from django.db import models

# Create your models here.
class residente(models.Model):
    rut = models.CharField(max_length=12, primary_key=True, db_column="rut")
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    edad = models.IntegerField()
    contactos = models.CharField(max_length=30)
    nroEmergencia = models.CharField(max_length=20)

    def __str__(self):
        return self.rut
    
class receta(models.Model):
    idReceta = models.AutoField(primary_key=True, db_column="idReceta")
    residente = models.ForeignKey("residente", on_delete=models.CASCADE, db_column="rut")

    def __str__(self):
        return str(self.residente)

class medicamento(models.Model):
    idMedicamento = models.AutoField(primary_key=True, db_column="idMedicamento")
    nombre = models.CharField(max_length=80)
    
    def __str__(self):
        return self.nombre

class detalleReceta(models.Model):
    idDetalleR = models.AutoField(primary_key=True, db_column="idDetalleR")
    idReceta = models.ForeignKey("receta", on_delete=models.CASCADE, db_column="idReceta")
    idMedicamento = models.ForeignKey("medicamento", on_delete=models.CASCADE, db_column="idMedicamento")
    cantDosis = models.IntegerField()
    horario = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.idDetalleR)
