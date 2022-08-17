from django.shortcuts import render, redirect
from .models import Caso, Domicilio
from .models import Victima
from .models import Incidencia
from .models import Documento
from .models import Contacto
from django.contrib.auth.decorators import login_required
from .forms import DomicilioForm, PerfilForm, ContactoForm
from django.http import HttpResponse
import os
import mimetypes

# Create your views here.
@login_required
def perfil(request):
    if request.user.is_superuser:
        response = redirect('/')
        return response
    else:
        victima = Victima.objects.get(usuario = request.user)
        print(victima)
        context = {
            "victima": victima,
            "casos": Caso.objects.filter(victima = victima),
            "contactos": Contacto.objects.filter(victima = victima),
        }
        return render(request, "casos/perfil.html", context=context)

def caso(request,id):
    caso = Caso.objects.get( id = id) # TODO aca seria solo el caso que pido el usuario
    incidencias = Incidencia.objects.filter(caso = caso)
    documentos = Documento.objects.filter(caso = caso) 
    historial = []
    for inc in incidencias :
        historial.append({
            'nombre': inc.nombre,
            'fecha': inc.fecha,
            'descripcion': inc.descripcion
            }
        )
    for doc in documentos :
        historial.append({
            'nombre': doc.archivo.name,
            'fecha': doc.fecha,
            'descripcion': doc.descripcion
            }
        )
    context = {
        "caso": caso, 
        "historial" : sorted(historial, key = lambda x: x['fecha']),
        "incidencias" : incidencias,
        "documentos" : documentos 
    }
    return render(request, "casos/caso.html", context=context)

def home(request): 
    if request.user.is_authenticated and (not request.user.is_superuser): 
        response = redirect('/perfil')
        return response
    else: 
        return render(request, "casos/home.html")

def about(request):
    return render(request, "casos/about.html")


def editar_perfil(request):
    victima = Victima.objects.get(usuario = request.user)
    domicilio = Domicilio.objects.get(victima = victima)
    form_perfil = PerfilForm(request.POST or None, request.FILES or None, instance=victima)
    form_domicilio = DomicilioForm(request.POST or None, request.FILES or None, instance=domicilio)
    context = {
        "form_perfil" : form_perfil,
        "form_domicilio" : form_domicilio,
    }
    if form_perfil.is_valid() and form_domicilio.is_valid():
        form_perfil.save()
        form_domicilio.save()
        response = redirect('/perfil')
        return response
    return render(request, "casos/editar_perfil.html", context = context)

def agregar_contacto(request):
    victima = Victima.objects.get(usuario = request.user)
    contacto = Contacto(victima = victima, nombre ='', telefono='', email='')
    form_contacto = ContactoForm(request.POST or None, request.FILES or None, instance=contacto)
    context = {
        "form_contacto" : form_contacto,
    }
    if form_contacto.is_valid():
        form_contacto.save()
        response = redirect('/perfil')
        return response
    return render(request, "casos/agregar_contacto.html", context = context)

def editar_contacto(request,id_contacto):
    victima = Victima.objects.get(usuario = request.user)
    contacto = Contacto.objects.get(victima = victima, id = id_contacto)
    form_contacto = ContactoForm(request.POST or None, request.FILES or None, instance=contacto)
    context = {
        "form_contacto" : form_contacto,
    }
    if form_contacto.is_valid():
        form_contacto.save()
        response = redirect('/perfil')
        return response
    return render(request, "casos/editar_contacto.html", context = context)

def descargar(request, filename):
    if filename != '':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR +"/" + filename
        path = open(filepath, 'r')
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response