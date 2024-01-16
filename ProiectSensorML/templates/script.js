function updateChart() {
    var selectedParameter = document.getElementById("parameter").value;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            temperature: selectedParameter === 'temp1' ? 1 : 0,
            humidity: selectedParameter === 'umid' ? 1 : 0,
            light: 0,
            pressure: 0,
            soil_moisture: 0
        })
    })
    .then(response => response.json())
    .then(predictions => {
        drawChart(predictions);
    })
    .catch(error => console.error('Error:', error));
}

function drawChart(predictions) {
    var ctx = document.getElementById('sensorChart').getContext('2d');

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
                x: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            }
        }
    });
}

// Alte funcții sau cod suplimentar pot fi adăugate aici
