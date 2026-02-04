from flask import Flask, request, jsonify
from vercel_wsgi import handle_request

app = Flask(__name__)

API_KEY = "AIMM2025"

@app.route("/honeypot", methods=["POST"])
def honeypot():
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401

    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "No scam message provided"}), 400

    scam_message = data["message"].lower()

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

def handler(event, context):
    return handle_request(app, event, context)
