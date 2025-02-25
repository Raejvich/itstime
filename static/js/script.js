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