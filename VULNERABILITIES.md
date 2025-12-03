# Python Security Vulnerabilities

This project contains intentional security vulnerabilities for testing purposes.

## Vulnerabilities

### app.py
- **Command Injection** (`/api/ping`): User input passed directly to shell command
- **Path Traversal** (`/api/files`): No path sanitization on file reads
- **Weak JWT Secret**: Using `secret123` as JWT secret
- **Hardcoded Credentials**: Admin credentials in source code
- **Unsafe YAML Parsing**: Using `yaml.Loader` allows code execution
- **ReDoS**: Evil regex pattern with exponential backtracking
- **Open Redirect**: No validation on redirect URLs
- **SSTI**: Server-Side Template Injection via `render_template_string`
- **Pickle Deserialization**: Unsafe pickle.loads on user data
- **Debug Mode**: Flask debug mode enabled in production

### database.py
- **SQL Injection**: Multiple endpoints with string concatenation
- **SQL Injection in Authentication**: Classic SQLi in login
- **SQL Injection in ORDER BY**: Unvalidated column names
- **SQL Injection in LIKE**: Searchable injection point
- **Bulk Insert SQLi**: Injection via bulk operations

### utils.py
- **Weak Hashing**: Using MD5 and SHA1 for passwords
- **Unsafe Deserialization**: Pickle serialization/deserialization
- **Code Execution**: Using `eval()` and `exec()` on user input
- **Hardcoded Secrets**: API keys and passwords in source code
