from django.shortcuts import render
from .models import Caso
from .models import Incidencia
from .models import Documento

# Create your views here.
def perfil(request):
    context = {
        "victima": Caso.objects.first().victima,
        "casos": Caso.objects.all(), # esto esta tirando error-> sera por db vacia?
    }
    return render(request, "casos/perfil.html", context=context)

def caso(request):
    context = {
        "caso": Caso.objects.first(), # TODO aca seria solo el caso que pido el usuario
        "historial" : Incidencia.objects.first(), #TODO aca se enviaria un arreglo ordenado de los eventos
        "incidencias" : Incidencia.objects.first(), # TODO aca se deberian agregar las incidencias que correspondan al caso
        "documentos" : Documento.objects.first() # TODO aca se deberian agregar los documentos que correspondan al caso
    }
    return render(request, "casos/caso.html", context=context)

def home(request):
    # TODO: Agregar redireccion al que esta logeado
    return render(request, "casos/home.html")

def about(request):
    return render(request, "casos/about.html", {"title": "Resultado del Hackaton Contra la Violencia de Género 2021"})