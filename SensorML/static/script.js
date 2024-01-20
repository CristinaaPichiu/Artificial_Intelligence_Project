$(document).ready(function() {
    $('#method_type').change(function() {
        $('#method_type option[value=""]').remove();

        var selectedMethod = $(this).val();
        if (selectedMethod === 'Prophet') {
            var dropdownHtml = `
                <div class="form-group">
                    <label for="parameter_type">Select Parameter for Visualization:</label>
                    <select class="form-control" name="parameter_type" id="parameter_type">
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
        } else if (selectedMethod === 'Seq2Seq'){
            var dropdownHtml3 = `
                <div class="form-group">
                    <label for="parameter_type">Select Parameter for Visualization:</label>
                    <select class="form-control" name="parameter_type" id="parameter_type">
                        <!-- Opțiunile pentru Seq2Seq -->
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
            $('#parameter-dropdown-placeholder').html(dropdownHtml3);
        } else if (selectedMethod === 'RN'){
            var dropdownHtml2 = `
                <div class="form-group">
                    <label for="parameter_type">Select Parameter for Visualization:</label>
                    <select class="form-control" name="parameter_type" id="parameter_type">
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
            $('#parameter-dropdown-placeholder').html(dropdownHtml2);
        } else {
            $('#parameter-dropdown-placeholder').empty();
        }
    });
});

document.getElementById('method_type').addEventListener('change', function() {
    updateParameterDropdown(this.value);
});

