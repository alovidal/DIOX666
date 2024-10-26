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
        return self.nombre+" "+self.apellido
    
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
        return str(self.idReceta)

class cargoPersonal(models.Model):
    idCargo = models.CharField(max_length=6, primary_key=True, db_column="idCargo")
    descripcion = models.CharField(max_length=30)
    
    def __str__(self):
        return self.descripcion

class personal(models.Model):
    rut = models.CharField(max_length=12, primary_key=True, db_column="rut")
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    cargo = models.ForeignKey("cargoPersonal", on_delete=models.CASCADE, db_column="idCargo")
    
    def __str__(self):
        return self.nombre+" "+self.apellido
    
class emergencia(models.Model):
    idEmergencia = models.AutoField(primary_key=True, db_column="idEmergencia")
    residente = models.ForeignKey("residente", on_delete=models.CASCADE, db_column="rut")
    fecha = models.DateField()
    descripcion = models.CharField(max_length=1000)

    def __str__(self) :
        return str(self.residente)

class acceso(models.Model):
    idAcceso = models.AutoField(primary_key = True, db_column="idAcceso")
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)
    personaRut = models.CharField(max_length=12)
    personaNombre = models.CharField(max_length=100)

    def __str__(self):
        return str(self.idAcceso)
    
class notificacion(models.Model):
    idNotificacion = models.AutoField(primary_key=True, db_column="idNotificacion")
    fecha = models.DateField()
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return str(self.idNotificacion)