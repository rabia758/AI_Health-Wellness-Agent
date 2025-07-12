# 🧠 Rabia' s Health & Wellness Planner Agent 💪🌿
 Powered by the OpenAI Agents SDK 🚀

👋 Welcome to your personal AI-powered wellness assistant! Syeda's Agent is designed to help you:

🎯 Understand and track your fitness & nutrition goals

🥗 Generate personalized meal plans (e.g., vegan, low-carb, 1500 cal/day)

🏋️ Create custom workout routines (e.g., strength, cardio, flexibility)

⏰ Set reminders and log progress

🧠 Chat in natural language with real-time streaming

# 🩺 Handoff to experts like a Nutrition Coach or Injury Support Agent when needed

# 📖 Overview
Syeda's Health & Wellness Planner Agent is a smart, AI-powered assistant built using the OpenAI Agents SDK. It helps users achieve their fitness, nutrition, and well-being goals through interactive, real-time conversations.

Whether you're trying to lose weight, eat healthier, build muscle, or recover from an injury, this agent is your 24/7 personal planner — packed with specialized tools and expert agents.

# 🔑 Key Capabilities
Feature	Status	Description
Multi-turn Conversations	✅	Understands user goals through natural dialogue
Goal Analysis	✅	Interprets health objectives and dietary restrictions
Meal Planning	✅	Generates 7-day personalized meal plans
Workout Recommendations	✅	Suggests customized fitness routines
Progress Tracking	✅	Logs daily/weekly activity and progress
Reminders & Scheduling	✅	Keeps users on track with scheduled routines
Expert Handoff	✅	Escalates to nutrition or injury support agents when needed
Streaming Responses	✅	Provides real-time, chatbot-like user experience
Secure & Guarded	✅	Input/output validation and controlled agent handoff
# ✅ SDK Features Overview
🧩 Feature	✅ Status	📄 Description
Agent + Tool Creation	✅ Yes	Created a main agent using Assistant(...) and integrated 5 domain-specific tools.
State Management	✅ Yes	Implemented UserSessionContext to maintain per-user state across conversations.
Guardrails (Input/Output)	✅ Yes	Applied via custom run_hooks using MyRunHooks, allowing validation and sanitization.
Real-Time Streaming	✅ Yes	Implemented via utils/streaming.py for live user feedback during longer responses.
Handoff to Another Agent	✅ Yes	Delegates tasks to nutrition_expert_agent, injury_support_agent, and escalation_agent.
Lifecycle Hooks	✅ Yes	Fully implemented using hooks/MyRunHooks.py for pre/post-p
🧩 Modular Architecture
health_wellness_agent/ ├── main.py # Entry

├── context/UserSessionContext.py # User session state management

├── tools/goal_analyzer.py # User goal analysis

├── tools/meal_planner.py # Meal planning tool

├── tools/workout_recommender.py # Workout recommendations

├── tools/scheduler.py # Weekly check-in scheduling

├── tools/tracker.py # Progress tracking

├── agents/nutrition_expert_agent.py # Nutrition expert handoff

├── agents/injury_support_agent.py # Injury support handoff

├── agents/escalation_agent.py # Coach escalation agent

├── hooks/MyRunHooks.py # Lifecycle hooks and validations

├── utils/streaming.py # Real-time streaming utils

├── planner_agent.py # Main assistant agent config

└── .env # Environment variables & API keys

# 🔧 Tools Overview
## 🛠️ Tool Name	📌 Purpose
GoalAnalyzerTool	Converts user goals into structured format using input/output guardrails
MealPlannerTool	Async tool to suggest 7-day meal plan honoring dietary preferences
WorkoutRecommenderTool	Suggests workout plan based on parsed goals and experience
CheckinSchedulerTool	Schedules recurring weekly progress checks
ProgressTrackerTool	Accepts updates, tracks user progress, modifies session context
🤝 Handoffs (Specialized Agents)
Specialized agents receive control through handoff() based on user input.

## 🤖 Agent Name	🎯 Trigger Condition
EscalationAgent	User wants to speak to a human coach
NutritionExpertAgent	Complex dietary needs like diabetes or allergies
InjurySupportAgent	Physical limitations or injury-specific workouts
📝 Each agent should:

Be declared and passed in the handoffs parameter of the main agent
Optionally implement on_handoff() for logging or initialization
# 📦 Context Management
A shared context class is used across all tools and agents to persist user-specific state.

class UserSessionContext(BaseModel): name: str

uid: int

goal: Optional[dict] = None

diet_preferences: Optional[str] = None

workout_plan: Optional[dict] = None

meal_plan: Optional[List[str]] = None

injury_notes: Optional[str] = None

handoff_logs: List[str] = []

progress_logs: List[Dict[str, str]] = []
# 🔒 Guardrails
## ✅ Input Guardrails:
Validate goal input format: quantity, metric, duration (e.g. "lose 5kg in 2 months")

Ensure valid dietary or injury-related inputs

Block unsupported or incomplete entries

## ✅ Output Guardrails:
Ensure tools return structured JSON or Pydantic models

Useful for validating and parsing agent responses

# 🔄 Streaming
Real-time responses are streamed using the Runner.stream(...) method:

async for step in Runner.stream(starting_agent=agent, input="Help me lose weight", context=user_context): print(step.pretty_output)

# 🔧 What I Implemented:
✅ CLI & Streamlit Interface ➤ Interact via terminal or a clean web UI

✅ FastAPI Backend ➤ Robust APIs for input/output handling

✅ Database Integration ➤ Store user goals, track progress, save meal/workout plans

✅ PDF Export Feature ➤ Save health goals as downloadable PDFs with timestamp

✅ AI Tools ➤ GoalAnalyzerTool, MealPlannerTool, WorkoutRecommender, ProgressTracker & more

✅ Real-Time Streaming ➤ Immediate feedback using async + WebSockets

✅ Agent Handoffs ➤ Delegate special cases to InjurySupportAgent, NutritionExpertAgent, EscalationAgent

# 🚀 Getting Started
Clone the repository:

git clone https://github.com/yourusername/health-wellness-agent.git

cd health-wellness-agent

Install dependencies:
pip install -r requirements.txt

Add your .env file:
GEMINI_API_KEY=your_gemini_api_key_here

Run the planner agent:
python main.py

(Optional) Run Streamlit dashboard:
streamlit run streamlit_app.py

# ✨ Made with ❤️ by Rabia
💻🚴‍♀️🍎 Building healthy habits, one line of code at a time.

Code + Care = Wellness Aware 💡💪
