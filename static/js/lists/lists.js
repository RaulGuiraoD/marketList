/**
 * MarketList - Shopping List Operations
 * Añadir sugerencias frecuentes y control asíncrono de cantidades por pulsación prolongada.
 */

function addFromSugerencia(nombre) {
    const input = document.getElementById('inputProducto');
    const form = document.getElementById('formAdd');
    
    if (!input || !form) return;
    
    input.value = nombre;
    form.submit();
    if (typeof showToast === 'function') {
        showToast("Producto añadido: " + nombre);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    let intervalId = null;
    let timeoutId = null;

    function startUpdating(button) {
        ejecutarCambio(button);

        // Retardo de 500ms para confirmar acción de mantener pulsado en móviles/ratón
        timeoutId = setTimeout(() => {
            intervalId = setInterval(() => {
                ejecutarCambio(button);
            }, 150);
        }, 500);
    }

    function stopUpdating() {
        clearTimeout(timeoutId);
        clearInterval(intervalId);
    }

    function ejecutarCambio(button) {
        const url = button.getAttribute('data-url');
        const itemId = button.getAttribute('data-item-id');
        const spanCantidad = document.getElementById(`cantidad-${itemId}`);

        if (!url || !spanCantidad) return;

        fetch(url, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.nueva_cantidad !== undefined) {
                spanCantidad.innerText = data.nueva_cantidad;
                
                // Efecto de escala elástico temporal
                spanCantidad.classList.add('scale-up');
                setTimeout(() => spanCantidad.classList.remove('scale-up'), 100);
            }
        })
        .catch(error => console.error('Error al actualizar unidades:', error));
    }

    // Configuración de listeners híbridos (Touch + Mouse)
    document.querySelectorAll('.btn-cantidad').forEach(button => {
        button.addEventListener('click', (e) => e.preventDefault());

        button.addEventListener('mousedown', () => startUpdating(button));
        button.addEventListener('touchstart', (e) => {
            e.preventDefault(); 
            startUpdating(button);
        });

        button.addEventListener('mouseup', stopUpdating);
        button.addEventListener('mouseleave', stopUpdating);
        button.addEventListener('touchend', stopUpdating);
        button.addEventListener('touchcancel', stopUpdating);
    });
});