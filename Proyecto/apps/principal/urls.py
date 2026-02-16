from django.urls import path
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.home, name='home'),
    path('sobre-el-robot/', views.sobre_robot, name='sobre_robot'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('el-proyecto/', views.el_proyecto, name='el_proyecto'),
    
    # Juegos
    path('quiz/', views.quiz_reciclaje, name='quiz_reciclaje'),
    path('clasifica/', views.clasifica_residuos, name='clasifica_residuos'),  # ← NUEVO
    
    # APIs
    path('api/guardar-puntaje-quiz/', views.guardar_puntaje_quiz, name='guardar_puntaje_quiz'),
    path('api/guardar-puntaje-clasifica/', views.guardar_puntaje_clasifica, name='guardar_puntaje_clasifica'),  # ← NUEVO
    path('api/leaderboard/', views.obtener_leaderboard, name='obtener_leaderboard'),
]