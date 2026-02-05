from flask import Flask, request, jsonify

app = Flask(__name__)

# Your API key
API_KEY = "AIMM2025"

@app.route("/")
def home():
    return "Honeypot API Running Successfully!"

@app.route("/honeypot", methods=["POST"])
def honeypot():
    # Authentication
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401

    data = request.json

    if not data:
        return jsonify({"error": "Invalid or empty JSON"}), 400

    # Accept multiple possible message formats
    scam_message = None

    # Case 1: {"message": "text"}
    if isinstance(data.get("message"), str):
        scam_message = data["message"]

    # Case 2: {"scam_message": "text"}
    elif isinstance(data.get("scam_message"), str):
        scam_message = data["scam_message"]

    # Case 3: nested: {"message": {"text": "text"}}
    elif isinstance(data.get("message"), dict):
        scam_message = data["message"].get("text") or data["message"].get("content")

    # If no valid message
    if not scam_message:
        return jsonify({"error": "No valid scam message provided"}), 400

    scam_message = scam_message.lower()

    # Scam detection logic
    intelligence = {
        "scam_type": "",
        "risk_level": "",
        "keywords": [],
        "pattern_detected": "",
        "recommendation": ""
    }

    if "loan" in scam_message:
        intelligence["scam_type"] = "Loan Scam"
        intelligence["risk_level"] = "high"
        intelligence["keywords"] = ["loan", "approved"]
        intelligence["pattern_detected"] = "Financial bait + urgency"
        intelligence["recommendation"] = "Do not pay any fee."

    elif "otp" in scam_message:
        intelligence["scam_type"] = "OTP Scam"
        intelligence["risk_level"] = "critical"
        intelligence["keywords"] = ["otp", "verify"]
        intelligence["pattern_detected"] = "Identity theft"
        intelligence["recommendation"] = "Never share OTP."

    else:
        intelligence["scam_type"] = "Unknown"
        intelligence["risk_level"] = "medium"
        intelligence["keywords"] = ["generic"]
        intelligence["pattern_detected"] = "No clear pattern"
        intelligence["recommendation"] = "Be cautious."

    return jsonify(intelligence)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
