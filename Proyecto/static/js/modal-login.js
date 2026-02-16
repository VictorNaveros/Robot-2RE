function mostrarModalLogin() {
    const modal = document.getElementById('modalLogin');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function cerrarModalLogin() {
    const modal = document.getElementById('modalLogin');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}

function irAlLogin() {
    window.location.href = '/login/';
}

window.onclick = function(event) {
    const modal = document.getElementById('modalLogin');
    if (event.target === modal) {
        cerrarModalLogin();
    }
}