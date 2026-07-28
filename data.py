"""
DreamzLab — Data layer
Uses JSON files for persistence. No database required.
"""
import json
import os
import uuid
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".dreamzlab_data")
DREAMS_FILE = os.path.join(DATA_DIR, "dreams.json")

# ── Affirmations ──────────────────────────────────────────────────────────────
AFFIRMATIONS = [
    "You are capable of achieving everything you set your mind to. 🌟",
    "Every step forward, no matter how small, brings you closer to your dream. 🚶",
    "Your dreams are valid. Your goals are achievable. Keep going. 💫",
    "The journey of a thousand miles begins with a single step. 🌈",
    "You have survived 100% of your hardest days. You can do this. 💪",
    "Believe in yourself. You are more powerful than you know. ✨",
    "Progress, not perfection. Every day counts. 🎯",
    "Your future self is cheering for you right now. 🙌",
    "Dream big. Start small. Act now. 🚀",
    "You are exactly where you need to be on your journey. 🌸",
    "Challenges are just opportunities in disguise. 🦋",
    "The best time to start was yesterday. The second best time is now. ⏰",
    "Your potential is limitless. Don't let anyone — including yourself — tell you otherwise. 💎",
    "Small consistent actions create extraordinary results. 🌱",
    "You are worthy of the life you dream about. 👑",
    "Trust the process. Your dreams are unfolding perfectly. 🌺",
    "Every expert was once a beginner. Keep learning, keep growing. 📚",
    "Your dreams matter. You matter. Never stop believing. ❤️",
    "The only limit is the one you set in your mind. Break free. 🦅",
    "Today is a great day to make progress on your dreams. Let's go! 🎉",
    "You are braver than you believe, stronger than you seem. 🌟",
    "Success is not a destination — it's a journey you're already on. 🛤️",
    "Each morning brings a new chance to move closer to your dream. 🌅",
    "Your story isn't over. The best chapters are still being written. 📖",
    "Celebrate every small win. They all add up. 🏆",
    "You have everything you need to begin. Start today. 🌻",
    "Doubt kills more dreams than failure ever will. Believe. 💡",
    "The dream in your heart was placed there for a reason. Chase it. 🌙",
    "Resilience is your superpower. You've got this. ⚡",
    "One day closer. One step stronger. Keep going. 🔥",
]

MILESTONE_SUGGESTIONS = {
    "career": [
        "Update your resume and LinkedIn profile",
        "Research 10 companies you'd love to work for",
        "Reach out to 3 people in your target industry",
        "Complete one online course relevant to your goal",
        "Apply to 5 positions per week",
        "Schedule informational interviews with 2 professionals",
        "Build a portfolio project showcasing your skills",
    ],
    "health": [
        "Schedule a check-up with your doctor",
        "Set a consistent sleep schedule (7-8 hours)",
        "Start with 15 minutes of exercise daily",
        "Meal prep healthy lunches for the week",
        "Drink 8 glasses of water daily for 2 weeks",
        "Find a workout buddy for accountability",
        "Track your progress with a health journal",
    ],
    "learning": [
        "Define exactly what you want to learn and why",
        "Find the top 3 resources (books, courses, mentors)",
        "Dedicate 30 minutes daily to learning",
        "Join a community of people with the same goal",
        "Teach someone else what you've learned",
        "Complete one project applying your new skills",
        "Set a milestone date to demonstrate your knowledge",
    ],
    "financial": [
        "Track all your expenses for one month",
        "Create a monthly budget",
        "Set up automatic savings (even $10/week)",
        "Pay off the smallest debt first (snowball method)",
        "Research one investment option",
        "Find one way to increase your income",
        "Build a 3-month emergency fund",
    ],
    "relationship": [
        "Identify the qualities you value most",
        "Invest in existing relationships first",
        "Join groups aligned with your interests",
        "Practice being present in conversations",
        "Set healthy boundaries with clarity and kindness",
        "Schedule regular quality time with loved ones",
        "Write a letter of appreciation to someone important",
    ],
    "creative": [
        "Set aside 20 minutes daily for creative practice",
        "Complete one small creative project this week",
        "Share your work with one trusted person",
        "Study the work of creators you admire",
        "Enter one competition or open call",
        "Build an audience by posting consistently",
        "Collaborate with another creative person",
    ],
    "default": [
        "Define your dream clearly — write it down in detail",
        "Research what success looks like for this dream",
        "Identify 3 people who have achieved something similar",
        "Break the dream into 3 major phases",
        "Complete the first small action this week",
        "Find an accountability partner",
        "Set a review date to assess your progress",
    ],
}

def get_category_milestones(dream_text: str) -> list:
    text = dream_text.lower()
    if any(w in text for w in ["job", "career", "work", "promotion", "business", "startup"]):
        return MILESTONE_SUGGESTIONS["career"]
    if any(w in text for w in ["health", "fit", "weight", "exercise", "gym", "run", "diet"]):
        return MILESTONE_SUGGESTIONS["health"]
    if any(w in text for w in ["learn", "study", "skill", "course", "degree", "language"]):
        return MILESTONE_SUGGESTIONS["learning"]
    if any(w in text for w in ["money", "save", "invest", "debt", "financial", "rich", "wealth"]):
        return MILESTONE_SUGGESTIONS["financial"]
    if any(w in text for w in ["relationship", "love", "family", "friend", "social", "connect"]):
        return MILESTONE_SUGGESTIONS["relationship"]
    if any(w in text for w in ["art", "music", "write", "creative", "paint", "design", "film"]):
        return MILESTONE_SUGGESTIONS["creative"]
    return MILESTONE_SUGGESTIONS["default"]


# ── Persistence ───────────────────────────────────────────────────────────────
def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_dreams() -> list:
    _ensure_data_dir()
    if not os.path.exists(DREAMS_FILE):
        return []
    with open(DREAMS_FILE, "r") as f:
        return json.load(f)

def save_dreams(dreams: list):
    _ensure_data_dir()
    with open(DREAMS_FILE, "w") as f:
        json.dump(dreams, f, indent=2)

def add_dream(title: str, description: str, milestones: list) -> dict:
    dreams = load_dreams()
    dream = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "milestones": [
            {
                "id": str(uuid.uuid4()),
                "text": m,
                "done": False,
                "completed_at": None,
            }
            for m in milestones
        ],
    }
    dreams.append(dream)
    save_dreams(dreams)
    return dream

def toggle_milestone(dream_id: str, milestone_id: str):
    dreams = load_dreams()
    for dream in dreams:
        if dream["id"] == dream_id:
            for ms in dream["milestones"]:
                if ms["id"] == milestone_id:
                    ms["done"] = not ms["done"]
                    ms["completed_at"] = datetime.now().isoformat() if ms["done"] else None
    save_dreams(dreams)

def delete_dream(dream_id: str):
    dreams = [d for d in load_dreams() if d["id"] != dream_id]
    save_dreams(dreams)

def add_milestone(dream_id: str, text: str):
    dreams = load_dreams()
    for dream in dreams:
        if dream["id"] == dream_id:
            dream["milestones"].append({
                "id": str(uuid.uuid4()),
                "text": text,
                "done": False,
                "completed_at": None,
            })
    save_dreams(dreams)

def get_daily_affirmation() -> str:
    day_of_year = datetime.now().timetuple().tm_yday
    return AFFIRMATIONS[day_of_year % len(AFFIRMATIONS)]

def get_progress(dream: dict) -> float:
    ms = dream.get("milestones", [])
    if not ms:
        return 0.0
    return round(sum(1 for m in ms if m["done"]) / len(ms) * 100, 1)
