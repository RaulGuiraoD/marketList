/**
 * MarketList - User Profile & Dashboard Metrics
 * Renderizado interactivo de selectores de avatar y animación del presupuesto.
 */

document.addEventListener('DOMContentLoaded', function () {
    
    // 1. Manejo del panel selector de avatares interactivos
    const avatarInputs = document.querySelectorAll('.avatar-input');
    const currentAvatarDisplay = document.getElementById('current-avatar');

    avatarInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.checked) {
                if (currentAvatarDisplay) {
                    currentAvatarDisplay.innerText = this.value;
                }

                document.querySelectorAll('.avatar-selector-btn').forEach(btn => {
                    btn.classList.remove('active-avatar');
                });
                this.parentElement.classList.add('active-avatar');
            }
        });
    });

    // 2. Animación de llenado progresivo en barra de estadísticas
    const bar = document.getElementById('budget-bar');
    
    if (bar) {
        // Obtenemos el valor asignado por Django y normalizamos formato decimal local
        let pct = bar.getAttribute('data-percentage').replace(',', '.');
        
        // Inicializamos forzado a cero
        bar.style.setProperty('width', '0%', 'important');

        // Renderizado fluido diferido
        setTimeout(() => {
            bar.style.setProperty('width', pct + '%', 'important');
        }, 300);
    }
});