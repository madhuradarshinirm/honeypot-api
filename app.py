from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "AIMM2025"  # your authentication key

@app.route("/honeypot", methods=["POST"])
def honeypot():
    # Authentication
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401

    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "No scam message provided"}), 400

    scam_message = data["message"].lower()

    # Intelligence extraction
    intelligence = {
        "scam_type": "",
        "risk_level": "",
        "keywords": [],
        "pattern_detected": "",
        "recommendation": ""
    }

    if "loan" in scam_message or "approved" in scam_message:
        intelligence["scam_type"] = "Loan Scam"
        intelligence["risk_level"] = "high"
        intelligence["keywords"] = ["loan", "approved", "verification"]
        intelligence["pattern_detected"] = "Financial bait + urgency"
        intelligence["recommendation"] = "Do not pay any fee."

    elif "otp" in scam_message or "verify" in scam_message:
        intelligence["scam_type"] = "OTP Scam"
        intelligence["risk_level"] = "critical"
        intelligence["keywords"] = ["otp", "verify"]
        intelligence["pattern_detected"] = "Identity theft attempt"
        intelligence["recommendation"] = "Never share OTP."

    else:
        intelligence["scam_type"] = "Unknown"
        intelligence["risk_level"] = "medium"
        intelligence["keywords"] = ["generic"]
        intelligence["pattern_detected"] = "No clear scam pattern"
        intelligence["recommendation"] = "Be cautious."

    return jsonify(intelligence)

@app.route("/")
def home():
    return "Honeypot API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
