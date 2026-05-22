document.addEventListener("DOMContentLoaded", function() {
    const budgetBar = document.getElementById("budget-bar");
    if (budgetBar) {
        const percentage = budgetBar.getAttribute("data-percentage");
        // Asegura que no rompa el contenedor si el porcentaje supera el 100%
        const finalWidth = Math.min(percentage, 100);
        setTimeout(() => {
            budgetBar.style.width = finalWidth + "%";
        }, 150);
    }
});