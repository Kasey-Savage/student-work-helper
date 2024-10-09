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

    # Load existing assignments, append new one, and save back to CSV
    df = pd.DataFrame(columns=['assignment', 'due_date', 'est_time'])
    if os.path.exists('data/assignments.csv'):
        df = pd.read_csv('data/assignments.csv')

    new_assignment = pd.DataFrame([[assignment, due_date, est_time]], columns=['assignment', 'due_date', 'est_time'])
    df = pd.concat([df, new_assignment], ignore_index=True)
    df.to_csv('data/assignments.csv', index=False)

    return jsonify({"message": "Assignment added!"}), 200

@app.route('/get_assignments', methods=['GET'])
def get_assignments():
    if not os.path.exists('data/assignments.csv'):
        return jsonify([])

    df = pd.read_csv('data/assignments.csv')
    assignments = df.to_dict(orient='records')  # Convert to list of dictionaries
    return jsonify(assignments)

if __name__ == '__main__':
    app.run(debug=True)
