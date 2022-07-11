from django.shortcuts import render
from .models import Caso
from .models import Incidencia
from .models import Documento

# Create your views here.
def perfil(request):
    victima = Caso.objects.first().victima
    context = {
        "victima": victima,
        "casos": Caso.objects.filter(victima = victima),
    }
    return render(request, "casos/perfil.html", context=context)

def caso(request):
    #El historial se compone de elementos con: nombre, descripcion y fecha 
    caso = Caso.objects.first() # TODO aca seria solo el caso que pido el usuario
    context = {
        "caso": caso, 
        "historial" : Incidencia.objects.all(), #TODO aca se enviaria un arreglo ordenado de los eventos
        "incidencias" : Incidencia.objects.filter(caso = caso),
        "documentos" : Documento.objects.filter(caso = caso) 
    }
    return render(request, "casos/caso.html", context=context)

def home(request):
    # TODO: Agregar redireccion al que esta logeado
    return render(request, "casos/home.html")

def about(request):
    return render(request, "casos/about.html", {"title": "Resultado del Hackaton Contra la Violencia de Género 2021"})