var myChart = null;
function createDataArray(selectedParameter) {
    var dataArray = [];
    for (var i = 0; i < 24; i++) {
        dataArray.push({
            temperature: selectedParameter === 'temp1' ? 3 : 0,
            humidity: selectedParameter === 'umid' ? 25 : 0,
            light: 23,   // Aceste valori pot fi ajustate în funcție de necesități
            pressure: 98,
            soil_moisture: 213
        });
    }
    return dataArray;
}

function updateChart() {
    var selectedParameter = document.getElementById("parameter").value;
    var dataToSend = createDataArray(selectedParameter);

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => response.json())
    .then(predictions => {
        drawChart(predictions);
    })
    .catch(error => console.error('Error:', error));
}

function drawChart(predictions) {
    var ctx = document.getElementById('sensorChart').getContext('2d');

    if (chart) {
        chart.destroy();  // Distrugerea instanței graficului existent
    }
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: predictions.length }, (_, i) => i + 1),
            datasets: [{
                label: 'Predicted Values',
                data: predictions,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            }
        }
    });
}

// Alte funcții sau cod suplimentar pot fi adăugate aici
