from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache  # ← agregar
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from apps.login.models import Usuario
from apps.telemetria.views import obtener_datos_dashboard

@never_cache
@login_required
def dashboard_view(request):
    datos_telemetria = obtener_datos_dashboard(request)
    return render(request, 'dashboard/dashboard.html', datos_telemetria)

@never_cache
@login_required
def cambiar_username_view(request):
    if request.method == 'POST':
        nuevo_username = request.POST.get('nuevo_username')
        if not nuevo_username or len(nuevo_username.strip()) == 0:
            messages.error(request, 'El nombre de usuario no puede estar vacío')
        elif Usuario.objects.filter(username=nuevo_username).exclude(id=request.user.id).exists():
            messages.error(request, 'Este nombre de usuario ya está en uso')
        else:
            request.user.username = nuevo_username
            request.user.save()
            messages.success(request, 'Nombre de usuario actualizado exitosamente')
            return redirect('perfil')
    return redirect('perfil')

@never_cache
@login_required
def perfil_view(request):
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirmar = request.POST.get('password_confirmar')
        
        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta')
        elif password_nueva != password_confirmar:
            messages.error(request, 'Las contraseñas nuevas no coinciden')
        elif len(password_nueva) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
        else:
            request.user.set_password(password_nueva)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Contraseña actualizada exitosamente')
            return redirect('perfil')
    
    return render(request, 'dashboard/perfil.html')