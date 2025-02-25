const eventContainers = document.querySelectorAll(".event-container")
const fightsContainers = document.querySelectorAll(".fights-container")

eventContainers.forEach(eventContainer => {
    // Find the corresponding fightsContainer (child of the current eventContainer)
    const fightsContainer = eventContainer.querySelector(".fights-container");

    // Add click event listener to the eventContainer
    eventContainer.addEventListener("click", () => {
        toggleFights(fightsContainer);
    });
});


function toggleFights(fightsContainer) {
    if (fightsContainer.style.display === "none" || fightsContainer.style.display === "") {
        fightsContainer.style.display = "block";
    } else {
        fightsContainer.style.display = "none";
    }
}

const eventDatesET = document.querySelectorAll(".event-date");

eventDatesET.forEach(eventDateET => {
    // Get the date in Eastern Time (ET) from the DOM element (assuming it's in ISO format like "2025-03-01T15:00:00")
    const eventDateStr = eventDateET.textContent.trim();  // Or use eventDateET.getAttribute('data-time') if it's in a data attribute
    
    // Create a Date object from the ET time (which is in ISO 8601 format)
    const eventDateETObj = new Date(eventDateStr + " GMT-0500"); // Adding the GMT offset for ET (-5 hours) manually
    
    // Convert the event date to the user's local time
    const localDate = eventDateETObj.toLocaleString("en-US", {
        weekday: "long",          
        year: "numeric",             
        month: "long",                 
        day: "numeric",            
        hour: "numeric",               
        minute: "numeric",           
        second: "numeric",             
        hour12: true                  
    });

    // Update the DOM element with the converted local time
    eventDateET.textContent = localDate;
});