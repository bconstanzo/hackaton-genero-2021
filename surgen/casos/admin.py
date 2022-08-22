from pydoc import Doc
from django.contrib import admin
from .models import Caso, Contacto, Domicilio, Victima, Agresor, Incidencia, Documento, Nota


# Register your models here.
admin.site.register(Caso)
admin.site.register(Contacto)
admin.site.register(Domicilio)
admin.site.register(Victima)
admin.site.register(Agresor)
admin.site.register(Incidencia)
admin.site.register(Documento)
admin.site.register(Nota)