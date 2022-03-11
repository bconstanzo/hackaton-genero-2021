from django.shortcuts import render

casos = [
    {
        "victima": "Alicia",
        "agresor": "Bartolomé",
        "fecha": "12 Noviembre 2021",
    },
    {
        "victima": "Carla",
        "agresor": "Darío",
        "fecha": "12 de Noviembre 2021",
    },

]


# Create your views here.
def home(request):
    context = {
        "casos": casos,
    }
    return render(request, "casos/home.html", context=context)

def about(request):
    return render(request, "casos/about.html", {"title": "Resultado del Hackaton Contra la Violencia de Género 2021"})