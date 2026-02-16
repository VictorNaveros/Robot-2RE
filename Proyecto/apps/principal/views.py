from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import PuntajeJuego
import json


def home(request):
    return render(request, 'principal/home.html')


def sobre_robot(request):
    return render(request, 'principal/sobre_robot.html')


def sobre_nosotros(request):
    return render(request, 'principal/sobre_nosotros.html')


def el_proyecto(request):
    return render(request, 'principal/el_proyecto.html')


def quiz_reciclaje(request):
    """Vista del quiz de reciclaje"""
    return render(request, 'principal/quiz.html')

def clasifica_residuos(request):
    """Vista del juego clasifica residuos"""
    return render(request, 'principal/clasifica.html')


@require_POST
def guardar_puntaje_quiz(request):
    """Guarda el puntaje del quiz"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        puntos = int(data.get('puntos', 0))
        
        if not nombre or len(nombre) < 2:
            return JsonResponse({'error': 'Nombre inválido'}, status=400)
        
        if puntos < 0:
            return JsonResponse({'error': 'Puntos inválidos'}, status=400)
        
        # SIEMPRE guardar la jugada (historial completo)
        puntaje = PuntajeJuego.objects.create(
            nombre=nombre[:50],
            puntos=puntos,
            tipo_juego='quiz'
        )
        
        # Verificar si es récord personal
        mejor_anterior = PuntajeJuego.objects.filter(
            nombre__iexact=nombre,
            tipo_juego='quiz'
        ).exclude(id=puntaje.id).order_by('-puntos').first()
        
        es_record = not mejor_anterior or puntos > mejor_anterior.puntos
        
        # Obtener top 5 (solo el mejor puntaje de cada jugador)
        from django.db.models import Max
        
        # Subconsulta: obtener el max puntaje por cada nombre
        mejores_por_jugador = PuntajeJuego.objects.filter(
            tipo_juego='quiz'
        ).values('nombre').annotate(
            max_puntos=Max('puntos')
        )
        
        # Obtener los registros completos de esos mejores puntajes
        top_5 = []
        nombres_procesados = set()
        
        for item in PuntajeJuego.objects.filter(tipo_juego='quiz').order_by('-puntos', '-fecha'):
            nombre_lower = item.nombre.lower()
            if nombre_lower not in nombres_procesados:
                top_5.append(item)
                nombres_procesados.add(nombre_lower)
                if len(top_5) >= 5:
                    break
        
        # Encontrar posición del jugador (basado en su mejor puntaje)
        mejor_jugador = PuntajeJuego.objects.filter(
            nombre__iexact=nombre,
            tipo_juego='quiz'
        ).order_by('-puntos').first()
        
        # Calcular posición
        mejores_unicos = []
        nombres_vistos = set()
        for p in PuntajeJuego.objects.filter(tipo_juego='quiz').order_by('-puntos', '-fecha'):
            nombre_lower = p.nombre.lower()
            if nombre_lower not in nombres_vistos:
                mejores_unicos.append(p)
                nombres_vistos.add(nombre_lower)
        
        posicion = mejores_unicos.index(mejor_jugador) + 1 if mejor_jugador in mejores_unicos else len(mejores_unicos)
        
        return JsonResponse({
            'success': True,
            'posicion': posicion,
            'es_record': es_record,
            'puntos_mejor': mejor_jugador.puntos if mejor_jugador else puntos,
            'top_5': [
                {'nombre': p.nombre, 'puntos': p.puntos}
                for p in top_5
            ]
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def obtener_leaderboard(request):
    """Obtiene el top 5 del leaderboard"""
    tipo = request.GET.get('tipo', 'quiz')
    top_5 = PuntajeJuego.objects.filter(tipo_juego=tipo)[:5]
    
    return JsonResponse({
        'top_5': [
            {'nombre': p.nombre, 'puntos': p.puntos}
            for p in top_5
        ]
    })

@require_POST
def guardar_puntaje_clasifica(request):
    """Guarda el puntaje del juego clasifica residuos"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        puntos = int(data.get('puntos', 0))
        
        if not nombre or len(nombre) < 2:
            return JsonResponse({'error': 'Nombre inválido'}, status=400)
        
        if puntos < 0:
            return JsonResponse({'error': 'Puntos inválidos'}, status=400)
        
        # SIEMPRE guardar la jugada (historial completo)
        puntaje = PuntajeJuego.objects.create(
            nombre=nombre[:50],
            puntos=puntos,
            tipo_juego='arrastrar'  # ← IMPORTANTE: tipo diferente
        )
        
        # Verificar si es récord personal
        mejor_anterior = PuntajeJuego.objects.filter(
            nombre__iexact=nombre,
            tipo_juego='arrastrar'
        ).exclude(id=puntaje.id).order_by('-puntos').first()
        
        es_record = not mejor_anterior or puntos > mejor_anterior.puntos
        
        # Obtener top 5 (solo el mejor puntaje de cada jugador)
        top_5 = []
        nombres_procesados = set()
        
        for item in PuntajeJuego.objects.filter(tipo_juego='arrastrar').order_by('-puntos', '-fecha'):
            nombre_lower = item.nombre.lower()
            if nombre_lower not in nombres_procesados:
                top_5.append(item)
                nombres_procesados.add(nombre_lower)
                if len(top_5) >= 5:
                    break
        
        # Encontrar posición del jugador
        mejor_jugador = PuntajeJuego.objects.filter(
            nombre__iexact=nombre,
            tipo_juego='arrastrar'
        ).order_by('-puntos').first()
        
        # Calcular posición
        mejores_unicos = []
        nombres_vistos = set()
        for p in PuntajeJuego.objects.filter(tipo_juego='arrastrar').order_by('-puntos', '-fecha'):
            nombre_lower = p.nombre.lower()
            if nombre_lower not in nombres_vistos:
                mejores_unicos.append(p)
                nombres_vistos.add(nombre_lower)
        
        posicion = mejores_unicos.index(mejor_jugador) + 1 if mejor_jugador in mejores_unicos else len(mejores_unicos)
        
        return JsonResponse({
            'success': True,
            'posicion': posicion,
            'es_record': es_record,
            'puntos_mejor': mejor_jugador.puntos if mejor_jugador else puntos,
            'top_5': [
                {'nombre': p.nombre, 'puntos': p.puntos}
                for p in top_5
            ]
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)