// Banco de preguntas del quiz
const preguntas = [
    {
        pregunta: "¿En qué contenedor se debe depositar una botella de plástico?",
        opciones: ["Contenedor azul", "Contenedor amarillo", "Contenedor verde", "Contenedor gris"],
        respuestaCorrecta: 1
    },
    {
        pregunta: "¿Qué material NO es reciclable?",
        opciones: ["Papel", "Vidrio", "Pañales desechables", "Cartón"],
        respuestaCorrecta: 2
    },
    {
        pregunta: "¿Cuánto tiempo tarda en degradarse una botella de plástico?",
        opciones: ["10 años", "50 años", "100 años", "450 años"],
        respuestaCorrecta: 3
    },
    {
        pregunta: "¿En qué contenedor se deposita el papel y cartón?",
        opciones: ["Azul", "Amarillo", "Verde", "Gris"],
        respuestaCorrecta: 0
    },
    {
        pregunta: "¿Qué significa el símbolo de reciclaje con un número en el centro?",
        opciones: [
            "El número de veces que se puede reciclar",
            "El tipo de plástico",
            "El peso del objeto",
            "El año de fabricación"
        ],
        respuestaCorrecta: 1
    },
    {
        pregunta: "¿Qué se debe hacer antes de reciclar una lata?",
        opciones: [
            "Pintarla",
            "Enjuagarla",
            "Romperla",
            "Nada especial"
        ],
        respuestaCorrecta: 1
    },
    {
        pregunta: "¿Cuál de estos objetos va en el contenedor orgánico?",
        opciones: [
            "Bolsa de plástico",
            "Cáscaras de frutas",
            "Lata de refresco",
            "Periódico"
        ],
        respuestaCorrecta: 1
    },
    {
        pregunta: "¿Qué color de contenedor se usa para el vidrio?",
        opciones: ["Azul", "Amarillo", "Verde", "Rojo"],
        respuestaCorrecta: 2
    },
    {
        pregunta: "¿Qué es la regla de las 3R?",
        opciones: [
            "Reciclar, Reutilizar, Renovar",
            "Reducir, Reutilizar, Reciclar",
            "Recoger, Revisar, Reciclar",
            "Reparar, Renovar, Reciclar"
        ],
        respuestaCorrecta: 1
    },
    {
        pregunta: "¿Cuánta energía se ahorra al reciclar una lata de aluminio?",
        opciones: ["25%", "50%", "75%", "95%"],
        respuestaCorrecta: 3
    }
];

// Variables del juego
let preguntaActual = 0;
let puntos = 0;
let nombreJugador = "";
let tiempoRestante = 15;
let temporizador = null;

// Función para obtener el CSRF token
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

// Permitir Enter para iniciar el quiz
document.addEventListener('DOMContentLoaded', function() {
    const inputNombre = document.getElementById('nombre-jugador');
    if (inputNombre) {
        inputNombre.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                iniciarQuiz();
            }
        });
    }
});
// Función para iniciar el quiz
function iniciarQuiz() {
    const input = document.getElementById('nombre-jugador');
    const nombre = input.value.trim();

    if (nombre.length < 2) {
        document.getElementById('error-nombre').classList.remove('hidden');
        input.focus();
        return;
    }
    nombreJugador = nombre;
    // Ocultar pantalla de inicio, mostrar quiz
    document.getElementById('screen-inicio').classList.add('hidden');
    document.getElementById('screen-quiz').classList.remove('hidden');

    // Cargar primera pregunta
    mostrarPregunta();
}


// Función para mostrar una pregunta
function mostrarPregunta() {
    const pregunta = preguntas[preguntaActual];

    // Actualizar número de pregunta
    document.getElementById('pregunta-actual').textContent = preguntaActual + 1;

    // Actualizar barra de progreso
    const progreso = ((preguntaActual + 1) / preguntas.length) * 100;
    document.getElementById('barra-progreso').style.width = progreso + '%';

    // Mostrar texto de la pregunta
    document.getElementById('texto-pregunta').textContent = pregunta.pregunta;

    // Crear opciones
    const contenedor = document.getElementById('opciones-contenedor');
    contenedor.innerHTML = '';

    pregunta.opciones.forEach((opcion, index) => {
        const btn = document.createElement('button');
        btn.className = 'w-full text-left p-4 border-2 border-gray-300 rounded-lg hover:border-green-500 hover:bg-green-50 transition font-semibold text-lg';
        btn.textContent = opcion;
        btn.onclick = () => seleccionarRespuesta(index);
        contenedor.appendChild(btn);
    });

    // Iniciar temporizador
    iniciarTemporizador();
}

