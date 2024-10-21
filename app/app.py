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
    task_desc = data.get('task_desc')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    # Save schedule to CSV
    file_path = 'data/schedule.csv'
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write header if file is empty
        if os.path.getsize(file_path) == 0:
            writer.writerow(['task_desc','date', 'start_time', 'end_time'])
        writer.writerow([task_desc, date, start_time, end_time])

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

    try:
        # Check if schedule file exists and read from it
        if os.path.exists(schedule_file_path) and os.path.getsize(schedule_file_path) > 0:
            with open(schedule_file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) == 4:
                        date = datetime.strptime(row[1], '%Y-%m-%d')  # Correct date format
                        day_of_week = date.strftime('%A')
                        start_time = row[2]
                        end_time = row[3]
                        schedule = f"Schedule: {row[0]} from {start_time} - {end_time} on {row[1]}"
                        if day_of_week in weekly_schedule:
                            weekly_schedule[day_of_week].append(schedule)

        # Check if assignments file exists and read from it
        if os.path.exists(assignments_file_path) and os.path.getsize(assignments_file_path) > 0:
            with open(assignments_file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) == 4:
                        due_date = datetime.strptime(row[1], '%Y-%m-%d')  # Correct date format
                        day_of_week = due_date.strftime('%A')
                        due_time = row[2]
                        estimated_time = row[3]
                        task = f"Assignment: {row[0]} - Due: {due_date.date()} {due_time} (Est. {estimated_time} hours)"
                        if day_of_week in weekly_schedule:
                            weekly_schedule[day_of_week].append(task)

        return jsonify(weekly_schedule), 200

    except Exception as e:
        print(f"Error loading weekly schedule: {e}")
        return jsonify({"error": "Failed to load weekly schedule"}), 500

if __name__ == '__main__':
    app.run(debug=True)
