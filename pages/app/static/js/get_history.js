window.onload = function() {
    const username = document.body.getAttribute('data-username');

    if(username) {
        fetchHistoricalData(username);
        fetchPredictionData(username);
    } else {
        console.log('No user logged in');
    }
};

function fetchHistoricalData(username) {
    fetch(`/historical_data_history/${username}`)
        .then(response => response.json())
        .then(data => displayHistoricalData(data))
        .catch(error => console.error('Failed to fetch historical data:', error));
}

function fetchPredictionData(username) {
    fetch(`/prediction_history/${username}`)
        .then(response => response.json())
        .then(data => displayPredictionData(data))
        .catch(error => console.error('Failed to fetch prediction data:', error));
}
function displayHistoricalData(data) {
    const container = document.getElementById('historical-data-container');
    container.innerHTML = ''; // Clear previous entries
    data.forEach((item, index) => {
        const barDiv = document.createElement('div');
        barDiv.id = `historicalBar${index}`; // Unique ID for the bar
        barDiv.className = 'data-bar';
        const request = item.request_data;
        const response = item.response_data;
        const rates = Object.entries(response.rates).map(([currency, value]) => `${currency}: ${value}`).join(', ');

        barDiv.innerHTML = `Date: ${request.date}, Base Currency: ${request.base_currency}, Target Currency: ${request.target_currency}, Rates: ${rates} <button onclick='deleteHistoricalData(${index})'>Delete</button>`;
        container.appendChild(barDiv);
    });
}

function displayPredictionData(data) {
    const container = document.getElementById('prediction-data-container');
    container.innerHTML = ''; // Clear previous entries
    window.graphs = []; // Initialize an array to hold multiple Chart instances

    data.forEach((item, index) => {
        const timestamp = new Date(item.timestamp);
        const formattedTimestamp = timestamp.toLocaleString(); // Adjust formatting as needed

        const summaryDiv = document.createElement('div');
        summaryDiv.id = `predictionBar${index}`; // Unique ID for the bar
        summaryDiv.className = 'data-bar';
        summaryDiv.innerHTML = `<strong>Saved on:</strong> ${formattedTimestamp}, <strong>Date:</strong> ${item.data.future_date}, <strong>Base Currency:</strong> ${item.data.base_currency}, <strong>Target Currency:</strong> ${item.data.target_currency}, <strong>Rate:</strong> ${item.data.predictions[0].prediction.toFixed(4)} <button onclick='deletePrediction(${index})'>Delete</button>`;

        const detailDiv = document.createElement('div');
        detailDiv.className = 'details';
        const predictionsText = item.data.predictions.map(p => `${p.prediction.toFixed(4)}`).join(', ');
        detailDiv.textContent = `Predictions: ${predictionsText}`;

        const graphContainer = document.createElement('canvas');
        graphContainer.id = `predictionGraph${index}`;
        graphContainer.className = 'graph-container';

        const expandButton = document.createElement('button');
        expandButton.textContent = 'Expand/Compress';
        expandButton.onclick = () => { detailDiv.classList.toggle('active-details'); };

        const graphButton = document.createElement('button');
        graphButton.textContent = 'Generate Graph/Hide Graph';
        graphButton.onclick = () => {
            const isGraphVisible = graphContainer.classList.contains('active-graph');
            graphContainer.classList.toggle('active-graph');
            if (isGraphVisible && window.graphs[index]) {
                window.graphs[index].destroy();
                window.graphs[index] = null; // Clear the stored graph instance
            } else if (!window.graphs[index]) {
                window.graphs[index] = displayGraph(item.data.predictions.map(p => p.prediction), graphContainer.id);
            }
        };

        summaryDiv.appendChild(expandButton);
        summaryDiv.appendChild(graphButton);
        container.appendChild(summaryDiv);
        container.appendChild(detailDiv);
        container.appendChild(graphContainer);
    });
}



function displayGraph(predictions, canvasId) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: predictions.map((_, index) => `Forecast ${index + 1}`),
            datasets: [{
                label: 'Currency Prediction',
                data: predictions,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}
