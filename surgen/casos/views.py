from django.shortcuts import render
from .models import Caso
from .models import Incidencia
from .models import Documento
from .models import Contacto

# Create your views here.
def perfil(request):
    victima = Caso.objects.first().victima
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
    # TODO: Agregar redireccion al que esta logeado
    #if request.user.is_authenticated: 
    #    return render(request, "casos/perfil.html")
    #else: 
        return render(request, "casos/home.html")

def about(request):
    return render(request, "casos/about.html")

def descargar():
    pass