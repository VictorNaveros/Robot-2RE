from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    # Qué columnas se ven en la lista de usuarios
    list_display = ['username','documento', 'first_name', 'last_name', 'is_active']
    
    # Por qué campos se puede buscar
    search_fields = ['username','documento', 'first_name', 'last_name', 'email']
    
    # Cómo se ordenan los usuarios
    ordering = ['documento']
    
    # Campos al EDITAR un usuario
    fieldsets = (
        ('Información Personal', {
            'fields': ('username','documento', 'first_name', 'last_name', 'email')
        }),
        ('Contraseña', {
            'fields': ('password',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
    )
    
    # Campos al CREAR un nuevo usuario
    add_fieldsets = (
        ('Información del Usuario', {
            'fields': ('username','documento', 'first_name', 'last_name', 'email', 'password1', 'password2')
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)
