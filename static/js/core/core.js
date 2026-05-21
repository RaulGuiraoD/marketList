/**
 * MarketList - Core Utilities
 * Manejo de alertas globales y toasts compartidos.
 */

// Sistema global de notificaciones Toasts
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

// Desvanecimiento automático de los mensajes de Django de la base común
document.addEventListener('DOMContentLoaded', function () {
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