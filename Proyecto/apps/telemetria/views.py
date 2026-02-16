import json
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import EstadoSensores, EventoSensor, EstadoRobot, JornadaRobot


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@csrf_exempt  # IMPORTANTE para ESP32
def recibir_telemetria(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "JSON inválido"},
            status=400
        )

    sensores = data.get("sensores")
    if not sensores:
        return JsonResponse(
            {"error": "sensores faltantes"},
            status=400
        )

    # 🔍 DEBUG (puedes quitar esto luego)
    print("========== TELEMETRÍA RECIBIDA ==========")
    print(f"🕒 Hora: {datetime.now()}")
    print(f"📦 Payload: {data}")
    print("========================================")

    # Snapshot único
    estado, _ = EstadoSensores.objects.get_or_create(pk=1)

    mapa_sensores = {
        "camara": "camara",
        "s_infrarrojo": "Infrarrojo",
        "s_ultrasonico": "ultrasonico",
    }

    cambios = []

    for campo_modelo, tipo_evento in mapa_sensores.items():
        nuevo_valor = sensores.get(tipo_evento)

        if nuevo_valor is None:
            continue

        estado_actual = getattr(estado, campo_modelo)
        nuevo_estado = "ok" if nuevo_valor == 1 else "error"

        if estado_actual != nuevo_estado:
            EventoSensor.objects.create(
                tipo_sensor=tipo_evento,
                valor=nuevo_valor
            )

            setattr(estado, campo_modelo, nuevo_estado)
            cambios.append(tipo_evento)

    if cambios:
        estado.save()

    return JsonResponse({
        "status": "ok",
        "cambios": cambios
    })


@login_required
def obtener_datos_dashboard(request):
    """
    Retorna el estado actual de sensores y robot
    """
    # Obtener estado actual de sensores (singleton pk=1)
    try:
        sensores = EstadoSensores.objects.get(pk=1)
    except EstadoSensores.DoesNotExist:
        sensores = None
    
    # Obtener último estado del robot
    try:
        estado_robot = EstadoRobot.objects.latest('fecha_registro')
    except EstadoRobot.DoesNotExist:
        estado_robot = None
    
    # Obtener jornada activa (sin fecha_fin)
    try:
        jornada_activa = JornadaRobot.objects.filter(fecha_fin__isnull=True).latest('fecha_inicio')
    except JornadaRobot.DoesNotExist:
        jornada_activa = None
    
    context = {
        'sensores': sensores,
        'estado_robot': estado_robot,
        'jornada_activa': jornada_activa,
    }
    
    return context