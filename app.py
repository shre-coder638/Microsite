import streamlit as st
import streamlit.components.v1 as components
import json
import os
import time

st.set_page_config(page_title="HopeFund", layout="wide")

GOAL = 10_000_000
DATA_FILE = "donations.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    data = {"total": 0}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Sidebar admin panel
st.sidebar.title("Admin / Test Panel")
donation = st.sidebar.number_input("Add donation (₹)", min_value=0, step=100)
if st.sidebar.button("Add"):
    data = load_data()
    data["total"] += int(donation)
    save_data(data)
    st.sidebar.success(f"Added ₹{donation}")

# Container for HTML
html_container = st.empty()

# Auto-refresh loop
while True:
    data = load_data()
    progress = round((data.get("total", 0) / GOAL) * 100, 2)
    progress = min(progress, 100.0)

    with open("Untitled-1.html", "r", encoding="utf-8") as f:
        html_code = f.read()

    html_code = html_code.replace("0%", f"{progress}% (₹{data.get('total', 0)} / ₹{GOAL})")
    html_code = html_code.replace("width: 0%;", f"width: {progress}%;")

    html_container.html(html_code, height=2000, scrolling=True)

    time.sleep(5)
