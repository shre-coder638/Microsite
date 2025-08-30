from flask import Flask, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)  # allow fetches from Streamlit iframe / other origins

GOAL = 10_000_000
DATA_FILE = "donations.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"total": 0}

@app.route("/progress")
def progress():
    data = load_data()
    total = int(data.get("total", 0))
    pct = round((total / GOAL) * 100, 2)
    return jsonify({"total": total, "goal": GOAL, "progress": min(pct, 100.0)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
