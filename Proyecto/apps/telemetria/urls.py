from django.urls import path
from .views import recibir_telemetria

app_name = 'telemetria'

urlpatterns = [
    path('', recibir_telemetria, name='recibir_telemetria'),
]