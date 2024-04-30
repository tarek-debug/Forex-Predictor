function deletePrediction(index) {
    fetch(`/delete_prediction/${index}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`predictionBar${index}`).remove(); // Remove the specific bar from the DOM
                showAlert('Prediction deleted successfully.');
            }
        });
}

function clearPredictionHistory() {
    fetch('/clear_predictions', { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('prediction-data-container').innerHTML = ''; // Clear the container
                showAlert('All prediction history cleared.');
            }
        });
}

function deleteHistoricalData(index) {
    fetch(`/delete_historical_data/${index}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`historicalBar${index}`).remove(); // Remove the specific bar from the DOM
                showAlert('Historical data deleted successfully.');
            }
        });
}

function clearHistoricalData() {
    fetch('/clear_historical_data', { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('historical-data-container').innerHTML = ''; // Clear the container
                showAlert('All historical data cleared.');
            }
        });
}

// Utility function to show alert messages
function showAlert(message) {
    // Assuming you have a div with id 'alertContainer' to show alerts
    const alertContainer = document.getElementById('alertContainer');
    alertContainer.innerText = message;
    alertContainer.style.display = 'block'; // Make the alert visible
    setTimeout(() => alertContainer.style.display = 'none', 3000); // Hide after 3 seconds
}
