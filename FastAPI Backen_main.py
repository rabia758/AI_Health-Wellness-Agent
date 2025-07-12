# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# --- AI Logic Functions ---
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
    return "A human trainer will contact you."

def weight_loss_exercises():
    return """
- Cardio (5x/week): Jogging, brisk walking, or cycling (30-45 min)  
- Stretching/Yoga (2x/week): To increase flexibility and reduce stress  
- Strength training (3x/week): Bodyweight exercises (squats, pushups, planks)  
- Routine: Alternate cardio and strength days  
"""

# --- FastAPI Request Model ---
class Query(BaseModel):
    question: str

# --- API Endpoints ---
@app.post("/ask")
def ask_agent(query: Query):
    text = query.question.lower()
    responses = []

    if "lose" in text and "kg" in text:
        responses.append(("Goal Analysis", analyze_goal(text)))
        responses.append(("Weight Loss Exercises", weight_loss_exercises()))
    if "vegetarian" in text:
        responses.append(("Vegetarian Meal Plan", generate_meal_plan(veg=True)))
    if "knee pain" in text or "injury" in text:
        responses.append(("Injury Support Plan", handle_injury(text)))
    if "diabetic" in text:
        responses.append(("Diabetic-Friendly Diet", handle_diabetic_diet()))
    if "real trainer" in text or "talk to" in text:
        responses.append(("Escalation", escalate_to_human()))

    return {"responses": responses}
