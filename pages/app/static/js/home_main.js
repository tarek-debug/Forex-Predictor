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
    results.innerHTML = ''; // Clear existing results

    if (data && data.base && data.date && data.rates) {
        // Building a list of currency rates
        const ratesList = Object.entries(data.rates).map(([currency, rate]) => {
            return `${currency}: ${rate.toFixed(4)}`; // Format rate to 4 decimal places
        }).join(', ');

        // Create a formatted output
        const formattedData = `
            <h3>Historical Exchange Rates</h3>
            <p style="margin: 2px 0;"><strong>Base Currency:</strong> ${data.base}</p>
            <p style="margin: 2px 0;"><strong>Date:</strong> ${data.date}</p>
            <p style="margin: 2px 0;"><strong>Rates:</strong> ${ratesList}</p>
        `;

        results.innerHTML = formattedData;
    } else {
        results.textContent = "No data available for the selected date and currencies.";
    }
}


function sendPrediction() {
    const baseCurrency = document.getElementById('fromCurrency').value.toUpperCase(); // Using dropdown
    const targetCurrency = document.getElementById('toCurrency').value.toUpperCase();
    const futureDate = document.querySelector('input[placeholder="YYYY-MM-DD"]').value;
    console.log(baseCurrency);
    console.log(targetCurrency);
    console.log(futureDate);

    const predictionData = {
        base_currency: baseCurrency,
        target_currency: targetCurrency,
        future_date: futureDate
    };

    const spinner = document.getElementById('loadingSpinner');
    if (spinner) spinner.style.display = 'block'; // Show the spinner

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
        if (spinner) spinner.style.display = 'none'; // Hide the spinner
    })
    .catch(error => {
        console.error('Error sending prediction data:', error);
        if (spinner) spinner.style.display = 'none'; // Hide the spinner in case of error
    });
}


function displayPredictionResults(data) {
    const results = document.querySelector('.results');
    results.innerHTML = ''; // Clear existing results

    if (Array.isArray(data) && data.length > 0) {
        const lastPrediction = data[data.length - 1];
        const predictionText = `Last Prediction - Date: ${lastPrediction.date}, Prediction: ${lastPrediction.prediction.toFixed(4)}`;
        const lastResult = document.createElement('div');
        lastResult.textContent = predictionText;
        results.appendChild(lastResult);
    } else {
        // Handle errors or no data with a custom message and an emoji
        const errorText = "Oopsies, the prediction failed, please try again later 😔";
        const errorDisplay = document.createElement('div');
        errorDisplay.textContent = errorText;
        errorDisplay.style.color = 'red'; // Change text color to red for errors
        errorDisplay.style.margin = '10px 0';
        errorDisplay.style.fontSize = '16px';
        errorDisplay.style.fontWeight = 'bold';

        // Optionally, add a retry button
        const retryButton = document.createElement('button');
        retryButton.textContent = 'Retry';
        retryButton.style.marginTop = '10px';
        retryButton.addEventListener('click', sendPrediction); // Re-run the prediction function on click

        results.appendChild(errorDisplay);
        results.appendChild(retryButton); // Add the retry button below the error message
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
