import streamlit as st
import streamlit.components.v1 as components
import json, os

st.set_page_config(page_title="HopeFund", layout="wide")

GOAL = 10_000_000  # INR
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

# === Load once ===
data = load_data()

# === Sidebar Admin ===
st.sidebar.title("Admin / Test Panel")
donation = st.sidebar.number_input("Add donation (₹)", min_value=0, step=100)
if st.sidebar.button("Add"):
    # Reload before write to avoid overwrites from other processes
    data = load_data()
    data["total"] = int(data.get("total", 0)) + int(donation)
    save_data(data)
    st.sidebar.success(f"Added ₹{donation}")

# === Calculate Progress (use `data`, not `latest`) ===
progress = round((data.get("total", 0) / GOAL) * 100, 2)
progress = min(progress, 100.0)

# === Inject into HTML ===
with open("Untitled-1.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Replace initial values so the page isn't blank before JS fetch runs
html_code = html_code.replace("0%", f"{progress}% (₹{data.get('total', 0)} / ₹{GOAL})")
html_code = html_code.replace("width: 0%;", f"width: {progress}%;")

# === Render Full Screen ===
st.markdown("""
<style>
.block-container {padding: 0 !important;}
header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

components.html(html_code, height=2000, scrolling=True)
