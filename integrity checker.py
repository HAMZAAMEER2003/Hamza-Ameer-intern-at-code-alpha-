import os
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define a trusted database of file hashes (you should populate this)
trusted_database = {
    "/path/to/file1.txt": "hash_of_file1",
    "/path/to/file2.txt": "hash_of_file2",
    # Add more files and their hashes as needed
}

def calculate_file_hash(file_path):
    """Calculate the hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>System File Integrity Checker</title>
    </head>
    <body>
        <h1>System File Integrity Checker</h1>
        <form method="POST" action="/check">
            <label for="file_path">Select a file to check:</label>
            <select name="file_path" id="file_path">
                {% for file in files %}
                <option value="{{ file }}">{{ file }}</option>
                {% endfor %}
            </select>
            <button type="submit">Check Integrity</button>
        </form>
        <div>
            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    <ul>
                        {% for message in messages %}
                            <li {% if 'error' in message %}style="color: red;"{% endif %}>{{ message }}</li>
                        {% endfor %}
                    </ul>
                {% endif %}
            {% endwith %}
        </div>
    </body>
    </html>
    """

@app.route('/check', methods=['POST'])
def check_integrity():
    file_path = request.form['file_path']
    if file_path not in trusted_database:
        flash('File not found in the trusted database', 'error')
    else:
        expected_hash = trusted_database[file_path]
        current_hash = calculate_file_hash(file_path)
        if expected_hash == current_hash:
            flash('File integrity is maintained.', 'success')
        else:
            flash('File integrity has been compromised!', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
