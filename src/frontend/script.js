// ipAddress = the ip of the machine that is hosting the server

let port;
let ipAddress;

fetch('/config.json', {
    method: 'GET',
    mode: 'no-cors',  // Add the 'no-cors' mode
  })
.then(response => {
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }
  return response.json();
})
.then(config => {
  // Pass the config to another function if needed
  useConfig(config);
})
.catch(error => console.error('Error loading config:', error));

function useConfig(config) {
    port = config["server"]["port"];
    ipAddress = config["server"]["ip_address"];
}


document.getElementById("reportForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission
    

    // Get the value of the location input field
    var location = document.getElementById("curlInput").value;
    location = location.replace(/\s+/g, "_");
    console.log("LOCATION: ", location)

    // Function to handle the response from the HTTP GET request
    function handleResponse(responseText) {
        // Do something with the response, such as updating the UI
        console.log("Response from server:", responseText);
    }

    // Construct the URL with the location query parameter
    var url = `http://${ipAddress}:${port}?location=${encodeURIComponent(location)}`;
    console.log(url);

    // Call httpGetAsync with the URL and the handleResponse function as parameters
    httpGetAsync(url, handleResponse);
});

// Function to make an asynchronous HTTP GET request
function httpGetAsync(theUrl, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}


document.addEventListener("submit", function() {
    // Function to make the HTTP GET request and update the HTML content
    // Function to make the HTTP GET request and update the HTML content
    function fetchDataAndUpdateHTML() {
        // Make the HTTP GET request
        // Get the value of the location input field
        var location = document.getElementById("curlInput").value;
        location = location.replace(/\s+/g, "_");
        fetch(`http://${ipAddress}:${port}?location=${encodeURIComponent(location)}`)
            .then(response => response.text())
            .then(data => {
                // Parse the response text to extract the desired information
                var lines = data.split('\n'); // Split the response into lines
                let extractedData = ''; // Initialize an empty string to store extracted data

                // Loop through each line and extract relevant information
                lines.forEach(line => {
                    if (line.startsWith('Location') ||
                        line.startsWith('UV index') ||
                        line.startsWith('Wave Height') ||
                        line.startsWith('Wave Direction') ||
                        line.startsWith('Wave Period')) {
                        extractedData += line + '<br>'; // Add line to extractedData
                    }
                });

                // Update the content of the serverResponse div with the extracted data
                document.getElementById('serverResponse').innerHTML = extractedData;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }
    // Call the function to fetch data and update HTML content when the form is submitted
    fetchDataAndUpdateHTML();
});




