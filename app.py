"""
DreamzLab ✨
Your dream journal — bring your dreams to reality.
Run: streamlit run app.py
"""
import sys
import os
import random
from datetime import datetime

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import (
    load_dreams, add_dream, toggle_milestone, delete_dream,
    add_milestone, get_daily_affirmation, get_progress,
    get_category_milestones,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DreamzLab ✨",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Palette ───────────────────────────────────────────────────────────────────
BG      = "#0a0a0f"
SURFACE = "#12121a"
CARD    = "#1a1a2e"
BORDER  = "#2d2d44"
TEXT    = "#f0e6ff"
SUB     = "#9d8ec0"
PURPLE  = "#b57bee"
PINK    = "#f472b6"
GOLD    = "#fbbf24"
TEAL    = "#34d399"
BLUE    = "#60a5fa"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background: {BG};
    color: {TEXT};
}}
[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
.main .block-container {{ padding-top: 1rem; padding-bottom: 2rem; max-width: 1200px; }}

/* Affirmation banner */
.affirmation {{
    background: linear-gradient(135deg, #1a1a2e 0%, #2d1b4e 50%, #1a2a3a 100%);
    border: 1px solid {BORDER};
    border-left: 4px solid {PURPLE};
    border-radius: 14px;
    padding: 22px 28px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}}
.affirmation::before {{
    content: '"';
    position: absolute;
    top: -10px; left: 16px;
    font-size: 6rem;
    color: {PURPLE};
    opacity: 0.15;
    font-family: 'Playfair Display', serif;
    line-height: 1;
}}
.affirmation-label {{
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: {PURPLE};
    margin-bottom: 8px;
}}
.affirmation-text {{
    font-size: 1.1rem;
    font-weight: 500;
    color: {TEXT};
    line-height: 1.6;
}}

/* Dream cards */
.dream-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 16px;
    position: relative;
}}
.dream-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
    background: linear-gradient(90deg, {PURPLE}, {PINK});
}}
.dream-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {TEXT};
    margin-bottom: 4px;
}}
.dream-desc {{
    font-size: .82rem;
    color: {SUB};
    line-height: 1.5;
    margin-bottom: 14px;
}}
.dream-date {{
    font-size: .7rem;
    color: {SUB};
}}

/* Progress bar */
.prog-wrap {{ background: {BORDER}; border-radius: 999px; height: 8px; margin: 10px 0; }}
.prog-bar  {{ height: 8px; border-radius: 999px; background: linear-gradient(90deg, {PURPLE}, {PINK}); }}

/* Milestone item */
.ms-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 4px;
    font-size: .85rem;
    background: {SURFACE};
    border: 1px solid {BORDER};
}}
.ms-done {{ opacity: 0.5; text-decoration: line-through; }}

/* Section header */
.sec {{
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: {SUB};
    margin: 28px 0 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.sec::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}

/* Stats */
.stat {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
}}
.stat-val {{
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, {PURPLE}, {PINK});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.stat-lbl {{ font-size: .72rem; color: {SUB}; margin-top: 4px; text-transform: uppercase; letter-spacing: .06em; }}

/* Badge */
.badge {{
    display: inline-block;
    font-size: .68rem;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 999px;
    background: rgba(181,123,238,.15);
    color: {PURPLE};
    border: 1px solid rgba(181,123,238,.3);
}}

hr {{ border-color: {BORDER} !important; }}
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: {SURFACE}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 3px; }}

div[data-testid="metric-container"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 14px 18px;
}}
[data-testid="stMetricValue"] {{ font-size: 1.7rem !important; font-weight: 700 !important; }}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def sec(title):
    st.markdown(f'<div class="sec">{title}</div>', unsafe_allow_html=True)

def progress_bar(pct):
    return (
        f'<div class="prog-wrap">'
        f'<div class="prog-bar" style="width:{pct}%"></div>'
        f'</div>'
    )

