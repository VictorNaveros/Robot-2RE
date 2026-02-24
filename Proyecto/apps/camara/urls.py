from django.urls import path
from . import views

app_name = 'camara'

urlpatterns = [
    path("", views.recibir_imagen, name="recibir_imagen"),
]