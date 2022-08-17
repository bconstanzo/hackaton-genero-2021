from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="casos-home"),
    path("perfil/", views.perfil, name="casos-perfil"),
    path("perfil/caso/<id>", views.caso, name="casos-caso"),
    path("acercade/", views.about, name="casos-about"),
    path("editar_perfil/", views.editar_perfil, name="casos-editar_perfil"),
    path("agregar_contacto/", views.agregar_contacto, name="casos-agregar_contacto"),
    path("editar_contacto/<id_contacto>", views.editar_contacto, name="casos-editar_contacto"),
    path("descargar/<filename>", views.descargar, name="descargar"),
]