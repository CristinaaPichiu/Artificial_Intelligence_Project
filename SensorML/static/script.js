// script.js
function updateChart() {
    var selectedParameter = document.getElementById('parameter').value;

    if (selectedParameter === 'heatmap') {
        // Dacă utilizatorul a selectat heatmap, efectuează acțiunile corespunzătoare
        generateHeatmap();
    } else {
        // Altfel, implementează logica pentru alte tipuri de grafice
        alert('Implementează logica pentru alte tipuri de grafice în funcția updateChart()');
    }
}

function generateHeatmap() {
    // Implementează logica de generare a heatmap-ului și afișează imaginea
    alert('Implementează logica de generare a heatmap-ului și afișează imaginea');
    // Înlocuiește alert-ul cu codul care generează și afișează heatmap-ul
}