// Función para iniciar el temporizador
function iniciarTemporizador() {
    tiempoRestante = 15;
    document.getElementById('temporizador').textContent = tiempoRestante;

    if (temporizador) clearInterval(temporizador);

    temporizador = setInterval(() => {
        tiempoRestante--;
        document.getElementById('temporizador').textContent = tiempoRestante;

        if (tiempoRestante <= 0) {
            clearInterval(temporizador);
            // Tiempo agotado, siguiente pregunta sin puntos
            siguientePregunta();
        }
    }, 1000);
}

// Función para seleccionar una respuesta
function seleccionarRespuesta(indice) {
    clearInterval(temporizador);

    const pregunta = preguntas[preguntaActual];
    const botones = document.querySelectorAll('#opciones-contenedor button');

    // Deshabilitar todos los botones y quitar hover
    botones.forEach(btn => {
        btn.disabled = true;
        btn.classList.remove('hover:border-green-500', 'hover:bg-green-50');
        btn.classList.add('cursor-not-allowed');
    });

    // Marcar respuesta correcta e incorrecta
    if (indice === pregunta.respuestaCorrecta) {
        // Respuesta correcta
        botones[indice].classList.remove('border-gray-300');
        botones[indice].classList.add('bg-green-500', 'text-white', 'border-green-600');

        // Calcular puntos (10 base + bonus por velocidad)
        let puntosGanados = 10;
        if (tiempoRestante > 10) {
            puntosGanados += 2; // Bonus por rapidez
        }

        puntos += puntosGanados;
        document.getElementById('puntos-actuales').textContent = puntos;

    } else {
        // Respuesta incorrecta
        botones[indice].classList.remove('border-gray-300');
        botones[indice].classList.add('bg-red-500', 'text-white', 'border-red-600');

        // Mostrar la correcta
        botones[pregunta.respuestaCorrecta].classList.remove('border-gray-300');
        botones[pregunta.respuestaCorrecta].classList.add('bg-green-500', 'text-white', 'border-green-600');
    }

    // Pasar a la siguiente pregunta después de 2 segundos
    setTimeout(() => {
        siguientePregunta();
    }, 2000);
}

// Función para pasar a la siguiente pregunta
function siguientePregunta() {
    preguntaActual++;

    if (preguntaActual < preguntas.length) {
        // Hay más preguntas
        mostrarPregunta();
    } else {
        // Quiz terminado
        mostrarResultados();
    }
}

// Función para mostrar resultados
async function mostrarResultados() {
    // Ocultar quiz, mostrar resultados
    document.getElementById('screen-quiz').classList.add('hidden');
    document.getElementById('screen-resultados').classList.remove('hidden');

    // Mostrar puntos finales
    document.getElementById('puntos-finales').textContent = puntos;

    // Determinar icono según puntaje
    const icono = document.getElementById('resultado-icono');
    if (puntos >= 100) {
        icono.textContent = '🏆';
    } else if (puntos >= 80) {
        icono.textContent = '🎉';
    } else if (puntos >= 60) {
        icono.textContent = '😊';
    } else {
        icono.textContent = '📚';
    }

    // Guardar puntaje en el servidor
    try {
        const csrftoken = getCookie('csrftoken');

        const response = await fetch('/api/guardar-puntaje-quiz/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                nombre: nombreJugador,
                puntos: puntos
            })
        });

        const data = await response.json();

        if (data.success) {
            // Mostrar si es récord personal
            if (data.es_record && puntos > 0) {
                const recordDiv = document.createElement('div');
                recordDiv.className = 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white p-6 rounded-2xl mb-6 text-center';
                recordDiv.innerHTML = `
                    <div class="text-4xl mb-2">🎉</div>
                    <div class="text-2xl font-bold">¡Nuevo Récord Personal!</div>
                    <div class="text-lg mt-2">Tu mejor puntaje: ${data.puntos_mejor} pts</div>
                `;

                const container = document.getElementById('screen-resultados').querySelector('.max-w-2xl');
                container.insertBefore(recordDiv, document.getElementById('posicion-jugador-quiz'));
            }

            // Mostrar posición
            mostrarPosicion(data.posicion, data.top_5);
        }

    } catch (error) {
        console.error('Error al guardar puntaje:', error);
    }
}

// Función para mostrar posición y leaderboard
function mostrarPosicion(posicion, top5) {
    // Mostrar posición del jugador
    const posicionDiv = document.getElementById('posicion-jugador');

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

    // Mostrar leaderboard
    const leaderboardDiv = document.getElementById('leaderboard-contenedor');
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
            <span class="font-bold text-green-600">${jugador.puntos} pts</span>
        `;

        leaderboardDiv.appendChild(div);
    });
}

