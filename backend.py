from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

GOAL = 10_000_000  # target in INR
DATA_FILE = "donations.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"total": 0}


@app.route("/progress")
def progress():
    data = load_data()
    total = data.get("total", 0)
    progress = int((total / GOAL) * 100)
    progress = min(progress, 100)
    return jsonify({
        "total": total,
        "goal": GOAL,
        "progress": progress
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

