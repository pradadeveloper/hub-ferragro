// # Diccionario con la radiación solar por zona (kWh/m²/mes)
const RADIACION_ANUAL_POR_ZONA = {
    "Costa Caribe": 1643,
    "Región Andina": 1460,
    "Región Pacífica": 1278,
    "Llanos Orientales": 1643,
    "Amazonía": 1278,
    "Desierto de la Guajira": 2190
}


function toggleDropdown() {
    document.querySelector(".dropdown-options").classList.toggle("show");
}

function selectOption(name, logo) {
    document.getElementById("selected-text").textContent = name;
    document.getElementById("selected-logo").src = logo;
    document.getElementById("empresa").value = name;  // Guarda el valor real en el input oculto
    document.querySelector(".dropdown-options").classList.remove("show");
}

// Asigna las funciones al objeto global window
window.toggleDropdown = toggleDropdown;
window.selectOption = selectOption;

// Cierra el menú si se hace clic fuera
document.addEventListener("click", function(event) {
    if (!event.target.closest(".custom-dropdown")) {
        document.querySelector(".dropdown-options").classList.remove("show");
    }
});
