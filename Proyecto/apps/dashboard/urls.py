from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/cambiar-username/', views.cambiar_username_view, name='cambiar_username'),
]