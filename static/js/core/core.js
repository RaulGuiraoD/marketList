/**
 * MarketList - Core Utilities
 * Manejo de alertas globales, toasts y modales de borrado común.
 */

// Variable de persistencia para el formulario que se va a procesar en el modal
let formToSubmit = null;

/**
 * Lanza el modal de confirmación interceptando el envío de un formulario estándar
 */
function confirmDelete(event, element, message) {
    event.preventDefault();
    formToSubmit = element.closest('form');
    
    const msgElement = document.getElementById('deleteConfirmMessage');
    if (msgElement) msgElement.innerText = message;
    
    const modalElement = document.getElementById('deleteConfirmModal');
    if (modalElement) {
        const myModal = new bootstrap.Modal(modalElement);
        myModal.show();
    }
}

// Inicialización de Toasts y Desvanecimiento automático de Alertas Django
document.addEventListener('DOMContentLoaded', function () {
    
    // Vinculación del botón definitivo del modal de borrado
    const btnConfirm = document.getElementById('btnConfirmDelete');
    if (btnConfirm) {
        btnConfirm.addEventListener('click', function () {
            if (formToSubmit) {
                const modalEl = document.getElementById('deleteConfirmModal');
                const instance = bootstrap.Modal.getInstance(modalEl);
                if (instance) instance.hide();
                
                formToSubmit.submit();
            }
        });
    }

    // Desvanecimiento de mensajes flash
    const messageContainer = document.getElementById('messages-container');
    if (messageContainer) {
        setTimeout(function () {
            messageContainer.style.transition = "opacity 0.8s ease";
            messageContainer.style.opacity = "0";

            setTimeout(function () {
                messageContainer.remove();
            }, 800);
        }, 2000);
    }
});

// Sistema de alertas Toast dinámicas
function showToast(message, isError = false) {
    const toastElement = document.getElementById('liveToast');
    const toastBody = document.getElementById('toastMessage');

    if (!toastElement || !toastBody) return;

    toastBody.innerText = message;

    if (isError) {
        toastElement.classList.add('bg-danger-custom');
    } else {
        toastElement.classList.remove('bg-danger-custom');
    }

    const toast = new bootstrap.Toast(toastElement, { delay: 2500 });
    toast.show();
}