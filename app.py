from flask import Flask, jsonify

# Initialize the User Service
app = Flask(__name__)


# --- SERVICE ROUTES ---

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "service": "user-service",
        "status": "running"
    }), 200


# Start the User Service
if __name__ == "__main__":
    app.run(port=5001, debug=True)