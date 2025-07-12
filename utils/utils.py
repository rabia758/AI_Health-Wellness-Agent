import sqlite3

DB_NAME = 'wellness_app.db'

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

def analyze_goal(text):
    return "Goal: Lose 5kg in 2 months"

def generate_meal_plan(veg=False):
    if veg:
        return """- Breakfast: Oats with almond milk & banana
- Lunch: Chickpea salad with olive oil dressing
- Dinner: Lentil curry with brown rice"""
    return "Non-veg meal plan coming soon..."

def handle_injury(context):
    return """- Avoid squats and lunges
- Do seated leg extensions
- Try low-impact cycling
- Use resistance bands"""

def handle_diabetic_diet():
    return """- Avoid sugar & refined carbs
- Eat whole grains, fiber-rich foods
- Prefer low-GI fruits like berries"""

def escalate_to_human():
    return "A human trainer will contact you."

def weight_loss_exercises():
    return """- Cardio (5x/week): Jogging, brisk walking, or cycling (30-45 min)
- Stretching/Yoga (2x/week): Increase flexibility and reduce stress
- Strength training (3x/week): Bodyweight exercises (squats, pushups, planks)
- Routine: Alternate cardio and strength days"""