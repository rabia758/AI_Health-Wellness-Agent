import os
import google.generativeai as genai
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("🚨 GEMINI_API_KEY not found in environment variables!")

# ✅ Configure the Gemini model
genai.configure(api_key=api_key)

# ✅ Load Gemini model (v2.5)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")  # Change to available version if needed

# ✅ Main function to generate health plan
def generate_health_plan(user_input: str) -> str:
    prompt = f"""
You are a friendly and professional health and wellness assistant.
The user said: "{user_input}"

Based on this goal, create a detailed and motivational health plan that includes:
1. A personalized diet plan (breakfast, lunch, dinner)
2. A workout routine (with home and gym options)
3. Weekly goal tracking and encouragement tips

Format the response clearly using headings and bullet points.
"""

    try:
        response = model.generate_content(prompt)
        return response.text  # or response.parts[0].text if using multi-part
    except Exception as e:
        return f"❌ Error generating health plan: {str(e)}"