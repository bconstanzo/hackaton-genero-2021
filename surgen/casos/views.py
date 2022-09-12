from fileinput import filename
import os
import mimetypes
from asyncio.windows_events import NULL
from .models import Caso, Domicilio, Victima, Incidencia, Documento, Contacto, Nota
from .forms import DomicilioForm, PerfilForm, ContactoForm, NotaForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

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

@login_required
def caso(request,id):
    caso = Caso.objects.get( id = id) # TODO aca seria solo el caso que pido el usuario
    notas = Nota.objects.filter(caso = caso)
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
        "notas" : notas,
        "documentos" : documentos 
    }
    return render(request, "casos/caso.html", context=context)

@login_required
def documentos(request,id_caso, id_doc):  #TODO Manejo de mimetypes aca estoy solo mostrando los TXT
    caso = Caso.objects.get( id = id_caso)
    documentos = Documento.objects.filter(caso = caso) 
    imagen = ''
    if(id_doc != '-1'): # Si tengo un doc seleccionado para visualizar
        doc_actual =  Documento.objects.get(id = id_doc)
        filename = doc_actual.archivo.name
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR +"/" + filename
        #If mimetyoe = txt
        f = open(filepath, 'r')
        file_content = f.read()
        f.close()
        #if mimetype =imagen
        imagen = filepath

    else:
        doc_actual = NULL,
        file_content = ''

    context = {
        "caso": caso, 
        "documentos" : documentos,
        "doc_actual" : doc_actual,
        'file_content': file_content,
        "imagen" : imagen
    }
    return render(request, "casos/documentos.html", context=context)

def home(request): 
    if request.user.is_authenticated and (not request.user.is_superuser): 
        response = redirect('/perfil')
        return response
    else: 
        return render(request, "casos/home.html")

def about(request):
    return render(request, "casos/about.html")

@login_required
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

@login_required
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

@login_required
def agregar_nota(request, id):

    caso = Caso.objects.get(id = id)
    nota = Nota(caso = caso, fecha ='', descripcion='')
    form_nota = NotaForm(request.POST or None, request.FILES or None, instance=nota)
    context = {
        "form_nota" : form_nota,
    }
    if form_nota.is_valid():
        form_nota.save()
        response = redirect('/perfil/caso/'+id)
        return response
    return render(request, "casos/agregar_nota.html", context = context)

@login_required
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

@login_required
def descargar(request, filename):
    if filename != '':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR +"/" + filename
        path = open(filepath, 'r')
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

@login_required
def descargar_pdf_notas(request, id_caso):
    caso =  Caso.objects.get(id = id_caso)
    notas = Nota.objects.filter(caso = caso)
    template_path = 'casos/descargar_pdf_notas.html'
    template = get_template(template_path)
    context = {
        'notas': notas,
        'caso' : caso
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "Mis_notas.pdf"'  # si comento esta linea el pdf aparece en el navegador en vez de descargarse
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response