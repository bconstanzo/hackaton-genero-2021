from django.contrib import admin
from django.contrib.auth.models import User
from simple_history.admin import SimpleHistoryAdmin
from .models import Caso, Contacto, Domicilio, Victima, Agresor, Incidencia, Documento, Concurrencia
from .models import get_history_user
from django.db.models import Q

admin.site.site_header = 'Administrador Surgen'

class CasoAdmin(admin.ModelAdmin):
    list_display = ["ver_causa", "estado"]
    list_editable = ["estado"]
    # si no quiero que se pueda editar en la misma lista saco list_editable = ["estado"]
    list_filter = ['estado']
    raw_id_fields = ['agresor','victima']
    # readonly_fields = ['fecha']

    @admin.display(empty_value='???')
    def ver_causa(self, obj):
        agresores = "; ".join( str(a) for a in obj.agresor.all() )
        return f"{obj.victima}, agredida por {agresores}"


class DocumentoAdmin(SimpleHistoryAdmin):
    exclude = ('mimetype', 'changed_by')
    list_display = ['view_archivo', 'fecha', 'descripcion']
    search_fields = ['caso__victima__nombre','caso__victima__apellido'] #busqueda de related search

    @admin.display(empty_value='???')
    def view_archivo(self, obj):
        return f"{obj.archivo.name}"

class IncidenciaAdmin(SimpleHistoryAdmin):
    exclude = ('changed_by', )
    list_display = ['nombre', 'fecha', 'view_caso']
    search_fields = ['caso__victima__nombre','caso__victima__apellido'] #busqueda de related search
    
    @admin.display(empty_value='???')
    def view_caso(self, obj):
        agresores = "; ".join( str(a) for a in obj.caso.agresor.all() )
        return f"{obj.caso.victima}, agredida por {agresores}"

class DomicilioHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['view_domicilio', 'view_persona']
    exclude = ('changed_by', )
    search_fields =  ['calle', 'altura']
    @admin.display(empty_value='???')
    def view_persona(self, obj):
        victimas = "; ".join( str(a) for a in Victima.objects.filter(domicilio = obj) )
        agresores = "; ".join( str(a) for a in Agresor.objects.filter(domicilio = obj) )
        return f"{f' Victima: {victimas} ' if victimas else ''} {f'Agresor: {agresores} ' if agresores else ''} "

    @admin.display(empty_value='???')
    def view_domicilio(self, obj):
        return (f"{obj.calle} {obj.altura}{f' ({obj.piso_depto}) ' if obj.piso_depto else ''}" 
        f", {obj.localidad}")


class VictimaHistoryAdmin(SimpleHistoryAdmin):
    exclude = ('changed_by', )
    list_display = ["view_nombre","documento", "email", "telefono","usuario"]
    history_list_display = ["documento", "email", "telefono"]
    search_fields = ['documento','nombre','apellido']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "domicilio":
            try:
                victimas = Victima.objects.all() 
                agresores = Agresor.objects.all()
                domicilios_asignados = []
                for persona in victimas: #me imagino que hay una mejor forma de hacer y escribir esto pero ahora lo pruebo asi.
                    domicilios_asignados.append(persona.domicilio.id)
                for persona in agresores:
                    domicilios_asignados.append(persona.domicilio.id)
                kwargs["queryset"] = Domicilio.objects.all().exclude(id__in=domicilios_asignados)
            except IndexError:
                pass
        elif db_field.name == "usuario":
            try:
                victimas = Victima.objects.all() 
                usuarios_asignados = []
                for victima in victimas:
                    usuarios_asignados.append(victima.usuario.id)
                print(usuarios_asignados)
                kwargs["queryset"] = User.objects.all().exclude(Q(is_staff = True) | Q(id__in=usuarios_asignados))
            except IndexError:
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(empty_value='???')
    def view_nombre(self, obj):
        return f"{obj.nombre} {obj.apellido}"

class AgresorHistoryAdmin(SimpleHistoryAdmin):
    exclude = ('changed_by', )
    list_display = ["view_nombre","documento", "email", "telefono"]
    history_list_display = ["documento", "email", "telefono"]
    search_fields = ['documento','nombre','apellido']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "domicilio":
            try:
                victimas = Victima.objects.all() 
                agresores = Agresor.objects.all()
                domicilios_asignados = []
                for persona in victimas: #me imagino que hay una mejor forma de hacer y escribir esto pero ahora lo pruebo asi.
                    domicilios_asignados.append(persona.domicilio.id)
                for persona in agresores:
                    domicilios_asignados.append(persona.domicilio.id)
                kwargs["queryset"] = Domicilio.objects.all().exclude(id__in=domicilios_asignados)
            except IndexError:
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    @admin.display(empty_value='???')
    def view_nombre(self, obj):
        return f"{obj.nombre} {obj.apellido}"

class ContactoHistoryAdmin(SimpleHistoryAdmin):
    exclude = ('changed_by', )
    list_display = ["nombre", "email", "telefono"]
    history_list_display = ["email", "telefono"]
    search_fields = ['victima__nombre','victima__apellido'] #busqueda de related search

class ConcurrenciaAdmin(SimpleHistoryAdmin):
    exclude = ('changed_by', )
    list_display = ["caso", "fecha", 'lugar_concurrido']
    # si no quiero que se pueda editar en la misma lista saco list_editable = ["estado"]
    list_filter = ['fecha','caso']
    search_fields = ['caso__victima__nombre','caso__victima__apellido'] #busqueda de related search


# Register your models here.
admin.site.register(Caso,CasoAdmin)
admin.site.register(Contacto, ContactoHistoryAdmin, get_user=get_history_user)
admin.site.register(Domicilio, DomicilioHistoryAdmin, get_user=get_history_user)
admin.site.register(Victima, VictimaHistoryAdmin, get_user=get_history_user)
admin.site.register(Agresor, AgresorHistoryAdmin, get_user=get_history_user)
admin.site.register(Incidencia, IncidenciaAdmin, get_user=get_history_user)
admin.site.register(Documento, DocumentoAdmin, get_user=get_history_user)
admin.site.register(Concurrencia,ConcurrenciaAdmin, get_user=get_history_user)