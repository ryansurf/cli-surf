
document.getElementById("reportForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    const curlCommand = document.getElementById("curlInput").value;

    // Make an asynchronous HTTP request to the server
    fetch(`http://localhost:8000`, {
        mode: 'no-cors'
    })
    .then(response => response.text())
    .then(data => {
        // Display the response in an alert or any other way you prefer
        alert(data);
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle errors
    });
});
