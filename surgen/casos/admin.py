from pydoc import Doc
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Caso, Contacto, Domicilio, Victima, Agresor, Incidencia, Persona, Documento, Concurrencia
from .models import get_contacto_user, get_domicilio_user, get_victima_user

admin.site.site_header = 'Administrador Surgen'

class CasoAdmin(admin.ModelAdmin):
    list_display = ["view_caso", "estado"]
    list_editable = ["estado"]
    # si no quiero que se pueda editar en la misma lista saco list_editable = ["estado"]
    list_filter = ['estado']

    @admin.display(empty_value='???')
    def view_caso(self, obj):
        agresores = "; ".join( str(a) for a in obj.agresor.all() )
        return f"{obj.victima}, agredida por {agresores}"


class DocumentoAdmin(admin.ModelAdmin):
    exclude = ('mimetype', )
    # segun que atributos quiero ordenar: ordering = ['']
    list_display = ['view_archivo', 'fecha', 'descripcion']
    search_fields = ['caso__victima__nombre','caso__victima__apellido'] #busqueda de related search

    @admin.display(empty_value='???')
    def view_archivo(self, obj):
        return f"{obj.archivo.name}"

class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha', 'view_caso']
    search_fields = ['caso__victima__nombre','caso__victima__apellido'] #busqueda de related search
    
    @admin.display(empty_value='???')
    def view_caso(self, obj):
        agresores = "; ".join( str(a) for a in obj.caso.agresor.all() )
        return f"{obj.caso.victima}, agredida por {agresores}"


#TODO busqueda por persona 

class DomicilioHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['view_domicilio', 'view_persona']
    exclude = ('changed_by', )
    search_fields =  ['calle', 'altura']
    @admin.display(empty_value='???')
    def view_persona(self, obj):
        victimas = "; ".join( str(a) for a in Victima.objects.filter(domicilio = obj) )
        agresores = "; ".join( str(a) for a in Agresor.objects.filter(domicilio = obj) )
        return f"{f' Victima: {victimas} ' if victimas else ''} {f'; Agresor: {agresores} ' if agresores else ''} "

    @admin.display(empty_value='???')
    def view_domicilio(self, obj):
        return (f"{obj.calle} {obj.altura}{f' ({obj.piso_depto}) ' if obj.piso_depto else ''}" 
        f", {obj.localidad}")


class VictimaHistoryAdmin(SimpleHistoryAdmin):
    exclude = ('changed_by', )
    list_display = ["view_nombre", "email", "telefono"]
    history_list_display = ["email", "telefono"]
    search_fields = ['nombre','apellido']

    @admin.display(empty_value='???')
    def view_nombre(self, obj):
        return f"{obj.nombre} {obj.apellido}"

class ContactoHistoryAdmin(SimpleHistoryAdmin):
    exclude = ('changed_by', )
    list_display = ["nombre", "email", "telefono"]
    history_list_display = ["email", "telefono"]
    search_fields = ['victima__nombre','victima__apellido'] #busqueda de related search

class ConcurrenciaAdmin(admin.ModelAdmin):
    list_display = ["caso", "fecha", 'lugar_concurrido']
    # si no quiero que se pueda editar en la misma lista saco list_editable = ["estado"]
    list_filter = ['fecha','caso']
    search_fields = ['caso__victima__nombre','caso__victima__apellido'] #busqueda de related search


# Register your models here.
admin.site.register(Caso,CasoAdmin)
admin.site.register(Contacto, ContactoHistoryAdmin, get_user=get_contacto_user)
admin.site.register(Domicilio, DomicilioHistoryAdmin, get_user=get_domicilio_user)
admin.site.register(Victima, VictimaHistoryAdmin, get_user=get_victima_user)
admin.site.register(Agresor)
admin.site.register(Incidencia, IncidenciaAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Concurrencia,ConcurrenciaAdmin)