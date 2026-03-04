import json
from datetime import date
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import EstadoSensores, EstadoRobot, JornadaRobot, EventoSensor, ContadorBotellas


@csrf_exempt
def recibir_telemetria(request):
    """Recibe telemetría del ESP32/PC y la guarda en la BD"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("\n" + "=" * 40)
            print("========== TELEMETRÍA RECIBIDA ==========")
            print(f"🕒 Hora: {timezone.now()}")
            print(f"📦 Payload: {data}")
            print("=" * 40 + "\n")

            # ====== PROCESAR SENSORES ======
            sensores_data = data.get('sensores', {})
            infrarrojo = sensores_data.get('Infrarrojo', 0)
            ultrasonico_cm = sensores_data.get('Ultrasonico_cm', 0)
            camara_raw = sensores_data.get('camara', None)  # 0, 1 o None si no viene

            # ====== CONTADOR DE BOTELLAS ======
            if infrarrojo == 0:
                hoy = date.today()
                contador, created = ContadorBotellas.objects.get_or_create(
                    fecha=hoy,
                    defaults={'cantidad': 0}
                )
                contador.cantidad += 1
                contador.save()
                print(f"🧴 Botella detectada! Total hoy: {contador.cantidad}")

            # ====== CALCULAR ALMACENAMIENTO ======
            PROFUNDIDAD_CONTENEDOR = 94  # cm cuando está vacío

            if ultrasonico_cm >= PROFUNDIDAD_CONTENEDOR:
                almacenamiento_pct = 0
            elif ultrasonico_cm <= 0:
                almacenamiento_pct = 100
            else:
                almacenamiento_pct = int(
                    ((PROFUNDIDAD_CONTENEDOR - ultrasonico_cm) / PROFUNDIDAD_CONTENEDOR) * 100
                )

            print(f"📏 Distancia: {ultrasonico_cm}cm → Almacenamiento: {almacenamiento_pct}%")

            # ====== ESTADO DE SENSORES ======
            # La cámara controla el estado de todos los demás sensores
            if camara_raw is None:
                estado_camara = 'desconectado'
            elif camara_raw == 1:
                estado_camara = 'ok'
            else:
                estado_camara = 'error'

            # Si la cámara no está ok, los demás sensores se desconectan también
            if estado_camara != 'ok':
                estado_infrarrojo = 'desconectado'
                estado_ultrasonico = 'desconectado'
            else:
                estado_infrarrojo = 'ok' if infrarrojo in [0, 1] else 'error'
                estado_ultrasonico = 'ok' if ultrasonico_cm > 0 else 'error'

            sensor, _ = EstadoSensores.objects.get_or_create(pk=1)
            sensor.camara = estado_camara
            sensor.s_infrarrojo = estado_infrarrojo
            sensor.s_ultrasonico = estado_ultrasonico
            sensor.save()

            print(f"📷 Cámara: {estado_camara} | 🔴 Infrarrojo: {estado_infrarrojo} | 📶 Ultrasónico: {estado_ultrasonico}")

            # ====== ESTADO ROBOT ======
            # Si la cámara no está ok, el robot pasa a inactivo
            if estado_camara != 'ok':
                estado_robot = 'inactivo'
            else:
                estado_esp = data.get('estado_robot', 'ONLINE')
                estado_robot = 'activo' if estado_esp == 'ONLINE' else 'inactivo'

            EstadoRobot.objects.create(
                estado=estado_robot,
                almacenamiento_pct=almacenamiento_pct
            )

            # ====== RESPUESTA ======
            botellas_hoy = 0
            contador_hoy = ContadorBotellas.objects.filter(fecha=date.today()).first()
            if contador_hoy:
                botellas_hoy = contador_hoy.cantidad

            return JsonResponse({
                'status': 'ok',
                'mensaje': 'Telemetría guardada',
                'botellas_hoy': botellas_hoy,
                'almacenamiento': almacenamiento_pct,
                'camara': estado_camara,
            })

        except Exception as e:
            print(f"❌ ERROR al procesar telemetría: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'status': 'error',
                'mensaje': str(e)
            }, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def obtener_datos_dashboard(request):
    """Retorna el estado actual de sensores y robot"""
    try:
        sensores = EstadoSensores.objects.get(pk=1)
    except EstadoSensores.DoesNotExist:
        sensores = None

    try:
        estado_robot = EstadoRobot.objects.latest('fecha_registro')
    except EstadoRobot.DoesNotExist:
        estado_robot = None

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


@csrf_exempt
def esperar_orden_servo(request):
    """El ESP32 consulta si debe abrir el servo."""
    import apps.camara.estado_global as estado

    debe_abrir = estado.orden_abrir_servo

    if debe_abrir:
        estado.orden_abrir_servo = False

    return JsonResponse({
        'abrir_servo': debe_abrir
    })