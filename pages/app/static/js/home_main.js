let myChart = null; // This will hold the chart instance

function fetchData() {
    const baseCurrency = document.getElementById('fromCurrency').value.toUpperCase(); //updated for dropdown
    const targetCurrency = document.getElementById('toCurrency').value.toUpperCase();
    const date = document.querySelector('input[placeholder="YYYY-MM-DD"]').value;

    const url = `https://api.frankfurter.app/${date}?from=${baseCurrency}&to=${targetCurrency}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayResults(data);
            clearGraph(); // Clear the graph when fetching historical data
            // Log both request and response data
            logHistoricalData(baseCurrency, targetCurrency, date, data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function logHistoricalData(baseCurrency, targetCurrency, date, responseData) {
    if (username) { // Check if username is not empty
        const data = {
            username: username,
            base_currency: baseCurrency,
            target_currency: targetCurrency,
            date: date,
            response: responseData // Include the response data
        };

        fetch('/log_historical_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
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
    const baseCurrency = document.getElementById('fromCurrency').value.toUpperCase(); //updated for dropdown
    const targetCurrency = document.getElementById('toCurrency').value.toUpperCase();
    const futureDate = document.querySelector('input[placeholder="YYYY-MM-DD"]').value;

    const predictionData = {
        base_currency: baseCurrency,
        target_currency: targetCurrency,
        future_date: futureDate
    };

    const spinner = document.getElementById('loadingSpinner');
    if (spinner) spinner.style.display = 'block'; // Show the spinner only if it exists

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(predictionData)
    })
    .then(response => response.json())
    .then(data => {
        displayPredictionResults(data);
        displayGraph(data);
        if (spinner) spinner.style.display = 'none'; // Hide the spinner only if it exists
    })
    .catch(error => {
        console.error('Error sending prediction data:', error);
        if (spinner) spinner.style.display = 'none'; // Hide the spinner in case of error, only if it exists
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
