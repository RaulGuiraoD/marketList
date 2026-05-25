/**
 * MarketList - Shopping List Operations
 * Gestion asincrona de productos y cantidades en la lista de compras.
 */

let intervalId = null;
let timeoutId = null;

/**
 * Envia el formulario de adicion de producto via AJAX
 */
function enviarProductoForm(formulario, nombreProducto) {
    const url = formulario.action || window.location.href;
    const formData = new FormData(formulario);

    if (nombreProducto) {
        formData.set('nombre', nombreProducto);
    }

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            recargarListadoItems();

            const input = document.getElementById('inputProducto');
            if (input) {
                input.value = '';
                input.focus(); // Mantiene el teclado abierto en dispositivos moviles
            }

            if (typeof showToast === 'function' && nombreProducto) {
                showToast("Producto añadido: " + nombreProducto);
            }
        }
    })
    .catch(error => console.error('Error al añadir producto:', error));
}

/**
 * Agrega un producto directamente desde el panel de sugerencias frecuentes
 */
function addFromSugerencia(nombre) {
    const form = document.getElementById('formAdd');
    if (!form) return;
    enviarProductoForm(form, nombre);
}

/**
 * Actualiza el contenedor de productos y el contador sin recargar la pagina
 */
function recargarListadoItems() {
    fetch(window.location.href)
    .then(response => response.text())
    .then(htmlTexto => {
        const parser = new DOMParser();
        const docContenido = parser.parseFromString(htmlTexto, 'text/html');

        const nuevoContenedor = docContenido.getElementById('contenedorItems');
        const contenedorActual = document.getElementById('contenedorItems');
        if (nuevoContenedor && contenedorActual) {
            contenedorActual.innerHTML = nuevoContenedor.innerHTML;
        }

        const contadores = document.querySelectorAll('.text-muted.fw-bold.text-uppercase');
        const nuevoContador = docContenido.querySelector('.text-muted.fw-bold.text-uppercase');
        if (nuevoContador && contadores.length > 0) {
            contadores[0].innerHTML = nuevoContador.innerHTML;
        }

        vincularEventosBotonesCantidad();
    })
    .catch(error => console.error('Error al sincronizar vista de items:', error));
}

/**
 * Inicia el temporizador para el incremento/decremento continuo
 */
function startUpdating(button) {
    ejecutarCambio(button);
    timeoutId = setTimeout(() => {
        intervalId = setInterval(() => {
            ejecutarCambio(button);
        }, 150);
    }, 500);
}

/**
 * Detiene los temporizadores de actualizacion automatica
 */
function stopUpdating() {
    clearTimeout(timeoutId);
    clearInterval(intervalId);
}

/**
 * Realiza la peticion asincrona para modificar la cantidad del item
 */
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
            spanCantidad.classList.add('scale-up');
            setTimeout(() => spanCantidad.classList.remove('scale-up'), 100);
        }
    })
    .catch(error => console.error('Error al actualizar unidades:', error));
}

/**
 * Vincula los eventos de pulsacion normal y prolongada a los botones de cantidad
 */
function vincularEventosBotonesCantidad() {
    document.querySelectorAll('.btn-cantidad').forEach(button => {
        button.removeEventListener('click', (e) => e.preventDefault());
        
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
}

/**
 * Inicializacion de listeners principales tras la carga del DOM
 */
document.addEventListener('DOMContentLoaded', function () {
    vincularEventosBotonesCantidad();

    const formAdd = document.getElementById('formAdd');
    if (formAdd) {
        formAdd.addEventListener('submit', function (event) {
            event.preventDefault(); // Detiene el envio tradicional por formulario POST
            enviarProductoForm(formAdd, null);
        });
    }
});