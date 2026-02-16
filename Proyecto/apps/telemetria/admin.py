from django.contrib import admin
from .models import EstadoSensores, EventoSensor,EstadoRobot,JornadaRobot

admin.site.register(EstadoSensores)
admin.site.register(EventoSensor)
admin.site.register(EstadoRobot)
admin.site.register(JornadaRobot)