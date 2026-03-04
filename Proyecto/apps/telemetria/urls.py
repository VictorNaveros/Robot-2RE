from django.urls import path
from .views import esperar_orden_servo, recibir_telemetria

app_name = 'telemetria'

urlpatterns = [
    path("telemetria/", recibir_telemetria, name='recibir_telemetria'),
    path('esperar-orden-servo/', esperar_orden_servo, name='esperar_orden_servo'),
]