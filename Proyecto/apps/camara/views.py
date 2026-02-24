from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .yolo_detector import detectar_botella
import apps.camara.estado_global as estado
import os

ULTIMA_IMAGEN = os.path.join(os.path.dirname(__file__), "ultima.jpg")

@csrf_exempt
def recibir_imagen(request):

    # GET → mostrar última imagen en navegador
    if request.method == "GET":
        if os.path.exists(ULTIMA_IMAGEN):
            with open(ULTIMA_IMAGEN, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        else:
            return HttpResponse("No hay imagen disponible aún", status=404)

    # POST → desde ESP32
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    # Guardar la imagen
    if request.body:
        with open(ULTIMA_IMAGEN, "wb") as f:
            f.write(request.body)

    # Detectar botellas (solo 0 o 1)
    hay_botella = detectar_botella(ULTIMA_IMAGEN, conf=0.2, iou=0.2)

    # Activar servo si hay botella
    if hay_botella:
        estado.orden_abrir_servo = True

    # Mostrar en consola
    if hay_botella:
        print("🧴 BOTELLA DETECTADA")
    else:
        print("🚫 NO HAY BOTELLA")

    # Devolver JSON con la info
    return JsonResponse({
        "botellas": hay_botella  # 1 = hay, 0 = no hay
    })