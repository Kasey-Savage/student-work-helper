from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serve the index.html file

@app.route('/add_assignment', methods=['POST'])
def add_assignment():
    data = request.get_json()
    assignment = data.get('assignment')
    due_date = data.get('due_date')
    est_time = data.get('est_time')

    print(f"Received assignment data: {data}")  # Debugging line

    # Check if the data folder exists; if not, create it
    if not os.path.exists('data'):
        os.makedirs('data')

    # Save the assignment to a CSV file
    file_path = 'data/assignments.csv'
    with open(file_path, 'a') as f:
        # If the file is empty, write the header
        if os.path.getsize(file_path) == 0:
            f.write('assignment,due_date,est_time\n')  # Write the header

        f.write(f"{assignment},{due_date},{est_time}\n")

    print(f"Assignment added: {assignment}, Due Date: {due_date}, Estimated Time: {est_time}")  # Debugging line

    return jsonify({"message": "Assignment added!"}), 200

@app.route('/get_assignments', methods=['GET'])
def get_assignments():
    # Check if the file exists and is not empty
    if not os.path.exists('data/assignments.csv') or os.path.getsize('data/assignments.csv') == 0:
        return jsonify([])

    assignments = []
    with open('data/assignments.csv', 'r') as f:
        for line in f:
            assignment_data = line.strip().split(',')
            if len(assignment_data) == 3:
                assignments.append({
                    'assignment': assignment_data[0],
                    'due_date': assignment_data[1],
                    'est_time': assignment_data[2]
                })

    return jsonify(assignments)

if __name__ == '__main__':
    app.run(debug=True)
