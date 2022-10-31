from pydoc import Doc
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Caso, Contacto, Domicilio, Victima, Agresor, Incidencia, Documento, Concurrencia
from .models import get_contacto_user, get_domicilio_user, get_victima_user

admin.site.site_header = 'Administrador Surgen'

class DocumentoAdmin(admin.ModelAdmin):
    exclude = ('mimetype', )

class DomicilioHistoryAdmin(SimpleHistoryAdmin):
    exclude = ('changed_by', )

class VictimaHistoryAdmin(SimpleHistoryAdmin):
    exclude = ('changed_by', )
    list_display = ["id", "email", "telefono"]
    history_list_display = ["email", "telefono"]

class ContactoHistoryAdmin(SimpleHistoryAdmin):
    exclude = ('changed_by', )
    list_display = ["nombre", "email", "telefono"]
    history_list_display = ["email", "telefono"]

# Register your models here.
admin.site.register(Caso)
admin.site.register(Contacto, ContactoHistoryAdmin, get_user=get_contacto_user)
admin.site.register(Domicilio, DomicilioHistoryAdmin, get_user=get_domicilio_user)
admin.site.register(Victima, VictimaHistoryAdmin, get_user=get_victima_user)
admin.site.register(Agresor)
admin.site.register(Incidencia)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Concurrencia)