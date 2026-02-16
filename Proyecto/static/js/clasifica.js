// Banco de objetos del juego
const objetos = [
    // Orgánicos
    { icono: '🍎', nombre: 'Manzana', tipo: 'organico' },
    { icono: '🍌', nombre: 'Plátano', tipo: 'organico' },
    { icono: '🥕', nombre: 'Zanahoria', tipo: 'organico' },
    { icono: '🍞', nombre: 'Pan', tipo: 'organico' },
    { icono: '🌽', nombre: 'Maíz', tipo: 'organico' },
    { icono: '🥔', nombre: 'Papa', tipo: 'organico' },
    { icono: '🍊', nombre: 'Naranja', tipo: 'organico' },
    { icono: '🥬', nombre: 'Lechuga', tipo: 'organico' },
    
    // Reciclables
    { icono: '📰', nombre: 'Periódico', tipo: 'reciclable' },
    { icono: '📦', nombre: 'Caja de cartón', tipo: 'reciclable' },
    { icono: '🥫', nombre: 'Lata de aluminio', tipo: 'reciclable' },
    { icono: '🍶', nombre: 'Botella de vidrio', tipo: 'reciclable' },
    { icono: '📄', nombre: 'Papel', tipo: 'reciclable' },
    { icono: '🧃', nombre: 'Tetra pak', tipo: 'reciclable' },
    { icono: '🗂️', nombre: 'Carpeta', tipo: 'reciclable' },
    { icono: '📚', nombre: 'Revista', tipo: 'reciclable' },
    
    // No reciclables
    { icono: '🍼', nombre: 'Biberón usado', tipo: 'no-reciclable' },
    { icono: '🧷', nombre: 'Pañal', tipo: 'no-reciclable' },
    { icono: '🧻', nombre: 'Papel higiénico', tipo: 'no-reciclable' },
    { icono: '🔋', nombre: 'Pila', tipo: 'no-reciclable' },
    { icono: '💊', nombre: 'Medicamento', tipo: 'no-reciclable' },
    { icono: '🧴', nombre: 'Envase de químicos', tipo: 'no-reciclable' },
    { icono: '🧽', nombre: 'Esponja usada', tipo: 'no-reciclable' },
];

// Variables del juego
let nombreJugador = '';
let puntosActuales = 0;
let objetosRestantes = 15;
let tiempoRestante = 60;
let temporizador = null;
let objetosJuego = [];
let objetoActualIndex = 0;
let juegoFinalizado = false;  // ← NUEVA VARIABLE

// Función para obtener el CSRF token (igual que en quiz.js)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Permitir Enter para iniciar el juego
document.addEventListener('DOMContentLoaded', function() {
    const inputNombre = document.getElementById('nombre-jugador-clasifica');
    if (inputNombre) {
        inputNombre.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                iniciarClasifica();
            }
        });
    }
});

// Función para iniciar el juego
function iniciarClasifica() {
    const input = document.getElementById('nombre-jugador-clasifica');
    const nombre = input.value.trim();
    
    if (nombre.length < 2) {
        document.getElementById('error-nombre-clasifica').classList.remove('hidden');
        input.focus();
        return;
    }
    
    nombreJugador = nombre;
    
    // Seleccionar 15 objetos aleatorios
    objetosJuego = seleccionarObjetosAleatorios(15);
    
    // Ocultar pantalla de inicio, mostrar juego
    document.getElementById('screen-inicio-clasifica').classList.add('hidden');
    document.getElementById('screen-juego-clasifica').classList.remove('hidden');
    
    // Mostrar primer objeto
    mostrarObjeto();
    
    // Iniciar temporizador
    iniciarTemporizador();
}

// Función para seleccionar objetos aleatorios
function seleccionarObjetosAleatorios(cantidad) {
    const shuffled = [...objetos].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, cantidad);
}

// Función para mostrar el objeto actual
function mostrarObjeto() {
    if (objetoActualIndex >= objetosJuego.length) {
        // Terminó el juego
        finalizarJuego();
        return;
    }
    
    const objeto = objetosJuego[objetoActualIndex];
    document.getElementById('objeto-icono').textContent = objeto.icono;
    document.getElementById('objeto-nombre').textContent = objeto.nombre;
    
    // Actualizar contador
    document.getElementById('objetos-restantes').textContent = objetosRestantes;
}

// Función para iniciar el temporizador
function iniciarTemporizador() {
    tiempoRestante = 60;
    document.getElementById('tiempo-restante').textContent = tiempoRestante + 's';
    
    if (temporizador) clearInterval(temporizador);
    
    temporizador = setInterval(() => {
        tiempoRestante--;
        document.getElementById('tiempo-restante').textContent = tiempoRestante + 's';
        
        // Cambiar color según tiempo
        const tiempoDiv = document.getElementById('tiempo-restante');
        if (tiempoRestante <= 10) {
            tiempoDiv.classList.add('text-red-600');
            tiempoDiv.classList.remove('text-orange-600');
        } else if (tiempoRestante <= 30) {
            tiempoDiv.classList.add('text-orange-600');
            tiempoDiv.classList.remove('text-green-600');
        }
        
        if (tiempoRestante <= 0) {
            clearInterval(temporizador);
            finalizarJuego();
        }
    }, 1000);
}

// Funciones de drag and drop
function allowDrop(ev) {
    ev.preventDefault();
    // Agregar efecto visual al pasar sobre el contenedor
    ev.target.closest('.contenedor').classList.add('scale-105', 'border-dashed');
}

function dragLeave(ev) {
    // Quitar efecto visual
    ev.target.closest('.contenedor').classList.remove('scale-105', 'border-dashed');
}

