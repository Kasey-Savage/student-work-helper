document.addEventListener('DOMContentLoaded', function() {
    // Fetch assignments when the page loads
    fetch('/get_assignments')
        .then(response => response.json())
        .then(assignments => {
            updateUpcomingAssignments(assignments);
        })
        .catch(error => console.error('Error fetching assignments:', error));

    // Function to update the Upcoming Assignments section
    function updateUpcomingAssignments(assignments) {
        const scheduleSection = document.getElementById('schedule');
        scheduleSection.innerHTML = ''; // Clear existing assignments

        if (assignments.length === 0) {
            scheduleSection.innerHTML = '<p>No upcoming assignments available.</p>';
        } else {
            assignments.forEach(assignment => {
                const div = document.createElement('div');
                div.innerHTML = `${assignment.assignment} (Due: ${assignment.due_date}, Est Time: ${assignment.est_time} hrs)`;
                scheduleSection.appendChild(div);
            });
        }
    }

    // Handle form submission
    document.getElementById('assignment-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const assignment = document.getElementById('assignment').value;
        const dueDate = document.getElementById('due-date').value;
        const estTime = document.getElementById('est-time').value;

        console.log('Adding assignment:', assignment, dueDate, estTime);  // Debugging line

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
            // Re-fetch assignments to update the list
            return fetch('/get_assignments');
        })
        .then(response => response.json())
        .then(assignments => {
            updateUpcomingAssignments(assignments);
        })
        .catch(error => console.error('Error:', error));

        // Clear the form
        event.target.reset();
    });
});
