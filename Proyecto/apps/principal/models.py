from django.db import models

# Create your models here.

class PuntajeJuego(models.Model):
    TIPO_JUEGO = [
        ('quiz', 'Quiz de Reciclaje'),
        ('arrastrar', 'Clasifica Residuos'),
    ]
    
    nombre = models.CharField(max_length=50)
    puntos = models.IntegerField()
    tipo_juego = models.CharField(max_length=20, choices=TIPO_JUEGO)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-puntos', '-fecha']
        indexes = [
            models.Index(fields=['tipo_juego', '-puntos']),
        ]
    
    def __str__(self):
        return f"{self.nombre} - {self.puntos} pts ({self.tipo_juego})"