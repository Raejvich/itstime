const eventContainers = document.querySelectorAll(".event-container")
const fightsContainers = document.querySelectorAll(".fights-container")

eventContainers.forEach(eventContainer => {
    // Find the corresponding fightsContainer 
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
    // Get the date in Eastern Time (ET)
    const eventDateStr = eventDateET.textContent.trim();  
    
    // Create a Date object from the ET time 
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