document.addEventListener('DOMContentLoaded', function () {
    const avatarInput = document.getElementById('avatar_input');
    const previewImg = document.getElementById('current-avatar-img');
    const placeholderDiv = document.getElementById('avatar-placeholder');

    if (avatarInput) {
        avatarInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                // Validación estricta de peso en cliente (5MB)
                if (file.size > 5242880) { 
                    if (typeof showToast === 'function') {
                        showToast("La imagen excede los 5MB.", true);
                    } else {
                        alert("La imagen no puede superar los 5MB.");
                    }
                    this.value = "";
                    return;
                }

                // Lector asíncrono de ficheros en tiempo real
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (previewImg) {
                        previewImg.src = e.target.result;
                        previewImg.classList.remove('d-none');
                        previewImg.style.display = 'block'; // Asegura renderizado
                    }
                    if (placeholderDiv) {
                        placeholderDiv.classList.add('d-none');
                        placeholderDiv.style.display = 'none';
                    }
                }
                reader.readAsDataURL(file);
            }
        });
    }
});