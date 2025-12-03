from flask import Flask, request, jsonify, redirect
import subprocess
import os
import jwt
import yaml

app = Flask(__name__)

# VULNERABILITY: Weak secret key
JWT_SECRET = 'secret123'

# VULNERABILITY: Debug mode enabled
app.config['DEBUG'] = True

# In-memory database
items = [
    {'id': 1, 'name': 'Item 1'},
    {'id': 2, 'name': 'Item 2'},
    {'id': 3, 'name': 'Item 3'}
]


# VULNERABILITY: SQL Injection simulation with raw query building
def find_item_by_name(name):
    # Simulating SQL injection vulnerability with string concatenation
    query = "SELECT * FROM items WHERE name = '" + name + "'"
    print('Executing query:', query)
    # In real DB this would be vulnerable
    return next((item for item in items if item['name'] == name), None)


# VULNERABILITY: Command Injection
@app.route('/api/ping')
def ping():
    host = request.args.get('host', '')
    # VULNERABILITY: Direct command injection
    result = subprocess.run(
        'ping -c 1 ' + host,
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return jsonify({'error': result.stderr}), 500
    return jsonify({'output': result.stdout})


# VULNERABILITY: Path Traversal
@app.route('/api/files')
def get_file():
    filename = request.args.get('file', '')
    # VULNERABILITY: No path sanitization
    filepath = os.path.join(os.path.dirname(__file__), 'uploads', filename)

    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


# VULNERABILITY: Insecure JWT
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # VULNERABILITY: Hardcoded credentials
    if username == 'admin' and password == 'admin123':
        # VULNERABILITY: Weak secret and no expiration
        token = jwt.encode({'user': username, 'role': 'admin'}, JWT_SECRET, algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401


# VULNERABILITY: YAML deserialization
@app.route('/api/parse-yaml', methods=['POST'])
def parse_yaml():
    try:
        data = request.get_json()
        # VULNERABILITY: Unsafe YAML parsing (allows code execution)
        parsed = yaml.load(data.get('yaml', ''), Loader=yaml.Loader)
        return jsonify({'parsed': parsed})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# VULNERABILITY: Regex DoS (ReDoS)
@app.route('/api/validate-email')
def validate_email():
    import re
    email = request.args.get('email', '')
    # VULNERABILITY: Evil regex - exponential backtracking
    email_regex = r'^([a-zA-Z0-9]+)+@([a-zA-Z0-9]+)+\.([a-zA-Z0-9]+)+$'
    is_valid = bool(re.match(email_regex, email))
    return jsonify({'valid': is_valid})


# Standard CRUD endpoints
@app.route('/api/items')
def get_items():
    return jsonify(items)


@app.route('/api/items/<int:item_id>')
def get_item(item_id):
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Not found'}), 404

    item['next_item'] = f'http://localhost:5000/api/items/{item_id + 1}'
    return jsonify(item)


@app.route('/api/items', methods=['POST'])
def create_item():
    new_item = request.get_json()
    items.append(new_item)
    return jsonify(new_item), 201


@app.route('/api/items/bulk', methods=['POST'])
def bulk_create_items():
    new_items = request.get_json()
    items.extend(new_items)
    return jsonify({'message': f'Created {len(new_items)} items'}), 201


# VULNERABILITY: Open redirect
@app.route('/api/redirect')
def open_redirect():
    url = request.args.get('url', '')
    # VULNERABILITY: No validation on redirect URL
    return redirect(url)


# VULNERABILITY: Server-Side Template Injection (SSTI)
@app.route('/api/greet')
def greet():
    from flask import render_template_string
    name = request.args.get('name', 'Guest')
    # VULNERABILITY: User input directly in template
    template = f'<h1>Hello {name}!</h1>'
    return render_template_string(template)


# VULNERABILITY: Pickle deserialization
@app.route('/api/load-data', methods=['POST'])
def load_data():
    import pickle
    import base64
    data = request.get_json()
    # VULNERABILITY: Unsafe pickle deserialization
    try:
        decoded = base64.b64decode(data.get('data', ''))
        obj = pickle.loads(decoded)
        return jsonify({'loaded': str(obj)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
