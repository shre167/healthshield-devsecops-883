import os
from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "healthcare_http_requests_total",
    "Total HTTP requests"
)

PATIENTS = {
    "demo-001": {
        "patient_id": "demo-001",
        "name": "Demo Patient",
        "status": "Example record only"
    }
}

@app.before_request
def count_requests():
    REQUEST_COUNT.inc()

@app.route("/")
def home():
    return jsonify({
        "application": "Healthcare Demo API",
        "status": "running"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/patients/<patient_id>")
def get_patient(patient_id):
    patient = PATIENTS.get(patient_id)

    if patient is None:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify(patient)

@app.route("/patients", methods=["POST"])
def create_patient():
    data = request.get_json(silent=True) or {}
    name = data.get("name")

    if not isinstance(name, str) or not name.strip() or len(name) > 100:
        return jsonify({"error": "Invalid patient name"}), 400

    return jsonify({
        "message": "Demo patient accepted"
    }), 201

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": "text/plain; version=0.0.4"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
