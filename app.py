import streamlit as st
import streamlit.components.v1 as components
import json
import os

st.set_page_config(page_title="HopeFund", layout="wide")

# === Config ===
GOAL = 10000000  # target in INR
DATA_FILE = "donations.json"

# === Load/Init Donations ===
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"total": 0}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# === Sidebar for Admin/Testing ===
st.sidebar.title("Admin / Test Panel")
donation = st.sidebar.number_input("Add donation (₹)", min_value=0, step=100)
if st.sidebar.button("Add"):
    # Always reload before writing
    with open(DATA_FILE, "r") as f:
        latest = json.load(f)
    latest["total"] += donation
    with open(DATA_FILE, "w") as f:
        json.dump(latest, f)
    st.sidebar.success(f"Added ₹{donation}")

# === Calculate Progress ===
progress = int((latest["total"] / GOAL) * 100)
progress = min(progress, 100)  # cap at 100%

# === Inject into HTML ===
with open("Untitled-1.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Replace placeholders with real values
html_code = html_code.replace("0%", f"{progress}% (₹{data['total']} / ₹{GOAL})")
html_code = html_code.replace('width: 0%;', f'width: {progress}%;')

# === Render Full Screen ===
st.markdown(
    """
    <style>
    .block-container {padding: 0 !important;}
    header, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
components.html(html_code, height=2000, scrolling=True)
