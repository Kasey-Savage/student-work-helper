document.getElementById('assignment-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const assignment = document.getElementById('assignment').value;
    const dueDate = document.getElementById('due-date').value;
    const estTime = document.getElementById('est-time').value;

    // Send the assignment data to the backend
    fetch('/add_assignment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            assignment: assignment,
            due_date: dueDate,
            est_time: estTime
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Log the response message
    })
    .catch(error => console.error('Error:', error));

    // Clear the form
    event.target.reset();
});
