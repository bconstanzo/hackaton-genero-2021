from django.shortcuts import render

victima = {
    "nombre": "Alicia Perez",
    "domicilio": "Av.Colón 1234",
    "documento": "30 111 222",
    "telefono": "+542235112233",
    "email": "alicia_perez@gmail.com",
    "fecha_nacimiento": "01/02/1985",
    # contactos = ... # lista de Contactos
}

casos = [
    {
        "victima": "Alicia",
        "agresor": "Bartolomé Diaz",
        "fecha": "12 Noviembre 2021",
    },
    {
        "victima": "Alicia",
        "agresor": "Darío Martinez",
        "fecha": "12 de Noviembre 2021",
    },
]

# Create your views here.
def perfil(request):
    context = {
        "victima" : victima,
        "casos": casos,
    }
    return render(request, "casos/perfil.html", context=context)

def caso(request):
    context = {
        "caso": casos[0],
    }
    return render(request, "casos/caso.html", context=context)

def home(request):
    # TODO: Agregar redireccion al que esta logeado
    return render(request, "casos/home.html")

def about(request):
    return render(request, "casos/about.html", {"title": "Resultado del Hackaton Contra la Violencia de Género 2021"})