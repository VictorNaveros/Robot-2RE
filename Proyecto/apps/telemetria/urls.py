from django.urls import path
from .views import esperar_orden_servo, recibir_telemetria, estado_actual

app_name = 'telemetria'

urlpatterns = [
    path("", recibir_telemetria, name='recibir_telemetria'),
    path('esperar-orden-servo/', esperar_orden_servo, name='esperar_orden_servo'),
    path('estado/', estado_actual, name='estado_actual'),  # ← nuevo endpoint para polling
]