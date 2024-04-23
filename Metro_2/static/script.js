// Function to update sensor data on the webpage
function updateSensorData(data) {
    document.getElementById('people-count').innerText = data.people_count;
    document.getElementById('fire-alert').innerText = data.fire_alert_status;
}

// Function to update station information on the webpage
function updateStationInfo(data) {
    document.getElementById('current-station').innerText = data.current_station;
    document.getElementById('next-station').innerText = data.next_station;
}

// Function to fetch sensor data from the server
function fetchSensorData() {
    fetch('/data')
    .then(response => response.json())
    .then(data => {
        updateSensorData(data);
        updateStationInfo(data);
    });
}

// Function to update sensor data periodically
function updateDataPeriodically() {
    setInterval(fetchSensorData, 5000); // Update every 5 seconds
}

// Update sensor data when the page loads
window.onload = function() {
    fetchSensorData(); // Fetch initial data
    updateDataPeriodically(); // Update data periodically
};
