# ✨ DreamzLab

**Bring your dreams to reality.**

DreamzLab is your personal dream journal and life planner. Write down your dreams, get AI-suggested milestones, track your progress, and receive daily affirmations to keep you motivated.

## Features

- 💭 **Dream Journal** — capture and describe your dreams/goals
- ✨ **Daily Affirmations** — a fresh motivational message every day
- 🎯 **Smart Milestones** — auto-suggested based on your dream category, or write your own
- 📊 **Progress Tracking** — visual progress bars and stats for every dream
- 🏆 **Journey View** — see all your dreams and how far you've come

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo, set main file to `app.py`
4. Deploy — get a shareable public URL

## Categories Supported

| Category | Auto-detected from |
|---|---|
| Career | job, business, startup, promotion |
| Health | fitness, weight, exercise, gym |
| Learning | study, course, skill, language |
| Financial | money, savings, invest, debt |
| Relationships | love, family, social, connect |
| Creative | art, music, writing, design |

## Stack

- Python 3.8+
- Streamlit
- Plotly
- Pandas
- JSON file storage (no database needed)
