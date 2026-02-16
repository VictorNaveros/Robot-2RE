from django.db import models

class EstadoRobot(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('error', 'Error'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    estado = models.CharField(max_length=20, choices=ESTADOS)
    almacenamiento_pct = models.FloatField(help_text="Porcentaje de almacenamiento")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.estado

class JornadaRobot(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Jornada {self.fecha_inicio}"

class EstadoSensores(models.Model):
    ESTADO_SENSOR = [
        ('ok', 'OK'),
        ('error', 'Error'),
        ('desconectado', 'Desconectado'),
    ]

    camara = models.CharField(max_length=20, choices=ESTADO_SENSOR)
    s_infrarrojo = models.CharField(max_length=20, choices=ESTADO_SENSOR)
    s_ultrasonico = models.CharField(max_length=20, choices=ESTADO_SENSOR)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)




class EventoSensor(models.Model):

    """
    Guarda SOLO cambios de estado de sensores.
    No se insertan valores repetidos consecutivos.
    """

    SENSOR_CHOICES = [
        ('camara', 'Cámara'),
        ('infrarrojo', 'Infrarrojo'),
        ('ultrasonico', 'Ultrasónico'),
        ('presion', 'Presión'),
    ]

    tipo_sensor = models.CharField(
        max_length=20,
        choices=SENSOR_CHOICES
    )

    valor = models.FloatField()

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_sensor} → {self.valor} @ {self.fecha_registro}"

    class Meta:
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['tipo_sensor', '-fecha_registro']),
        ]
