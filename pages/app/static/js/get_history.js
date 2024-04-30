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
    data.forEach(item => {
        const div = document.createElement('div');
        div.textContent = `Date: ${item.data.date}, Base Currency: ${item.data.base_currency}, Target Currency: ${item.data.target_currency}`;
        container.appendChild(div);
    });
}

function displayPredictionData(data) {
    const container = document.getElementById('prediction-data-container');
    container.innerHTML = ''; // Clear previous entries
    data.forEach(item => {
        const div = document.createElement('div');
        div.textContent = `Date: ${item.data.future_date}, Base Currency: ${item.data.base_currency}, Target Currency: ${item.data.target_currency}, Prediction: ${item.data.predictions.map(p => p.prediction).join(', ')}`;
        container.appendChild(div);
    });
}
