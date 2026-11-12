from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
import mysql.connector

from db import get_db_connection

# Initialize the User Service
app = Flask(__name__)


# --- SERVICE ROUTES ---

# route to check status of microservice
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "service": "user-service",
        "status": "running"
    }), 200

# route for creating a new user
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

# route to get existing user data
@app.route("/user", methods=["GET"])
def get_user():
    """Retrieve user info by stored userID"""

    # set db query parameters
    user_id = request.args.get("userID")

    # verify userID provided 
    if not user_id:
        return jsonify({"error": "Missing userID"}), 400

    # verify input is a potential valid userID (positive#)
    if not user_id.isdigit() or int(user_id) < 1:
        return jsonify({"error": "Invalid userID"}), 400

    connection = None
    cursor = None

    try:
        # connect to db
        connection = get_db_connection()

        # return SQL query as dict
        cursor = connection.cursor(dictionary=True)

        # build query for user of matching ID
        query = """
            SELECT userID, username, email
            FROM users
            WHERE userID = %s
        """

        cursor.execute(query, (int(user_id),))

        # should only return one unique user
        user = cursor.fetchone()

        # return error if no matching user in db
        if user is None:
            return jsonify({"error": "User not found"}), 404

        # return found user
        return jsonify(user), 200

    except mysql.connector.Error:
        return jsonify({"error": "Database operation failure"}), 500

    # close db cursor / connection
    finally:
        if cursor is not None:
            cursor.close()

# route to update user's name or email
@app.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
        """Update existing user username and/or email"""

        # read incoming JSON
        data = request.get_json(silent=True)

        # verify JSON recieved
        if not isinstance(data, dict):
            return jsonify({"error": "A JSON object is needed for this request"}), 400

        # unpack updateed info from JSON
        username = data.get("username")
        email = data.get("email")

        # validate inputs
        if not all(isinstance(value, str) and value.strip() for value in (username, email)):
            return jsonify({"error": "Username and email required for update"}), 400

        # strip whitespace form inputs
        username = username.strip()
        email = email.strip()

        # check for appropriate lengths
        if len(username) > 80 or len(email) > 120:
            return jsonify({"error": "Username must be < 80 chars and email < 120"}), 400

        # validate user ID
        if user_id < 1:
            return jsonify({"error": "Invalid userID"}), 400

        connection = None
        cursor = None

        try:
            # make db cpnneciton
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            # check ofr user in db
            cursor.execute("SELECT userID FROM users WHERE userID = %s", (user_id,))

            user = cursor.fetchone()

            if user is None:
                return jsonify({"error": "No such user found"}), 404

            # update valid user info
            query = """UPDATE users SET username = %s, email = %s WHERE userID = %s"""

            cursor.execute(query, (username, email, user_id))

            # save updates info to db
            connection.commit()

            # return the changes to confirm
            return jsonify({
                "userID": user_id,
                "username": username,
                "email": email,
                "message": "User update completed successfully"
            }), 200

        except mysql.connector.IntegrityError:
            return jsonify({"error": "Username or email already in use"}), 409

        except mysql.connector.Error:
            return jsonify({"error": "Database operation failure"}), 500

        finally:
            #close cursor and discnnect db
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

# Start the User Service
if __name__ == "__main__":
    app.run(port=5001, debug=True)