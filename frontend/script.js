document.getElementById('assignment-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const assignment = document.getElementById('assignment').value;
    const dueDate = document.getElementById('due-date').value;
    const estTime = document.getElementById('est-time').value;
    
    // Logic to handle assignment data goes here

    console.log(`Assignment: ${assignment}, Due: ${dueDate}, Time: ${estTime} hrs`);
    
    // Clear the form
    event.target.reset();
});
