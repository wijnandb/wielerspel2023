document.addEventListener("DOMContentLoaded", function () {
    // Function to extract RiderID from the URL
    function getRiderIDFromURL() {
      const urlParts = window.location.href.split("/");
      const riderIDIndex = urlParts.indexOf("renners") + 2;
  
      // Check if RiderID is found in the URL
      if (riderIDIndex >= 0 && riderIDIndex < urlParts.length) {
        console.log(urlParts[riderIDIndex])
        return urlParts[riderIDIndex];
      } else {
        return null; // RiderID not found in the URL
      }
    }
  
    // Extract RiderID from the URL
    const riderIDString = getRiderIDFromURL();
    // Convert the string to an integer
    const riderID = parseInt(riderIDString, 10); // Base 10 for decimal numbers

  
    if (riderID) {
      // Fetch the cyclist data and display it based on the RiderID
      fetch("renners.json") // Adjust the path as needed
        .then((response) => response.json())
        .then((data) => {
          const riderData = data.find((item) => item.RiderID === riderID);

          if (riderData) {
            // Fill in the placeholder elements with rider data
            document.getElementById("rider-name").textContent = riderData.Name;
            document.getElementById("rider-team").textContent = riderData.Team;
            document.getElementById("rider-nationality").textContent = riderData.Nationality;
            document.getElementById("rider-age").textContent = riderData.Age;
            document.getElementById("rider-firstcycling").textContent = riderData.FirstCyclingRider_id;
          } else {
            console.error("Rider not found!");
          }
        })
        .catch((error) => {
          console.error("Error fetching cyclist data:", error);
        });
    } else {
      console.error("RiderID not found in the URL!");
    }
  });
  