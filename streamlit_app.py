import streamlit as st
import io
import sqlite3
from datetime import datetime
from fpdf import FPDF

DB_NAME = 'wellness_app.db'

# --- Database Functions ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            title TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(role, title, content):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO chat_history (role, title, content) VALUES (?, ?, ?)
    ''', (role, title, content))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT role, title, content, timestamp FROM chat_history ORDER BY id')
    rows = c.fetchall()
    conn.close()
    return rows

# --- Tool Functions ---
def analyze_goal(text):
    return "Goal: Lose 5kg in 2 months"

def generate_meal_plan(veg=False):
    if veg:
        return """
- Breakfast: Oats with almond milk & banana  
- Lunch: Chickpea salad with olive oil dressing  
- Dinner: Lentil curry with brown rice  
"""
    return "Non-veg meal plan coming soon..."

def handle_injury(context):
    return """
- Avoid squats and lunges  
- Do seated leg extensions  
- Try low-impact cycling  
- Use resistance bands  
"""

def handle_diabetic_diet():
    return """
- Avoid sugar & refined carbs  
- Eat whole grains, fiber-rich foods  
- Prefer low-GI fruits like berries  
"""

def escalate_to_human():
    return "A human trainer will contact you. [Book Now](https://example.com/booking)"

def weight_loss_exercises():
    return """
- Cardio (5x/week): Jogging, brisk walking, or cycling (30-45 min)  
- Stretching/Yoga (2x/week): To increase flexibility and reduce stress  
- Strength training (3x/week): Bodyweight exercises (squats, pushups, planks)  
- Routine: Alternate cardio and strength days  
"""

# --- Streamlit UI Setup ---
st.set_page_config(
    page_title="Health AI Wellness Planner",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Mint Green background and Dark Teal text/buttons ---
st.markdown("""
    <style>
    body {
        background-color: #CFFFE5;  /* Mint Green */
        color: #006666;  /* Dark Teal */
    }
    .stApp {
        background-color: #CFFFE5;
        color: #006666;
    }
    h1, h2, h3, h4 {
        color: #004d4d;  /* Darker Teal for headings */
    }
    .stButton > button {
        background-color: #006666;   /* Dark Teal background */
        color: #CFFFE5;              /* Mint Green text */
        border: none;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #004d4d;
        color: #e0fff9;
    }
    .stTextInput>div>div>input {
        background-color: #e6fff5;
        color: #004d4d;
    }
    .stTextInput label {
        color: #006666;
    }
    .st-expanderHeader {
        color: #006666;
    }
    .stMarkdown {
        color: #004d4d;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("""
    <h1 style='text-align:center;'>AI Health & Wellness Dashboard</h1>
    <p style='text-align:center; font-size:16px;'>Get personalized wellness plans tailored for YOU!</p>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Initialize Database ---
init_db()

# --- Help / Examples ---
with st.expander("What can I ask? (Click to expand)", expanded=True):
    st.markdown("""
    <ul style='font-size:16px;'>
        <li>Tips to boost my metabolism naturally</li>
        <li>Suggest high-protein meals without meat</li>
        <li>How to manage blood sugar levels through diet?</li>
        <li>Best low-impact workouts for joint pain</li>
        <li>Can I schedule a session with a fitness coach?</li>
    </ul>
    """, unsafe_allow_html=True)

# --- Quick Prompts ---
st.markdown("**Quick prompts:**")
cols = st.columns([1,1,1])

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

def set_quick_prompt(prompt):
    st.session_state['user_input'] = prompt

with cols[0]:
    if st.button("Lose 5kg"):
        set_quick_prompt("I want to lose 5kg in 2 months")

with cols[1]:
    if st.button("I'm vegetarian"):
        set_quick_prompt("I'm vegetarian")

with cols[2]:
    if st.button("I'm diabetic"):
        set_quick_prompt("I'm diabetic")

st.markdown("---")

# --- Chat Input ---
user_input = st.text_input("Your message here...", value=st.session_state['user_input'], key="input_box")

if user_input and user_input != "":
    # Save user message in DB
    save_message("user", "", user_input)

    st.session_state['user_input'] = ""
    lowered = user_input.lower()
    responses = []

    if "lose" in lowered and "kg" in lowered:
        responses.append(("Goal Analysis", analyze_goal(user_input)))
        responses.append(("Weight Loss Exercises", weight_loss_exercises()))
    if "vegetarian" in lowered:
        responses.append(("Vegetarian Meal Plan", generate_meal_plan(veg=True)))
    if "knee pain" in lowered or "injury" in lowered:
        responses.append(("Injury Support Plan", handle_injury(user_input)))
    if "diabetic" in lowered:
        responses.append(("Diabetic-Friendly Diet", handle_diabetic_diet()))
    if "real trainer" in lowered or "talk to" in lowered:
        responses.append(("Escalation", escalate_to_human()))

    # Save all bot responses in DB
    for title, content in responses:
        save_message("assistant", title, content)

# --- Fetch all messages from DB and display ---
chat_history = get_all_messages()
for role, title, content, timestamp in chat_history:
    timestamp_str = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    time_fmt = timestamp_str.strftime("%b %d %H:%M")
    if role == "user":
        st.markdown(f"**You ({time_fmt}):** {content}")
    else:
        st.markdown(f"### {title} ({time_fmt})")
        st.markdown(content)
        st.markdown("---")

# --- PDF Generator Class ---
class ChatPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 102, 102)  # Dark Teal
        self.cell(0, 10, "AI Health & Wellness Chat", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

# --- Create PDF from Chat History ---
def create_chat_pdf():
    pdf = ChatPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for role, title, content, timestamp in get_all_messages():
        if role == "user":
            pdf.set_text_color(0, 102, 102)  # Dark Teal
            pdf.multi_cell(0, 10, f"You: {content}")
        else:
            pdf.set_text_color(0, 102, 102)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, title, ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, content)
        pdf.ln(4)

    buffer = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    buffer.write(pdf_bytes)
    buffer.seek(0)
    return buffer

# --- Download PDF Button ---
st.markdown("### Download Your Chat as PDF")
pdf_data = create_chat_pdf()

st.download_button(
    label="Download Chat (.pdf)",
    data=pdf_data,
    file_name="wellness_chat_transcript.pdf",
    mime="application/pdf"
) 