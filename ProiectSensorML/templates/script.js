document.addEventListener('DOMContentLoaded', function() {
    fetchDataAndRenderChart();
});

function updateChart() {
    const selectedParameter = document.getElementById('parameter').value;
    fetchDataAndRenderChart(selectedParameter);
}

function fetchDataAndRenderChart(selectedParameter = 'temp1') {
    fetch(`http://localhost:5000/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            temperature: /* Valoare corespunzatoare */,
            humidity: /* Valoare corespunzatoare */,
            light: /* Valoare corespunzatoare */,
            pressure: /* Valoare corespunzatoare */,
            soil_moisture: /* Valoare corespunzatoare */
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        renderChart(data, selectedParameter);
    })
    .catch(error => console.error('Error:', error));
}


function renderChart(data, selectedParameter) {
    const ctx = document.getElementById('sensorChart').getContext('2d');
    if(window.sensorChart) {
        window.sensorChart.destroy();
    }
    window.sensorChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: /* Adaugă timestamp-urile aici */,
            datasets: [{
                label: selectedParameter,
                data: data.predictions[0],  // Adjust this based on your model's output structure
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
