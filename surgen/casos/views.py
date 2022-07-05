from django.shortcuts import render
from .models import Caso

# Create your views here.
def perfil(request):
    context = {
        "casos": Caso.objects.all(),
    }
    return render(request, "casos/perfil.html", context=context)

def caso(request):
    context = {
        "caso": Caso.objects.first(),
    }
    return render(request, "casos/caso.html", context=context)

def home(request):
    # TODO: Agregar redireccion al que esta logeado
    return render(request, "casos/home.html")

def about(request):
    return render(request, "casos/about.html", {"title": "Resultado del Hackaton Contra la Violencia de Género 2021"})