let myChart = null; // This will hold the chart instance

function fetchData() {
    const baseCurrency = document.querySelector('input[placeholder="From Currency"]').value.toUpperCase();
    const targetCurrency = document.querySelector('input[placeholder="To Currency"]').value.toUpperCase();
    const date = document.querySelector('input[placeholder="YYYY-MM-DD"]').value;

    const url = `https://api.frankfurter.app/${date}?from=${baseCurrency}&to=${targetCurrency}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayResults(data);
            clearGraph(); // Clear the graph when fetching historical data
            // Send the request data for logging
            logHistoricalRequest(baseCurrency, targetCurrency, date);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function logHistoricalRequest(baseCurrency, targetCurrency, date) {
    if (username) { // Check if username is not empty
        const requestData = {
            username: username,
            base_currency: baseCurrency,
            target_currency: targetCurrency,
            date: date
        };

        fetch('/log_historical_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(result => console.log('Historical data logged:', result))
        .catch(error => console.error('Error logging historical data:', error));
    } else {
        console.error('No user logged in');
    }
}


function displayResults(data) {
    const results = document.querySelector('.results');
    results.textContent = JSON.stringify(data, null, 2);
    clearGraph(); // Optionally clear the graph here if needed when displaying results
}

function sendPrediction() {
    console.log("sendPrediction called");
    const baseCurrency = document.querySelector('input[placeholder="From Currency"]').value.toUpperCase();
    const targetCurrency = document.querySelector('input[placeholder="To Currency"]').value.toUpperCase();
    const futureDate = document.querySelector('input[placeholder="YYYY-MM-DD"]').value;

    const predictionData = {
        base_currency: baseCurrency,
        target_currency: targetCurrency,
        future_date: futureDate
    };

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(predictionData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Prediction data received:", data); // Check received data
        displayPredictionResults(data);
        displayGraph(data); // Function to display graph
    })
    .catch(error => {
        console.error('Error sending prediction data:', error);
    });
}

function displayPredictionResults(data) {
    const results = document.querySelector('.results');
    results.innerHTML = ''; // Clear existing results

    if (Array.isArray(data)) {
        const lastPrediction = data[data.length - 1];
        const predictionText = `Last Prediction - Date: ${lastPrediction.date}, Prediction: ${lastPrediction.prediction.toFixed(4)}`;
        const lastResult = document.createElement('div');
        lastResult.textContent = predictionText;
        results.appendChild(lastResult);
    } else {
        // Handle other types of responses (errors, single data points, etc.)
        results.textContent = JSON.stringify(data, null, 2);
    }
}

function displayGraph(data) {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    
    if (myChart) { // Check if the chart instance exists
        myChart.destroy(); // Destroy the existing chart before creating a new one
    }

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => item.date),
            datasets: [{
                label: 'Prediction',
                data: data.map(item => item.prediction),
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

function clearGraph() {
    if (myChart) {
        myChart.destroy(); // Destroy the chart instance
        myChart = null; // Set the chart instance back to null
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const getHistoricalDataButton = document.querySelector('.get-historical-data');
    const predictButton = document.querySelector('.button.predict');

    getHistoricalDataButton.addEventListener('click', fetchData);
    predictButton.addEventListener('click', sendPrediction);
});
