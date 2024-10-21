// Function to toggle between assignment and schedule
function toggleTaskType(taskType) {
    const assignmentFields = document.getElementById('assignment-fields');
    const scheduleFields = document.getElementById('schedule-fields');

    if (taskType === 'assignment') {
        assignmentFields.style.display = 'block';
        scheduleFields.style.display = 'none';

        // Enable assignment fields and disable schedule fields
        document.getElementById('assignment').required = true;
        document.getElementById('due-date').required = true;
        document.getElementById('due-date-time').required = true;
        document.getElementById('est-time').required = true;

        // Disable required for schedule fields
        document.getElementById('task-desc').required = false;
        document.getElementById('date').required = false;
        document.getElementById('start-time').required = false;
        document.getElementById('end-time').required = false;
    } else if (taskType === 'schedule') {
        assignmentFields.style.display = 'none';
        scheduleFields.style.display = 'block';

        // Enable schedule fields and disable assignment fields
        document.getElementById('assignment').required = false;
        document.getElementById('due-date').required = false;
        document.getElementById('due-date-time').required = false;
        document.getElementById('est-time').required = false;

        // Enable required for schedule fields
        document.getElementById('task-desc').required = true;
        document.getElementById('date').required = true;
        document.getElementById('start-time').required = true;
        document.getElementById('end-time').required = true;
    }
}

// Function to handle form submission
document.getElementById('task-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const taskType = document.getElementById('task-type').value;

    if (taskType === 'assignment') {
        const assignment = document.getElementById('assignment').value;
        const dueDate = document.getElementById('due-date').value;
        const dueDateTime = document.getElementById('due-date-time').value;
        const estTime = document.getElementById('est-time').value;

        // Send the assignment data to the csv file
        fetch('/add_assignment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                assignment: assignment,
                due_date: dueDate,
                due_date_time: dueDateTime,
                est_time: estTime,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });

    } else if (taskType === 'schedule') {
        const taskDesc = document.getElementById('task-desc').value;
        const dateOf = document.getElementById('date').value;
        const startTime = document.getElementById('start-time').value;
        const endTime = document.getElementById('end-time').value;

        // Send the schedule data to the csv file
        fetch('/add_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task_desc : taskDesc,
                date: dateOf,
                start_time: startTime,
                end_time: endTime,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // Reset the form but keep the current task type
    document.getElementById('task-form').reset();
    document.getElementById('task-type').value = taskType; // Keep task type after reset
    loadWeeklySchedule();
});

// Call the function on page load to set the initial state
document.addEventListener('DOMContentLoaded', function() {
    toggleTaskType(document.getElementById('task-type').value);
});

function loadWeeklySchedule() {
    fetch('/get_weekly_schedule')
        .then(response => response.json())
        .then(data => {
            // Loop through each day of the week and populate the list
            for (const [day, tasks] of Object.entries(data)) {
                const dayList = document.getElementById(day.toLowerCase() + '-list');
                dayList.innerHTML = ''; // Clear the existing list
                tasks.forEach(task => {
                    const listItem = document.createElement('li');
                    listItem.textContent = task;
                    dayList.appendChild(listItem);
                });
            }
        })
        .catch(error => {
            console.error('Error loading weekly schedule:', error);
        });
}

// Update calander when the page loads
loadWeeklySchedule();