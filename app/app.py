from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serve the index.html file

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/add_assignment', methods=['POST'])
def add_assignment():
    data = request.get_json()
    assignment = data.get('assignment')
    due_date = data.get('due_date')
    est_time = data.get('est_time')

    # Save the assignment to a CSV file
    with open('data/assignments.csv', 'a') as f:
        f.write(f"{assignment},{due_date},{est_time}\n")

    return jsonify({"message": "Assignment added!"}), 200

@app.route('/get_assignments', methods=['GET'])
def get_assignments():
    if not os.path.exists('data/assignments.csv'):
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
