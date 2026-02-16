function verificarFortalezaPassword(password) {
    let fortaleza = 0;
    let mensaje = '';
    let color = '';
    
    // Criterios de fortaleza
    const tieneLongitud = password.length >= 8;
    const tieneMayuscula = /[A-Z]/.test(password);
    const tieneMinuscula = /[a-z]/.test(password);
    const tieneNumero = /[0-9]/.test(password);
    const tieneEspecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
    
    // Calcular fortaleza
    if (tieneLongitud) fortaleza++;
    if (tieneMayuscula) fortaleza++;
    if (tieneMinuscula) fortaleza++;
    if (tieneNumero) fortaleza++;
    if (tieneEspecial) fortaleza++;
    
    // Determinar nivel
    if (password.length === 0) {
        mensaje = '';
        color = '';
    } else if (fortaleza <= 2) {
        mensaje = '🔴 Débil';
        color = 'text-red-600';
    } else if (fortaleza === 3 || fortaleza === 4) {
        mensaje = '🟡 Media';
        color = 'text-yellow-600';
    } else {
        mensaje = '🟢 Fuerte';
        color = 'text-green-600';
    }
    
    return { mensaje, color };
}

function actualizarIndicadorFortaleza() {
    const passwordInput = document.getElementById('password_nueva');
    const indicador = document.getElementById('indicador-fortaleza');
    
    if (!passwordInput || !indicador) return;
    
    const password = passwordInput.value;
    const { mensaje, color } = verificarFortalezaPassword(password);
    
    // Actualizar el indicador
    indicador.textContent = mensaje;
    indicador.className = `text-sm font-semibold mt-1 ${color}`;
}

// Inicializar cuando cargue la página
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password_nueva');
    
    if (passwordInput) {
        // Escuchar cambios en el input
        passwordInput.addEventListener('input', actualizarIndicadorFortaleza);
        passwordInput.addEventListener('keyup', actualizarIndicadorFortaleza);
    }
});