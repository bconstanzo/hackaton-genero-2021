from django.shortcuts import render, redirect
from .models import Caso
from .models import Victima
from .models import Incidencia
from .models import Documento
from .models import Contacto
from django.contrib.auth.decorators import login_required


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

def caso(request):
    caso = Caso.objects.first() # TODO aca seria solo el caso que pido el usuario
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

def descargar(filename):
    print('llego aca')
    # if filename != '':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR +"/" + filename
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
