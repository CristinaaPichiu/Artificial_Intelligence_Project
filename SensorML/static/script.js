// script.js
$(document).ready(function() {
    $('#method_type').change(function() {
        $('#method_type option[value=""]').remove();

        var selectedMethod = $(this).val();
        if (selectedMethod === 'Prophet') {
            var dropdownHtml = `
                <div class="form-group">
                    <label for="parameter_type">Select Parameter for Visualization:</label>
                    <select class="form-control" name="parameter_type" id="parameter_type">
                        <option value="Timestamp">Timestamp</option>
                        <option value="pres">Pressure</option>
                        <option value="temp1">Temperature 1</option>
                        <option value="temp2">Temperature 2</option>
                        <option value="umid">Humidity</option>
                        <option value="V450">Violet light at approximately 450 nm</option>
                        <option value="B500">Blue light at approximately 500 nm</option>
                        <option value="G550">Green light at approximately 550 nm</option>
                        <option value="Y570">Yellow light at approximately 570 nm</option>
                        <option value="O600">Orange light at approximately 600 nm</option>
                        <option value="R650">Red light at approximately 650 nm</option>
                        <option value="lumina">Luminosity</option>
                    </select>
                </div>`;
            $('#parameter-dropdown-placeholder').html(dropdownHtml);
        } else {
            $('#parameter-dropdown-placeholder').empty();
        }
    });
});

document.getElementById('method_type').addEventListener('change', function() {
    updateParameterDropdown(this.value);
});
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
