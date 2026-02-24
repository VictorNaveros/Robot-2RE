from django.http import JsonResponse

def recibir_imagen(request):
    return JsonResponse({
        "mensaje": "Camara activa sin IA"
    })