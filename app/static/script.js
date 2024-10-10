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
        document.getElementById('est-time').required = true;

        // Disable required for schedule fields
        document.getElementById('day-of-week').required = false;
        document.getElementById('start-time').required = false;
        document.getElementById('end-time').required = false;
        document.getElementById('task-desc').required = false;
    } else if (taskType === 'schedule') {
        assignmentFields.style.display = 'none';
        scheduleFields.style.display = 'block';

        // Enable schedule fields and disable assignment fields
        document.getElementById('assignment').required = false;
        document.getElementById('due-date').required = false;
        document.getElementById('est-time').required = false;

        // Enable required for schedule fields
        document.getElementById('day-of-week').required = true;
        document.getElementById('start-time').required = true;
        document.getElementById('end-time').required = true;
        document.getElementById('task-desc').required = true;
    }
}

// Function to handle form submission
document.getElementById('task-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const taskType = document.getElementById('task-type').value;

    if (taskType === 'assignment') {
        const assignment = document.getElementById('assignment').value;
        const dueDate = document.getElementById('due-date').value;
        const estTime = document.getElementById('est-time').value;

        // Send the assignment data to the server
        fetch('/add_assignment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                assignment: assignment,
                due_date: dueDate,
                est_time: estTime,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            loadAssignments();
        })
        .catch((error) => {
            console.error('Error:', error);
        });

    } else if (taskType === 'schedule') {
        const dayOfWeek = document.getElementById('day-of-week').value;
        const startTime = document.getElementById('start-time').value;
        const endTime = document.getElementById('end-time').value;
        const taskDesc = document.getElementById('task-desc').value;

        // Send the schedule data to the server
        fetch('/add_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                day_of_week: dayOfWeek,
                start_time: startTime,
                end_time: endTime,
                task_desc: taskDesc,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            loadSchedule();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // Reset the form but keep the current task type
    document.getElementById('task-form').reset();
    document.getElementById('task-type').value = taskType; // Keep task type after reset
});

// Call the function on page load to set the initial state
document.addEventListener('DOMContentLoaded', function() {
    toggleTaskType(document.getElementById('task-type').value);
});

// Function to load assignments
function loadAssignments() {
    fetch('/get_assignments')
        .then(response => response.json())
        .then(assignments => {
            const assignmentsList = document.getElementById('assignments-list');
            assignmentsList.innerHTML = ''; // Clear the existing list

            if (assignments && assignments.length > 0) {
                assignments.forEach(assignment => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${assignment.assignment} - Due: ${assignment.due_date} - Est Time: ${assignment.est_time} hours`;
                    assignmentsList.appendChild(listItem);
                });
            }
        })
        .catch((error) => {
            console.error('Error loading assignments:', error);
        });
}

// Function to load schedule
function loadSchedule() {
    fetch('/get_schedule')
        .then(response => response.json())
        .then(data => {
            const scheduleList = document.getElementById('schedule-list');
            scheduleList.innerHTML = ''; // Clear the existing schedule

            if (data && data.schedule && data.schedule.length > 0) {
                data.schedule.forEach(item => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${item.day_of_week} - ${item.start_time} to ${item.end_time} - ${item.task_desc}`;
                    scheduleList.appendChild(listItem);
                });
            }
        })
        .catch((error) => {
            console.error('Error loading schedule:', error);
        });
}

// Initial load
loadAssignments();
loadSchedule();
