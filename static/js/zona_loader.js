// Diccionario de zonas con radiación solar
const RADIACION_ANUAL_POR_ZONA = {
    "Costa Caribe": 1643,
    "Región Andina": 1460,
    "Región Pacífica": 1278,
    "Llanos Orientales": 1643,
    "Amazonía": 1278,
    "Desierto de la Guajira": 2190
};

// Función para llenar el <select> con las zonas
function cargarZonas() {
    let select = document.getElementById("ubicacion");

    if (!select) {
        console.error("Error: No se encontró el elemento <select> con id 'ubicacion'");
        return;
    }

    // Limpiar y agregar la opción por defecto
    select.innerHTML = '<option value="">Seleccione una zona...</option>';

    // Agregar las opciones dinámicamente
    Object.keys(RADIACION_ANUAL_POR_ZONA).forEach(zona => {
        let option = document.createElement("option");
        option.value = zona;
        option.textContent = zona;
        select.appendChild(option);
    });
}

// Asegurar que el DOM esté cargado antes de ejecutar
document.addEventListener("DOMContentLoaded", cargarZonas);
