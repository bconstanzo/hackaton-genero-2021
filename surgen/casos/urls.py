from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="casos-home"),
    path("acercade/", views.about, name="casos-about"),
]