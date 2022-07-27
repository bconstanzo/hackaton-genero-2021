from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="casos-home"),
    path("perfil/", views.perfil, name="casos-perfil"),
    path("perfil/caso/", views.caso, name="casos-caso"),
    path("acercade/", views.about, name="casos-about"),
    path("descargar/<filename>", views.descargar, name="descargar"),
]