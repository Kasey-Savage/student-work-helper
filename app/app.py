from flask import Flask, render_template, request, jsonify
import os
import csv

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
    est_time = data.get('est_time')

    # Save assignment to CSV
    file_path = 'data/assignments.csv'
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write header if file is empty
        if os.path.getsize(file_path) == 0:
            writer.writerow(['assignment', 'due_date', 'est_time'])
        writer.writerow([assignment, due_date, est_time])

    return jsonify({"message": "Assignment added!"}), 200

# Route to get all assignments
@app.route('/get_assignments', methods=['GET'])
def get_assignments():
    assignments = []
    file_path = 'data/assignments.csv'

    # Check if assignments file exists
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return jsonify([])

    # Read from CSV file
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) == 3:
                assignments.append({
                    'assignment': row[0],
                    'due_date': row[1],
                    'est_time': row[2]
                })

    return jsonify(assignments)

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

# Route to get all schedule items
@app.route('/get_schedule', methods=['GET'])
def get_schedule():
    schedule = []
    file_path = 'data/schedule.csv'

    # Check if schedule file exists
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return jsonify([])

    # Read from CSV file
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            # Ensure each row has 4 elements (day_of_week, start_time, end_time, task_desc)
            if len(row) >= 4:
                schedule.append({
                    'day_of_week': row[0],
                    'start_time': row[1],
                    'end_time': row[2],
                    'task_desc': row[3]
                })

    return jsonify({'schedule': schedule})

if __name__ == '__main__':
    app.run(debug=True)