function drag(ev) {
    ev.dataTransfer.setData("objetoIndex", objetoActualIndex);
}

function drop(ev, tipoContenedor) {
    ev.preventDefault();
    
    // Quitar efectos visuales
    const contenedor = ev.target.closest('.contenedor');
    contenedor.classList.remove('scale-105', 'border-dashed');
    
    const objeto = objetosJuego[objetoActualIndex];
    
    // Verificar si es correcto
    if (objeto.tipo === tipoContenedor) {
        // ¡Correcto!
        puntosActuales += 15;
        mostrarFeedback(contenedor, true);
    } else {
        // Incorrecto
        puntosActuales -= 5;
        if (puntosActuales < 0) puntosActuales = 0;
        mostrarFeedback(contenedor, false);
    }
    
    // Actualizar puntos
    document.getElementById('puntos-clasifica').textContent = puntosActuales;
    
    // Siguiente objeto
    objetoActualIndex++;
    objetosRestantes--;
    
    setTimeout(() => {
        mostrarObjeto();
    }, 1000);
}

// Función para mostrar feedback visual
function mostrarFeedback(contenedor, esCorrecto) {
    if (esCorrecto) {
        contenedor.classList.add('bg-green-300', 'border-green-600');
        
        // Mostrar ✓
        const check = document.createElement('div');
        check.className = 'absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-8xl';
        check.textContent = '✓';
        contenedor.style.position = 'relative';
        contenedor.appendChild(check);
        
        setTimeout(() => {
            contenedor.classList.remove('bg-green-300', 'border-green-600');
            check.remove();
        }, 1000);
    } else {
        contenedor.classList.add('bg-red-300', 'border-red-600');
        
        // Mostrar ✗
        const cross = document.createElement('div');
        cross.className = 'absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-8xl';
        cross.textContent = '✗';
        contenedor.style.position = 'relative';
        contenedor.appendChild(cross);
        
        setTimeout(() => {
            contenedor.classList.remove('bg-red-300', 'border-red-600');
            cross.remove();
        }, 1000);
    }
}

// Función para finalizar el juego
async function finalizarJuego() {
    // Evitar ejecución múltiple
    if (juegoFinalizado) return;
    juegoFinalizado = true;
    
    clearInterval(temporizador);
    
    // Ocultar juego, mostrar resultados
    document.getElementById('screen-juego-clasifica').classList.add('hidden');
    document.getElementById('screen-resultados-clasifica').classList.remove('hidden');
    
    // Mostrar puntos finales
    document.getElementById('puntos-finales-clasifica').textContent = puntosActuales;
    
    // Determinar icono según puntaje
    const icono = document.getElementById('resultado-icono-clasifica');
    if (puntosActuales >= 200) {
        icono.textContent = '🏆';
    } else if (puntosActuales >= 150) {
        icono.textContent = '🎉';
    } else if (puntosActuales >= 100) {
        icono.textContent = '😊';
    } else {
        icono.textContent = '📚';
    }
    
    // Guardar puntaje en el servidor
    try {
        const csrftoken = getCookie('csrftoken');
        
        const response = await fetch('/api/guardar-puntaje-clasifica/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                nombre: nombreJugador,
                puntos: puntosActuales
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Mostrar si es récord personal
            if (data.es_record && puntosActuales > 0) {
                const recordDiv = document.createElement('div');
                recordDiv.className = 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white p-6 rounded-2xl mb-6 text-center';
                recordDiv.innerHTML = `
                    <div class="text-4xl mb-2">🎉</div>
                    <div class="text-2xl font-bold">¡Nuevo Récord Personal!</div>
                    <div class="text-lg mt-2">Tu mejor puntaje: ${data.puntos_mejor} pts</div>
                `;
                
                const container = document.getElementById('screen-resultados-clasifica').querySelector('.max-w-2xl');
                container.insertBefore(recordDiv, document.getElementById('posicion-jugador-clasifica'));
            }
            
            // Mostrar posición
            mostrarPosicionClasifica(data.posicion, data.top_5);
        }
        
    } catch (error) {
        console.error('Error al guardar puntaje:', error);
    }
}

// Función para mostrar posición y leaderboard
function mostrarPosicionClasifica(posicion, top5) {
    const posicionDiv = document.getElementById('posicion-jugador-clasifica');
    
    let medalla = '';
    if (posicion === 1) medalla = '👑';
    else if (posicion === 2) medalla = '🥈';
    else if (posicion === 3) medalla = '🥉';
    
    posicionDiv.innerHTML = `
        <div class="text-xl font-bold text-gray-800 mb-2">
            ${medalla} Tu posición: #${posicion}
        </div>
        <div class="text-gray-600">
            ${posicion <= 5 ? '¡Estás en el Top 5!' : '¡Sigue intentando para llegar al Top 5!'}
        </div>
    `;
    
    const leaderboardDiv = document.getElementById('leaderboard-contenedor-clasifica');
    leaderboardDiv.innerHTML = '';
    
    top5.forEach((jugador, index) => {
        const pos = index + 1;
        let insignia = '';
        
        if (pos === 1) insignia = '👑';
        else if (pos === 2) insignia = '🥈';
        else if (pos === 3) insignia = '🥉';
        
        const div = document.createElement('div');
        div.className = 'flex justify-between items-center p-3 bg-white rounded-lg';
        div.innerHTML = `
            <div class="flex items-center gap-3">
                <span class="text-2xl">${insignia}</span>
                <span class="font-semibold">#${pos}</span>
                <span class="text-gray-700">${jugador.nombre}</span>
            </div>
            <span class="font-bold text-orange-600">${jugador.puntos} pts</span>
        `;
        
        leaderboardDiv.appendChild(div);
    });
}
