from django.contrib import admin
from .models import PuntajeJuego

@admin.register(PuntajeJuego)
class PuntajeJuegoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'puntos', 'tipo_juego', 'fecha', 'id']
    list_filter = ['tipo_juego', 'fecha', 'nombre']
    search_fields = ['nombre']
    ordering = ['-fecha']  # Más recientes primero
    
    def get_queryset(self, request):
        # Mostrar TODOS los registros (historial completo)
        return super().get_queryset(request)