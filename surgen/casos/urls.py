from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="casos-home"),
    path("perfil/", views.perfil, name="casos-perfil"),
    path("perfil/caso/<id>", views.caso, name="casos-caso"),
    path("acercade/", views.about, name="casos-about"),
    path("editar_perfil/", views.editar_perfil, name="casos-editar_perfil"),
    path("agregar_contacto/", views.agregar_contacto, name="casos-agregar_contacto"),
    path("perfil/caso/agregar_nota/<id>/", views.agregar_nota, name="casos-agregar_nota"),
    path("perfil/caso/documentos/<id_caso>/<id_doc>", views.documentos, name="casos-documentos"),
    path("editar_contacto/<id_contacto>", views.editar_contacto, name="casos-editar_contacto"),
    path("descargar/<id_doc>", views.descargar, name="descargar"),
    path("perfil/caso/descargar_notas/<id_caso>", views.descargar_pdf_notas, name="casos-descargar_pdf_notas"),
    path("operador_busqueda/", views.operador_busqueda, name="casos-operador_busqueda"),
    path("operador_resultado/<id_victima>", views.operador_resultado, name="casos-operador_resultado"),
    path("operador_resultado/operador_ver_caso/<id_caso>", views.operador_ver_caso, name="casos-operador_ver_caso"),
]
