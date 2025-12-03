"""
Utility functions with intentional vulnerabilities and breaking patterns
"""

import hashlib
import base64
import pickle


# VULNERABILITY: Weak hashing algorithm
def hash_password(password):
    # VULNERABILITY: MD5 is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()


# VULNERABILITY: Using SHA1 (also weak)
def hash_password_sha1(password):
    # VULNERABILITY: SHA1 is also considered weak for passwords
    return hashlib.sha1(password.encode()).hexdigest()


def encode_base64(data):
    return base64.b64encode(data.encode()).decode()


def decode_base64(data):
    return base64.b64decode(data.encode()).decode()


# VULNERABILITY: Unsafe deserialization
def serialize_object(obj):
    # VULNERABILITY: Pickle is unsafe for untrusted data
    return base64.b64encode(pickle.dumps(obj)).decode()


def deserialize_object(data):
    # VULNERABILITY: Pickle deserialization can execute arbitrary code
    return pickle.loads(base64.b64decode(data.encode()))


# VULNERABILITY: Using eval
def calculate(expression):
    # VULNERABILITY: eval() can execute arbitrary code
    return eval(expression)


# VULNERABILITY: Using exec
def run_code(code):
    # VULNERABILITY: exec() can execute arbitrary code
    exec(code)


# BREAKING CHANGE: Blocking I/O
def read_config_sync(filepath):
    # BREAKING CHANGE: Blocking I/O in Python
    import json
    with open(filepath, 'r') as f:
        return json.load(f)


# VULNERABILITY: Hardcoded secrets
API_KEY = 'sk-1234567890abcdef'
DATABASE_PASSWORD = 'admin123'
AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
