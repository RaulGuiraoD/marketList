document.addEventListener("DOMContentLoaded", function() {
    const budgetBar = document.getElementById("budget-bar");
    if (budgetBar) {
        let rawPercentage = budgetBar.getAttribute("data-percentage");
        
        // Convertir comas en puntos por si Django localiza el número, y limpiar espacios
        rawPercentage = rawPercentage.replace(',', '.').trim();
        
        // Parsear a número flotante real
        const percentage = parseFloat(rawPercentage);

        // Validar que realmente sea un número antes de aplicar el estilo
        if (!isNaN(percentage)) {
            const finalWidth = Math.min(percentage, 100);
            setTimeout(() => {
                budgetBar.style.width = finalWidth + "%";
            }, 150);
        } else {
            console.error("SwiftList Error: El porcentaje de estadísticas no es un número válido:", rawPercentage);
        }
    }
});