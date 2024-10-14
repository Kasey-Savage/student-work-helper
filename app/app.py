import os
import csv
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Ensure the data folder exists
if not os.path.exists('data'):
    os.makedirs('data')

# Route to serve the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle adding an assignment
@app.route('/add_assignment', methods=['POST'])
def add_assignment():
    data = request.get_json()
    assignment = data.get('assignment')
    due_date = data.get('due_date')
    due_date_time = data.get('due_date_time')
    est_time = data.get('est_time')

    # Save assignment to CSV
    file_path = 'data/assignments.csv'
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write header if file is empty
        if os.path.getsize(file_path) == 0:
            writer.writerow(['assignment', 'due_date', 'due_date_time', 'est_time'])
        writer.writerow([assignment, due_date, due_date_time, est_time])

    return jsonify({"message": "Assignment added!"}), 200

# Route to handle adding a schedule entry
@app.route('/add_schedule', methods=['POST'])
def add_schedule():
    data = request.get_json()
    day_of_week = data.get('day_of_week')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    task_desc = data.get('task_desc')

    # Save schedule to CSV
    file_path = 'data/schedule.csv'
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write header if file is empty
        if os.path.getsize(file_path) == 0:
            writer.writerow(['day_of_week', 'start_time', 'end_time', 'task_desc'])
        writer.writerow([day_of_week, start_time, end_time, task_desc])

    return jsonify({"message": "Schedule added!"}), 200

# Route to get weekly schedule (grouped by day)
@app.route('/get_weekly_schedule', methods=['GET'])
def get_weekly_schedule():
    weekly_schedule = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": []
    }

    # File paths for assignments and schedule
    schedule_file_path = 'data/schedule.csv'
    assignments_file_path = 'data/assignments.csv'

    # Check if schedule file exists and read from it
    if os.path.exists(schedule_file_path) and os.path.getsize(schedule_file_path) > 0:
        with open(schedule_file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 4:
                    day_of_week = row[0]
                    task = f"Task: {row[1]} from {row[2]} - {row[3]}"
                    if day_of_week in weekly_schedule:
                        weekly_schedule[day_of_week].append(task)

    # Check if assignments file exists and read from it
    if os.path.exists(assignments_file_path) and os.path.getsize(assignments_file_path) > 0:
        with open(assignments_file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 4:
                    due_date = datetime.strptime(row[1], '%Y-%m-%d')  # Convert due_date to datetime object
                    day_of_week = due_date.strftime('%A')  # Get the day of the week (e.g., 'Monday')
                    due_time = row[2]  # Assuming due_date_time is the third column
                    estimated_time = row[3]  # Assuming estimated_time is the fourth column
                    task = f"Assignment: {row[0]} - Due: {due_date.date()} {due_time} (Est. {estimated_time} hours)"
                    if day_of_week in weekly_schedule:
                        weekly_schedule[day_of_week].append(task)

    return jsonify(weekly_schedule)

if __name__ == '__main__':
    app.run(debug=True)
