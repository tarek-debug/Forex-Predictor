function fetchData() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const baseCurrency = document.getElementById('base-currency').value.toUpperCase();
    const targetCurrency = document.getElementById('target-currency').value.toUpperCase();

    const url = `https://api.frankfurter.app/${startDate}..${endDate}?from=${baseCurrency}&to=${targetCurrency}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function displayResults(data) {
    const results = document.getElementById('results');
    results.innerHTML = '<h4>Results:</h4>' + JSON.stringify(data, null, 2);
}
