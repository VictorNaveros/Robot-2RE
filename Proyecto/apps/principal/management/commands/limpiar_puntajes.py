from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.principal.models import PuntajeJuego

class Command(BaseCommand):
    help = 'Limpia puntajes antiguos de juegos manteniendo el mejor de cada jugador'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dias',
            type=int,
            default=7,
            help='Días de antigüedad para eliminar (default: 7)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular sin borrar realmente'
        )

    def handle(self, *args, **options):
        dias = options['dias']
        dry_run = options['dry_run']
        
        fecha_limite = timezone.now() - timedelta(days=dias)
        
        self.stdout.write(self.style.WARNING(f'\n🧹 Limpiando puntajes de juegos anteriores a {fecha_limite.strftime("%Y-%m-%d %H:%M")}...\n'))
        
        # Obtener todos los jugadores únicos (nombre + tipo_juego)
        jugadores = PuntajeJuego.objects.values('nombre', 'tipo_juego').distinct()
        
        total_eliminados = 0
        total_conservados = 0
        jugadores_procesados = 0
        
        for jugador in jugadores:
            nombre = jugador['nombre']
            tipo = jugador['tipo_juego']
            
            # Obtener todos los puntajes de este jugador en este juego
            puntajes = PuntajeJuego.objects.filter(
                nombre__iexact=nombre,
                tipo_juego=tipo
            ).order_by('-puntos', '-fecha')
            
            total_puntajes = puntajes.count()
            
            if total_puntajes <= 1:
                # Solo tiene 1 registro, conservarlo siempre
                total_conservados += 1
                continue
            
            # Obtener el mejor (récord actual)
            mejor = puntajes.first()
            
            # Buscar registros antiguos (excluyendo el mejor)
            antiguos = puntajes.filter(
                fecha__lt=fecha_limite
            ).exclude(id=mejor.id)
            
            count = antiguos.count()
            
            if count > 0:
                jugadores_procesados += 1
                
                if not dry_run:
                    # Borrar realmente
                    antiguos.delete()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✓ {nombre} ({tipo}): Eliminados {count} registros antiguos, conservado récord de {mejor.puntos} pts'
                        )
                    )
                else:
                    # Solo simular
                    self.stdout.write(
                        self.style.WARNING(
                            f'  [SIMULACIÓN] {nombre} ({tipo}): Se eliminarían {count} registros antiguos'
                        )
                    )
                
                total_eliminados += count
            
            total_conservados += 1
        
        # Resumen final
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\n✓ Limpieza completada:\n'))
        self.stdout.write(f'  📊 Jugadores procesados: {jugadores_procesados}')
        self.stdout.write(f'  🗑️  Registros eliminados: {total_eliminados}')
        self.stdout.write(f'  💾 Récords conservados: {total_conservados}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f'\n⚠️  Esto fue una SIMULACIÓN (--dry-run)'))
            self.stdout.write(self.style.WARNING(f'   Ejecuta sin --dry-run para borrar realmente\n'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✅ Limpieza real ejecutada exitosamente\n'))