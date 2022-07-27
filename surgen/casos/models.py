from django.db import models
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import User

# Create your models here.

class Provincias(models.TextChoices):
    # de acuerdo con ISO 3166-2:AR
    CABA                = "AR-C", gettext_lazy("CABA")
    BUENOS_AIRES        = "AR-B", gettext_lazy("Buenos Aires")
    CATAMARCA           = "AR-K", gettext_lazy("Catamarca")
    CHACO               = "AR-H", gettext_lazy("Chaco")
    CHUBUT              = "AR-U", gettext_lazy("Chubut")
    CORDOBA             = "AR-X", gettext_lazy("Córdoba")
    CORRIENTES          = "AR-W", gettext_lazy("Corrientes")
    ENTRE_RIOS          = "AR-E", gettext_lazy("Entre Ríos")
    FORMOSA             = "AR-P", gettext_lazy("Formosa")
    JUJUY               = "AR-Y", gettext_lazy("Jujuy")
    LA_PAMPA            = "AR-L", gettext_lazy("La Pampa")
    LA_RIOJA            = "AR-F", gettext_lazy("La Rioja")
    MENDOZA             = "AR-M", gettext_lazy("Mendoza")
    MISIONES            = "AR-N", gettext_lazy("Misiones")
    NEUQUEN             = "AR-Q", gettext_lazy("Neuquén")
    RIO_NEGRO           = "AR-R", gettext_lazy("Río Negro")
    SALTA               = "AR-A", gettext_lazy("Salta")
    SAN_JUAN            = "AR-J", gettext_lazy("San Juan",)
    SAN_LUIS            = "AR-D", gettext_lazy("San Luis")
    SANTA_CRUZ          = "AR-Z", gettext_lazy("Santa Cruz")
    SANTA_FE            = "AR-S", gettext_lazy("Santa Fe")
    SANTIAGO_DEL_ESTERO = "AR-G", gettext_lazy("Santiago del Estero",)
    TIERRA_DEL_FUEGO    = "AR-V", gettext_lazy("Tierra del Fuego")
    TUCUMAN             = "AR-T", gettext_lazy("Tucumán")
    # sin especificar
    SIN_ESPECIIFAR      = "None", gettext_lazy("(sin especificar)")

class Domicilio(models.Model):
    calle = models.CharField(max_length=100)
    altura = models.IntegerField()
    piso_depto = models.CharField(max_length=10, blank=True)
    codigo_postal = models.CharField(max_length=12, blank=True)
    localidad = models.CharField(max_length=100)
    provincia = models.CharField(
        max_length=4,
        choices=Provincias.choices,
        default=Provincias.SIN_ESPECIIFAR,
    )

    # algunas ideas:
    # tipo de domicilio: residencia activa, legal, otro?
    # fecha_inicio, fecha_fin?  -- para el caso de ManyToMany

    def __str__(self):
        return (
            f"{self.calle} {self.altura}{f' ({self.piso_depto}) ' if self.piso_depto else ''}"
            f", {self.localidad}"
        )


class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    domicilio = models.ForeignKey(Domicilio, on_delete=models.DO_NOTHING)  # podría ser un ManyToMany?
    documento = models.CharField(max_length=15, blank=True)  # cambiar a futuro? va con espacio y sin puntos: DNI 12345678
    telefono = models.CharField(max_length=24, blank=True)
    email = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.DateField(null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class Victima(Persona):
    usuario = models.ForeignKey(User, null= True, on_delete=models.CASCADE)

class Agresor(Persona):
    pass


class Contacto(models.Model):
    # muy muy técnicamente, es una Persona con menos atributos
    victima = models.ForeignKey(Victima, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=24)
    email = models.CharField(max_length=50, null=True)


class Caso(models.Model):
    victima = models.ForeignKey(Victima, on_delete=models.SET_NULL, null=True)
    agresor = models.ManyToManyField(Agresor)
    fecha = models.DateTimeField()

    def __str__(self):
        agresores = "; ".join( str(a) for a in self.agresor.all() )
        return f"{self.victima}, agredida por {agresores}"


class Incidencia(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    fecha = models.DateTimeField(null=False)  # fecha denuncia/aviso/registro?
    descripcion = models.TextField()
    nombre = models.TextField() # ver si se deberia incluir o no
    def __str__(self):
        return self.nombre


class Documento(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING, blank=True, null=True)
    fecha = models.DateTimeField(null=False)
    descripcion = models.TextField()
    archivo = models.FileField()
    def __str__(self):
        return self.archivo.name