from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
import mysql.connector

from db import get_db_connection

# Initialize the User Service
app = Flask(__name__)


# --- SERVICE ROUTES ---

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "service": "user-service",
        "status": "running"
    }), 200

@app.route("/user", methods=["POST"])
def create_user():
    """Create a new user account."""

    # Read the incoming JSON request
    data = request.get_json(silent=True)

    # Verify that JSON was provided
    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    # Extract the user information
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validate the required fields
    if not all(
        isinstance(value, str) and value.strip()
        for value in (username, email, password)
    ):
        return jsonify({"error": "All fields are required"}), 400

    username = username.strip()
    email = email.strip()

    # Validate database field lengths
    if len(username) > 80 or len(email) > 120:
        return jsonify({"error": "Username or email is too long"}), 400

    # Hash the password before storing it
    password_hash = generate_password_hash(password)

    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the new user using a parameterized query
        query = """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (username, email, password_hash))

        # Save the record
        connection.commit()

        # Get the automatically generated user ID
        user_id = cursor.lastrowid

        return jsonify({
            "userID": user_id,
            "username": username,
            "email": email
        }), 201

    except mysql.connector.IntegrityError:
        return jsonify({
            "error": "Username or email already exists"
        }), 409

    except mysql.connector.Error:
        return jsonify({
            "error": "Database operation failed"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


# Start the User Service
if __name__ == "__main__":
    app.run(port=5001, debug=True)