def stat_card(col, value, label):
    col.markdown(
        f'<div class="stat"><div class="stat-val">{value}</div>'
        f'<div class="stat-lbl">{label}</div></div>',
        unsafe_allow_html=True,
    )


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<div style="padding:8px 0 16px">'
        f'<div style="font-size:1.4rem;font-weight:700;color:{TEXT}">✨ DreamzLab</div>'
        f'<div style="font-size:.75rem;color:{SUB};margin-top:2px">Bring your dreams to reality</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    page = st.radio(
        "",
        ["🏠 Home", "💭 My Dreams", "➕ Add Dream", "📊 Progress"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown(
        f'<div style="font-size:.72rem;color:{SUB};line-height:1.8">'
        f'✨ Dream it<br>📝 Plan it<br>🎯 Do it<br>🏆 Live it'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Daily affirmation ─────────────────────────────────────────────────────────
affirmation = get_daily_affirmation()


# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown(
        f'<div style="font-size:2rem;font-weight:700;color:{TEXT};letter-spacing:-.02em;margin-bottom:4px">'
        f'Welcome to DreamzLab ✨</div>'
        f'<div style="font-size:.95rem;color:{SUB};margin-bottom:24px">'
        f'Your personal space to dream big, plan smart, and make it happen.</div>',
        unsafe_allow_html=True,
    )

    # Affirmation
    st.markdown(
        f'<div class="affirmation">'
        f'<div class="affirmation-label">✨ Your daily affirmation</div>'
        f'<div class="affirmation-text">{affirmation}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Stats
    dreams = load_dreams()
    total  = len(dreams)
    done_ms = sum(sum(1 for m in d["milestones"] if m["done"]) for d in dreams)
    total_ms = sum(len(d["milestones"]) for d in dreams)
    completed = sum(1 for d in dreams if d["milestones"] and all(m["done"] for m in d["milestones"]))

    sec("YOUR JOURNEY AT A GLANCE")
    c1, c2, c3, c4 = st.columns(4)
    stat_card(c1, str(total), "Dreams")
    stat_card(c2, str(total_ms), "Milestones")
    stat_card(c3, str(done_ms), "Completed")
    stat_card(c4, f"{int(done_ms/total_ms*100) if total_ms else 0}%", "Progress")

    # Recent dreams
    if dreams:
        sec("RECENT DREAMS")
        for dream in sorted(dreams, key=lambda x: x["created_at"], reverse=True)[:3]:
            pct = get_progress(dream)
            ms_done = sum(1 for m in dream["milestones"] if m["done"])
            ms_total = len(dream["milestones"])
            st.markdown(
                f'<div class="dream-card">'
                f'<div class="dream-title">{dream["title"]}</div>'
                f'<div class="dream-desc">{dream["description"][:120]}{"..." if len(dream["description"]) > 120 else ""}</div>'
                f'{progress_bar(pct)}'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px">'
                f'<span class="dream-date">📅 {dream["created_at"][:10]}</span>'
                f'<span class="badge">{ms_done}/{ms_total} milestones</span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f'<div style="text-align:center;padding:40px;color:{SUB}">'
            f'<div style="font-size:3rem">💭</div>'
            f'<div style="font-size:1rem;margin-top:12px">No dreams yet.</div>'
            f'<div style="font-size:.85rem;margin-top:6px">Go to "Add Dream" to start your journey.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Motivational quote
    sec("REMEMBER THIS")
    quotes = [
        ("The secret of getting ahead is getting started.", "Mark Twain"),
        ("All our dreams can come true if we have the courage to pursue them.", "Walt Disney"),
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
        ("It always seems impossible until it's done.", "Nelson Mandela"),
        ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ]
    q, author = quotes[datetime.now().day % len(quotes)]
    st.markdown(
        f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:20px 24px;'
        f'border-left:4px solid {GOLD}">'
        f'<div style="font-size:1rem;color:{TEXT};font-style:italic;line-height:1.6">"{q}"</div>'
        f'<div style="font-size:.78rem;color:{GOLD};margin-top:8px;font-weight:600">— {author}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# MY DREAMS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💭 My Dreams":
    st.markdown(
        f'<div style="font-size:1.6rem;font-weight:700;color:{TEXT};margin-bottom:4px">💭 My Dreams</div>'
        f'<div style="font-size:.85rem;color:{SUB};margin-bottom:20px">Track and manage your dreams and milestones</div>',
        unsafe_allow_html=True,
    )

    # Affirmation strip
    st.markdown(
        f'<div style="background:{CARD};border:1px solid {BORDER};border-left:3px solid {PURPLE};'
        f'border-radius:10px;padding:12px 16px;margin-bottom:20px;font-size:.85rem;color:{TEXT}">'
        f'✨ {affirmation}</div>',
        unsafe_allow_html=True,
    )

    dreams = load_dreams()
    if not dreams:
        st.markdown(
            f'<div style="text-align:center;padding:60px;color:{SUB}">'
            f'<div style="font-size:4rem">💭</div>'
            f'<div style="font-size:1.1rem;margin-top:16px;color:{TEXT}">Your dream journal is empty</div>'
            f'<div style="font-size:.85rem;margin-top:8px">Head to "Add Dream" to plant your first seed 🌱</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        for dream in dreams:
            pct = get_progress(dream)
            ms_done  = sum(1 for m in dream["milestones"] if m["done"])
            ms_total = len(dream["milestones"])

            with st.expander(f"{'🏆' if pct == 100 else '🌱' if pct == 0 else '🚀'} {dream['title']}  —  {pct}% complete", expanded=False):
                st.markdown(
                    f'<div style="color:{SUB};font-size:.85rem;margin-bottom:10px">{dream["description"]}</div>'
                    f'{progress_bar(pct)}'
                    f'<div style="font-size:.75rem;color:{SUB};margin-bottom:16px">'
                    f'{ms_done} of {ms_total} milestones complete · Started {dream["created_at"][:10]}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(f'<div style="font-size:.78rem;font-weight:600;color:{SUB};margin-bottom:8px;text-transform:uppercase;letter-spacing:.06em">MILESTONES</div>', unsafe_allow_html=True)

                for ms in dream["milestones"]:
                    col1, col2 = st.columns([0.07, 0.93])
                    with col1:
                        checked = st.checkbox("", value=ms["done"], key=f"ms_{ms['id']}")
                        if checked != ms["done"]:
                            toggle_milestone(dream["id"], ms["id"])
                            st.rerun()
                    with col2:
                        style = f"text-decoration:line-through;opacity:.5;color:{SUB}" if ms["done"] else f"color:{TEXT}"
                        icon = "✅" if ms["done"] else "⭕"
                        st.markdown(f'<div style="padding:6px 0;font-size:.85rem;{style}">{icon} {ms["text"]}</div>', unsafe_allow_html=True)

                # Add milestone
                st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
                with st.form(key=f"add_ms_{dream['id']}"):
                    new_ms = st.text_input("Add a new milestone", placeholder="e.g. Complete first draft by Friday", label_visibility="collapsed")
                    if st.form_submit_button("➕ Add Milestone") and new_ms.strip():
                        add_milestone(dream["id"], new_ms.strip())
                        st.rerun()

                # Delete dream
                st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
                if st.button(f"🗑️ Delete this dream", key=f"del_{dream['id']}"):
                    delete_dream(dream["id"])
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# ADD DREAM
# ══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Add Dream":
    st.markdown(
        f'<div style="font-size:1.6rem;font-weight:700;color:{TEXT};margin-bottom:4px">➕ Add a Dream</div>'
        f'<div style="font-size:.85rem;color:{SUB};margin-bottom:24px">Describe your dream and we\'ll help you plan the journey</div>',
        unsafe_allow_html=True,
    )

    with st.form("add_dream_form"):
        title = st.text_input("Dream title *", placeholder="e.g. Start my own business, Run a marathon, Learn Spanish")
        description = st.text_area(
            "Describe your dream *",
            placeholder="Tell us more about this dream. What does it mean to you? What would achieving it look like?",
            height=120,
        )

        st.markdown(f'<div style="margin-top:8px;font-size:.85rem;color:{SUB}">How would you like to set milestones?</div>', unsafe_allow_html=True)
        milestone_mode = st.radio(
            "",
            ["✨ Suggest milestones for me", "✏️ I'll write my own"],
            label_visibility="collapsed",
        )
        custom_milestones = ""
        if milestone_mode == "✏️ I'll write my own":
            custom_milestones = st.text_area(
                "Your milestones (one per line)",
                placeholder="Step 1: ...\nStep 2: ...\nStep 3: ...",
                height=150,
            )

        submitted = st.form_submit_button("🚀 Start My Journey", type="primary", use_container_width=True)

    if submitted:
        if not title.strip() or not description.strip():
            st.error("Please fill in both the title and description.")
        else:
            if milestone_mode == "✨ Suggest milestones for me":
                milestones = get_category_milestones(title + " " + description)
            else:
                milestones = [m.strip() for m in custom_milestones.split("\n") if m.strip()]
                if not milestones:
                    milestones = get_category_milestones(title + " " + description)

            dream = add_dream(title.strip(), description.strip(), milestones)
            st.success(f"✨ Dream added! {len(milestones)} milestones created.")
            st.balloons()

            st.markdown(
                f'<div class="dream-card" style="margin-top:16px">'
                f'<div class="dream-title">{dream["title"]}</div>'
                f'<div class="dream-desc">{dream["description"]}</div>'
                f'<div style="font-size:.78rem;font-weight:600;color:{SUB};margin-bottom:8px;text-transform:uppercase;letter-spacing:.06em">YOUR MILESTONES</div>',
                unsafe_allow_html=True,
            )
            for i, ms in enumerate(dream["milestones"], 1):
                st.markdown(f'<div style="padding:6px 0;font-size:.85rem;color:{TEXT}">⭕ {i}. {ms["text"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PROGRESS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Progress":
    st.markdown(
        f'<div style="font-size:1.6rem;font-weight:700;color:{TEXT};margin-bottom:4px">📊 Your Progress</div>'
        f'<div style="font-size:.85rem;color:{SUB};margin-bottom:24px">See how far you\'ve come on every dream</div>',
        unsafe_allow_html=True,
    )

    dreams = load_dreams()
    if not dreams:
        st.markdown(
            f'<div style="text-align:center;padding:60px;color:{SUB}">'
            f'<div style="font-size:4rem">📊</div>'
            f'<div style="font-size:1rem;margin-top:16px">No dreams to show progress for yet.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        # Summary stats
        total_ms   = sum(len(d["milestones"]) for d in dreams)
        done_ms    = sum(sum(1 for m in d["milestones"] if m["done"]) for d in dreams)
        completed  = sum(1 for d in dreams if d["milestones"] and all(m["done"] for m in d["milestones"]))
        in_progress = sum(1 for d in dreams if any(m["done"] for m in d["milestones"]) and not all(m["done"] for m in d["milestones"]))

        sec("OVERALL STATS")
        c1, c2, c3, c4 = st.columns(4)
        stat_card(c1, str(len(dreams)), "Total Dreams")
        stat_card(c2, str(completed), "Completed")
        stat_card(c3, str(in_progress), "In Progress")
        stat_card(c4, f"{int(done_ms/total_ms*100) if total_ms else 0}%", "Overall")

        # Progress per dream
        sec("PROGRESS BY DREAM")
        df = pd.DataFrame([
            {
                "Dream": d["title"][:30] + ("..." if len(d["title"]) > 30 else ""),
                "Progress %": get_progress(d),
                "Done": sum(1 for m in d["milestones"] if m["done"]),
                "Total": len(d["milestones"]),
            }
            for d in dreams
        ])

        fig = px.bar(
            df, x="Progress %", y="Dream", orientation="h",
            color="Progress %",
            color_continuous_scale=[[0, "#2d1b4e"], [0.5, PURPLE], [1.0, PINK]],
            labels={"Progress %": "Completion %", "Dream": ""},
            text="Progress %",
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(
            plot_bgcolor=BG, paper_bgcolor=CARD,
            font=dict(family="Inter", color=SUB, size=11),
            margin=dict(l=8, r=40, t=8, b=8), height=max(250, len(dreams) * 60),
            coloraxis_showscale=False,
            xaxis=dict(range=[0, 110], gridcolor=BORDER, tickfont=dict(color=SUB)),
            yaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT, size=12)),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Dream breakdown
        sec("DREAM DETAILS")
        for dream in dreams:
            pct = get_progress(dream)
            ms_done  = sum(1 for m in dream["milestones"] if m["done"])
            ms_total = len(dream["milestones"])
            color = PINK if pct == 100 else PURPLE if pct > 50 else BLUE

            st.markdown(
                f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;'
                f'padding:16px 20px;margin-bottom:12px">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
                f'<div style="font-weight:600;color:{TEXT}">{dream["title"]}</div>'
                f'<div style="font-size:.85rem;color:{color};font-weight:600">{pct}%</div>'
                f'</div>'
                f'{progress_bar(pct)}'
                f'<div style="font-size:.75rem;color:{SUB};margin-top:6px">'
                f'{ms_done} of {ms_total} milestones · Started {dream["created_at"][:10]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    f'<div style="text-align:center;font-size:.72rem;color:{SUB}">'
    f'✨ DreamzLab · Bring your dreams to reality · Built with 💜'
    f'</div>',
    unsafe_allow_html=True,
)
