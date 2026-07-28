"""
DreamzLab ✨ — Bring your dreams to reality
Run: streamlit run app.py
"""
import sys, os, random
from datetime import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import (
    load_dreams, add_dream, toggle_milestone, delete_dream,
    add_milestone, get_daily_affirmation, get_progress,
    generate_specific_milestones,
)

st.set_page_config(page_title="DreamzLab ✨", page_icon="✨", layout="wide",
                   initial_sidebar_state="expanded")

# ── Palette ────────────────────────────────────────────────────────────────────
BG     = "#07080f"
SURF   = "#0f1018"
CARD   = "#13141f"
CARD2  = "#1a1b2e"
BORDER = "#252638"
TEXT   = "#f0ecff"
SUB    = "#8b85b0"
PURPLE = "#a78bfa"
PINK   = "#f472b6"
GOLD   = "#fbbf24"
TEAL   = "#2dd4bf"
BLUE   = "#60a5fa"
GREEN  = "#4ade80"

# ── Category config (image + colour) ─────────────────────────────────────────
CATEGORIES = {
    "career":    {"emoji":"🚀","color":"#818cf8","img":"https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&q=80"},
    "health":    {"emoji":"💪","color":"#4ade80","img":"https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80"},
    "creative":  {"emoji":"🎨","color":"#f472b6","img":"https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=600&q=80"},
    "travel":    {"emoji":"✈️","color":"#38bdf8","img":"https://images.unsplash.com/photo-1488085061387-422e29b40080?w=600&q=80"},
    "education": {"emoji":"📚","color":"#fbbf24","img":"https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=600&q=80"},
    "financial": {"emoji":"💰","color":"#34d399","img":"https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=600&q=80"},
    "music":     {"emoji":"🎵","color":"#c084fc","img":"https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600&q=80"},
    "startup":   {"emoji":"🦄","color":"#fb923c","img":"https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=600&q=80"},
    "fitness":   {"emoji":"🏃","color":"#f87171","img":"https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80"},
    "relationship":{"emoji":"❤️","color":"#f472b6","img":"https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=600&q=80"},
    "default":   {"emoji":"🌟","color":"#a78bfa","img":"https://images.unsplash.com/photo-1464852045489-bccb7d17fe39?w=600&q=80"},
}

def get_category(title: str, description: str) -> str:
    t = (title + " " + description).lower()
    if any(w in t for w in ["startup","founder","saas","product","venture"]): return "startup"
    if any(w in t for w in ["career","job","promotion","resume","linkedin"]): return "career"
    if any(w in t for w in ["marathon","run","race","5k","triathlon"]): return "fitness"
    if any(w in t for w in ["health","diet","nutrition","lose weight","eat"]): return "health"
    if any(w in t for w in ["art","paint","draw","design","creative","craft"]): return "creative"
    if any(w in t for w in ["travel","trip","visit","country","abroad","backpack"]): return "travel"
    if any(w in t for w in ["learn","study","degree","university","course","language"]): return "education"
    if any(w in t for w in ["invest","save","money","financial","wealth","retire"]): return "financial"
    if any(w in t for w in ["music","song","album","guitar","sing","piano","record"]): return "music"
    if any(w in t for w in ["relationship","love","family","partner","social","friend"]): return "relationship"
    return "default"

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

html,body,[class*="css"]{{font-family:'Inter',sans-serif;background:{BG};color:{TEXT}}}
[data-testid="stSidebar"]{{background:{SURF}!important;border-right:1px solid {BORDER}}}
[data-testid="stSidebar"] *{{color:{TEXT}!important}}
.main .block-container{{padding-top:.8rem;padding-bottom:2rem;max-width:1300px}}

/* ── Hero ── */
.hero{{
  background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
  border-radius:20px;padding:52px 48px;margin-bottom:28px;
  position:relative;overflow:hidden;
}}
.hero::after{{
  content:'';position:absolute;top:-60px;right:-60px;
  width:280px;height:280px;border-radius:50%;
  background:radial-gradient(circle,rgba(167,139,250,.25),transparent 70%);
}}
.hero-tag{{font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:{PURPLE};margin-bottom:10px}}
.hero-title{{font-family:'Playfair Display',serif;font-size:2.6rem;line-height:1.15;
  color:#fff;margin-bottom:12px}}
.hero-sub{{font-size:1rem;color:rgba(240,236,255,.65);line-height:1.6;max-width:520px}}

/* ── Affirmation ── */
.affirmation{{
  background:linear-gradient(135deg,{CARD2} 0%,#1e1040 100%);
  border:1px solid {BORDER};border-left:4px solid {PURPLE};
  border-radius:16px;padding:24px 28px;margin-bottom:28px;position:relative;overflow:hidden;
}}
.affirmation::before{{content:'"';position:absolute;top:-14px;left:14px;
  font-size:7rem;color:{PURPLE};opacity:.1;font-family:'Playfair Display',serif;line-height:1}}
.aff-label{{font-size:.65rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:{PURPLE};margin-bottom:8px}}
.aff-text{{font-size:1.05rem;font-weight:500;color:{TEXT};line-height:1.65}}

/* ── Dream card with image ── */
.dcard{{border-radius:18px;overflow:hidden;border:1px solid {BORDER};
  background:{CARD};margin-bottom:18px;transition:transform .15s ease}}
.dcard:hover{{transform:translateY(-3px)}}
.dcard-img{{width:100%;height:160px;object-fit:cover;display:block}}
.dcard-img-placeholder{{
  width:100%;height:160px;display:flex;align-items:center;justify-content:center;
  font-size:64px;
}}
.dcard-body{{padding:18px 20px}}
.dcard-title{{font-size:1rem;font-weight:700;color:{TEXT};margin-bottom:4px}}
.dcard-desc{{font-size:.78rem;color:{SUB};line-height:1.5;margin-bottom:12px}}
.dcard-prog{{background:{BORDER};border-radius:999px;height:6px;margin:8px 0}}
.dcard-prog-fill{{height:6px;border-radius:999px;background:linear-gradient(90deg,{PURPLE},{PINK})}}
.dcard-footer{{display:flex;justify-content:space-between;align-items:center;margin-top:10px}}
.dcard-date{{font-size:.68rem;color:{SUB}}}
.dcard-badge{{font-size:.68rem;font-weight:600;padding:3px 10px;border-radius:999px;
  background:rgba(167,139,250,.15);color:{PURPLE};border:1px solid rgba(167,139,250,.25)}}

/* ── Stat card ── */
.scard{{background:{CARD};border:1px solid {BORDER};border-radius:14px;
  padding:20px;text-align:center;position:relative;overflow:hidden}}
.scard::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px}}
.scard.purple::before{{background:linear-gradient(90deg,{PURPLE},{PINK})}}
.scard.teal::before{{background:linear-gradient(90deg,{TEAL},{BLUE})}}
.scard.gold::before{{background:linear-gradient(90deg,{GOLD},#f97316)}}
.scard.green::before{{background:linear-gradient(90deg,{GREEN},{TEAL})}}
.scard-val{{font-size:2.2rem;font-weight:800;
  background:linear-gradient(135deg,{PURPLE},{PINK});
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.scard-lbl{{font-size:.68rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
  color:{SUB};margin-top:4px}}

/* ── Section header ── */
.sec{{font-size:.65rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:{SUB};margin:28px 0 14px;display:flex;align-items:center;gap:8px}}
.sec::after{{content:'';flex:1;height:1px;background:{BORDER}}}

/* ── Quote card ── */
.qcard{{background:{CARD};border:1px solid {BORDER};border-left:4px solid {GOLD};
  border-radius:14px;padding:22px 26px}}
.qcard-text{{font-size:.95rem;color:{TEXT};font-style:italic;line-height:1.65}}
.qcard-author{{font-size:.75rem;color:{GOLD};font-weight:700;margin-top:10px}}

/* ── Category pill ── */
.cat-pill{{display:inline-flex;align-items:center;gap:5px;padding:4px 12px;
  border-radius:999px;font-size:.72rem;font-weight:600;border:1px solid {BORDER};
  background:{CARD2};color:{TEXT};margin-bottom:8px}}

/* ── Progress bar ── */
.pb{{background:{BORDER};border-radius:999px;height:8px;margin:8px 0}}
.pb-fill{{height:8px;border-radius:999px;background:linear-gradient(90deg,{PURPLE},{PINK})}}

/* ── Hide radio button dots, style as clean nav ── */
[data-testid="stRadio"] > div {{ gap: 2px !important; }}
[data-testid="stRadio"] label {{
    background: transparent !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    cursor: pointer !important;
    transition: background .15s ease !important;
    width: 100% !important;
}}
[data-testid="stRadio"] label:hover {{ background: rgba(167,139,250,.1) !important; }}
[data-testid="stRadio"] label[data-baseweb="radio"] {{ background: rgba(167,139,250,.15) !important; }}
[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {{
    font-size: .88rem !important;
    font-weight: 500 !important;
    color: #f0ecff !important;
}}
/* Hide the actual radio circle */
[data-testid="stRadio"] input[type="radio"] {{ display: none !important; }}
[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {{ display: none !important; }}

/* ── Sidebar nav buttons ── */
[data-testid="stSidebar"] [data-testid="stButton"] button {{
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    color: {SUB} !important;
    font-size: .88rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 10px 14px !important;
    width: 100% !important;
    transition: background .15s ease, color .15s ease !important;
}}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {{
    background: rgba(167,139,250,.12) !important;
    color: {TEXT} !important;
}}
::-webkit-scrollbar{{width:5px}}
::-webkit-scrollbar-track{{background:{SURF}}}
::-webkit-scrollbar-thumb{{background:{BORDER};border-radius:3px}}
div[data-testid="metric-container"]{{background:{CARD};border:1px solid {BORDER};border-radius:10px;padding:14px 18px}}
[data-testid="stMetricValue"]{{font-size:1.7rem!important;font-weight:800!important}}
[data-testid="stMetricLabel"]{{font-size:.7rem!important;color:{SUB}!important;text-transform:uppercase;letter-spacing:.06em}}
.stExpander{{border:1px solid {BORDER}!important;border-radius:14px!important;background:{CARD}!important}}

/* ── Mobile responsiveness ── */
@media (max-width: 768px) {{
  .hero{{padding:32px 24px}}
  .hero-title{{font-size:1.8rem}}
  .hero-sub{{font-size:.88rem}}
  .dcard-img, .dcard-img-placeholder{{height:120px}}
  .scard-val{{font-size:1.6rem}}
}}
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def sec(title): st.markdown(f'<div class="sec">{title}</div>', unsafe_allow_html=True)

def pb(pct):
    return f'<div class="pb"><div class="pb-fill" style="width:{pct}%"></div></div>'

def scard(col, value, label, variant="purple"):
    col.markdown(f'<div class="scard {variant}"><div class="scard-val">{value}</div>'
                 f'<div class="scard-lbl">{label}</div></div>', unsafe_allow_html=True)

def dream_card(dream):
    pct = get_progress(dream)
    ms_done  = sum(1 for m in dream["milestones"] if m["done"])
    ms_total = len(dream["milestones"])
    cat = get_category(dream["title"], dream.get("description",""))
    info = CATEGORIES.get(cat, CATEGORIES["default"])
    img_url = info["img"]
    emoji = info["emoji"]
    color = info["color"]

    st.markdown(f"""
    <div class="dcard">
      <img src="{img_url}" class="dcard-img"
           onerror="this.parentNode.querySelector('.dcard-img-placeholder').style.display='flex';this.style.display='none'">
      <div class="dcard-img-placeholder" style="display:none;background:{CARD2}">{emoji}</div>
      <div class="dcard-body">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
          <span class="cat-pill" style="border-color:{color}33;color:{color}">{emoji} {cat}</span>
        </div>
        <div class="dcard-title">{dream["title"]}</div>
        <div class="dcard-desc">{dream.get("description","")[:110]}{"..." if len(dream.get("description",""))>110 else ""}</div>
        {pb(pct)}
        <div class="dcard-footer">
          <span class="dcard-date">📅 {dream["created_at"][:10]}</span>
          <span class="dcard-badge">{ms_done}/{ms_total} milestones · {pct}%</span>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

affirmation = get_daily_affirmation()
dreams_all  = load_dreams()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 20px">
      <div style="font-size:1.4rem;font-weight:800;color:{TEXT};letter-spacing:-.01em">✨ DreamzLab</div>
      <div style="font-size:.72rem;color:{SUB};margin-top:3px;letter-spacing:.02em">Bring your dreams to reality</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    # Clean button navigation
    nav_items = ["🏠 Home", "💭 My Dreams", "➕ Add Dream", "📊 Progress"]
    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"

    for item in nav_items:
        if st.sidebar.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item
            st.rerun()

    page = st.session_state.page

    if dreams_all:
        st.divider()
        total_ms = sum(len(d["milestones"]) for d in dreams_all)
        done_ms  = sum(sum(1 for m in d["milestones"] if m["done"]) for d in dreams_all)
        pct_overall = int(done_ms/total_ms*100) if total_ms else 0
        st.markdown(
            f'<div style="font-size:.65rem;font-weight:700;letter-spacing:.1em;'
            f'text-transform:uppercase;color:{SUB};margin-bottom:8px">OVERALL PROGRESS</div>'
            f'{pb(pct_overall)}'
            f'<div style="font-size:.72rem;color:{PURPLE};font-weight:600;margin-top:4px">'
            f'{pct_overall}% of all milestones done</div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown(
        f'<div style="font-size:.72rem;color:{SUB};line-height:2.2">'
        f'✨ Dream it &nbsp; 📝 Plan it &nbsp; 🎯 Do it &nbsp; 🏆 Live it</div>',
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    # Hero
    st.markdown(f"""
    <div class="hero">
      <div class="hero-tag">✨ Your Dream Journal</div>
      <div class="hero-title">Make Your Dreams<br>Your Reality</div>
      <div class="hero-sub">Set intentions. Build milestones. Get daily motivation.
      Every big dream starts with one small step taken today.</div>
    </div>""", unsafe_allow_html=True)

    # Daily affirmation
    st.markdown(f"""
    <div class="affirmation">
      <div class="aff-label">✨ Your daily affirmation</div>
      <div class="aff-text">{affirmation}</div>
    </div>""", unsafe_allow_html=True)

    # Stats
    total    = len(dreams_all)
    done_ms  = sum(sum(1 for m in d["milestones"] if m["done"]) for d in dreams_all)
    total_ms = sum(len(d["milestones"]) for d in dreams_all)
    completed = sum(1 for d in dreams_all if d["milestones"] and all(m["done"] for m in d["milestones"]))

    sec("YOUR JOURNEY AT A GLANCE")
    c1,c2,c3,c4 = st.columns(4)
    scard(c1, str(total),    "Dreams",           "purple")
    scard(c2, str(total_ms), "Milestones",        "teal")
    scard(c3, str(done_ms),  "Completed",         "green")
    scard(c4, f"{int(done_ms/total_ms*100) if total_ms else 0}%", "Progress", "gold")

    # Recent dreams with images
    if dreams_all:
        sec("RECENT DREAMS")
        recent = sorted(dreams_all, key=lambda x: x["created_at"], reverse=True)[:3]
        cols = st.columns(min(len(recent), 3))
        for col, dream in zip(cols, recent):
            with col:
                dream_card(dream)
    else:
        st.markdown(f"""
        <div style="text-align:center;padding:60px 20px;background:{CARD};border:1px solid {BORDER};
             border-radius:18px;margin-top:16px">
          <div style="font-size:4rem;margin-bottom:16px">💭</div>
          <div style="font-size:1.1rem;font-weight:600;color:{TEXT}">No dreams yet</div>
          <div style="font-size:.85rem;color:{SUB};margin-top:6px">
            Click "➕ Add Dream" in the sidebar to plant your first seed 🌱</div>
        </div>""", unsafe_allow_html=True)

    # Quote
    sec("DAILY INSPIRATION")
    quotes = [
        ("All our dreams can come true, if we have the courage to pursue them.", "Walt Disney"),
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
        ("It always seems impossible until it's done.", "Nelson Mandela"),
        ("The secret of getting ahead is getting started.", "Mark Twain"),
        ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
        ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
        ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
    ]
    q, author = quotes[datetime.now().timetuple().tm_yday % len(quotes)]
    st.markdown(f"""
    <div class="qcard">
      <div class="qcard-text">"{q}"</div>
      <div class="qcard-author">— {author}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MY DREAMS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💭 My Dreams":
    st.markdown(f"""
    <div style="margin-bottom:20px">
      <div style="font-size:1.7rem;font-weight:800;color:{TEXT};letter-spacing:-.02em">💭 My Dreams</div>
      <div style="font-size:.88rem;color:{SUB};margin-top:4px">Track and manage your dreams and milestones</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="affirmation" style="padding:14px 20px"><div class="aff-label">✨ Today</div><div class="aff-text" style="font-size:.9rem">{affirmation}</div></div>', unsafe_allow_html=True)

    if not dreams_all:
        st.markdown(f"""
        <div style="text-align:center;padding:80px 20px;background:{CARD};border:1px solid {BORDER};border-radius:18px">
          <div style="font-size:5rem">💭</div>
          <div style="font-size:1.2rem;font-weight:600;color:{TEXT};margin-top:16px">Your dream journal is empty</div>
          <div style="font-size:.85rem;color:{SUB};margin-top:8px">Head to "➕ Add Dream" to plant your first seed 🌱</div>
        </div>""", unsafe_allow_html=True)
    else:
        # ── Search & filter ──
        fc1, fc2 = st.columns([2, 1])
        with fc1:
            search = st.text_input("Search", placeholder="🔍 Search dreams by title or keyword…",
                                    label_visibility="collapsed")
        with fc2:
            all_cats = sorted(set(get_category(d["title"], d.get("description","")) for d in dreams_all))
            cat_filter = st.selectbox("Category", ["All categories"] + all_cats, label_visibility="collapsed")

        filtered = dreams_all
        if search:
            s = search.lower()
            filtered = [d for d in filtered if s in d["title"].lower() or s in d.get("description","").lower()]
        if cat_filter != "All categories":
            filtered = [d for d in filtered if get_category(d["title"], d.get("description","")) == cat_filter]

        if not filtered:
            st.markdown(f"""
            <div style="text-align:center;padding:40px 20px;background:{CARD};border:1px solid {BORDER};border-radius:14px;margin-top:12px">
              <div style="font-size:.9rem;color:{SUB}">No dreams match your search or filter.</div>
            </div>""", unsafe_allow_html=True)

        for dream in filtered:
            pct     = get_progress(dream)
            ms_done = sum(1 for m in dream["milestones"] if m["done"])
            ms_total= len(dream["milestones"])
            cat     = get_category(dream["title"], dream.get("description",""))
            info    = CATEGORIES.get(cat, CATEGORIES["default"])
            icon    = "🏆" if pct==100 else "🚀" if pct>0 else "🌱"

            with st.expander(f"{icon} {dream['title']}  ·  {pct}% complete", expanded=False):
                # Image + description side by side
                ic, dc = st.columns([1,2])
                with ic:
                    st.markdown(f'<img src="{info["img"]}" style="width:100%;height:140px;object-fit:cover;border-radius:12px">', unsafe_allow_html=True)
                with dc:
                    st.markdown(f'<div style="color:{SUB};font-size:.85rem;line-height:1.6">{dream.get("description","")}</div>', unsafe_allow_html=True)
                    st.markdown(f'{pb(pct)}<div style="font-size:.72rem;color:{SUB};margin-top:4px">{ms_done} of {ms_total} milestones · Started {dream["created_at"][:10]}</div>', unsafe_allow_html=True)

                sec("MILESTONES")
                for ms in dream["milestones"]:
                    c1, c2 = st.columns([0.06, 0.94])
                    with c1:
                        checked = st.checkbox("", value=ms["done"], key=f"ms_{dream['id']}_{ms['id']}")
                        if checked != ms["done"]:
                            toggle_milestone(dream["id"], ms["id"])
                            st.rerun()
                    with c2:
                        style = f"text-decoration:line-through;opacity:.45;color:{SUB}" if ms["done"] else f"color:{TEXT}"
                        icon2 = "✅" if ms["done"] else "⭕"
                        st.markdown(f'<div style="padding:7px 0;font-size:.85rem;{style}">{icon2} {ms["text"]}</div>', unsafe_allow_html=True)

                st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
                with st.form(key=f"add_ms_{dream['id']}", clear_on_submit=True):
                    nm = st.text_input("", placeholder="Add a new milestone…", label_visibility="collapsed")
                    if st.form_submit_button("➕ Add Milestone") and nm.strip():
                        add_milestone(dream["id"], nm.strip())
                        st.rerun()

                # Two-step delete confirmation
                del_key = f"confirm_del_{dream['id']}"
                if st.session_state.get(del_key):
                    st.warning(f"Delete “{dream['title']}” permanently? This can't be undone.")
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        if st.button("✅ Yes, delete it", key=f"yes_{dream['id']}", use_container_width=True):
                            delete_dream(dream["id"])
                            st.session_state.pop(del_key, None)
                            st.rerun()
                    with cc2:
                        if st.button("Cancel", key=f"cancel_{dream['id']}", use_container_width=True):
                            st.session_state.pop(del_key, None)
                            st.rerun()
                else:
                    if st.button("🗑️ Delete dream", key=f"del_{dream['id']}"):
                        st.session_state[del_key] = True
                        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ADD DREAM
# ══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Add Dream":
    lc, rc = st.columns([1.2, 1])

    with lc:
        st.markdown(f"""
        <div style="margin-bottom:20px">
          <div style="font-size:1.7rem;font-weight:800;color:{TEXT};letter-spacing:-.02em">➕ Add a Dream</div>
          <div style="font-size:.88rem;color:{SUB};margin-top:4px">
            Describe your dream and we'll build your personalised roadmap</div>
        </div>""", unsafe_allow_html=True)

        # Title lives OUTSIDE the form so the category preview updates live as you type
        title = st.text_input("What's your dream? *",
            placeholder="e.g. Run a marathon, Launch a startup, Learn Spanish…",
            key="dream_title_input")

        with st.form("add_dream_form", clear_on_submit=True):
            description = st.text_area("Tell us more *",
                placeholder="Describe your dream in detail. What does success look like to you?",
                height=130)
            ms_mode = st.radio("Milestones",
                ["✨ Build my roadmap for me", "✏️ I'll write my own"],
                label_visibility="visible")
            custom = ""
            if ms_mode == "✏️ I'll write my own":
                custom = st.text_area("Your milestones (one per line)",
                    placeholder="Step 1: …\nStep 2: …\nStep 3: …", height=130)
            submitted = st.form_submit_button("🚀 Start My Journey", type="primary",
                                              use_container_width=True)

        if submitted:
            if not title.strip() or not description.strip():
                st.error("Please fill in both the title and description.")
            else:
                if ms_mode == "✨ Build my roadmap for me":
                    milestones = generate_specific_milestones(title.strip(), description.strip())
                else:
                    milestones = [m.strip() for m in custom.split("\n") if m.strip()]
                    if not milestones:
                        milestones = generate_specific_milestones(title.strip(), description.strip())
                dream = add_dream(title.strip(), description.strip(), milestones)
                st.success(f"✨ Dream added with {len(milestones)} personalised milestones!")
                st.balloons()
                st.session_state.dream_title_input = ""
                st.rerun()

    with rc:
        # Preview panel — now updates live as the title field changes
        cat  = get_category(title, "")
        info = CATEGORIES.get(cat, CATEGORIES["default"])
        st.markdown(f"""
        <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;overflow:hidden;margin-top:52px">
          <img src="{info["img"]}" style="width:100%;height:180px;object-fit:cover"
               onerror="this.style.display='none'">
          <div style="padding:20px">
            <div style="font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{info["color"]};margin-bottom:8px">
              {info["emoji"]} Dream Category Preview</div>
            <div style="font-size:.85rem;color:{SUB};line-height:1.6">
              Start typing your dream title on the left — we'll automatically detect your
              category and generate personalised milestones for you. 🎯</div>
            <div style="margin-top:16px;padding:14px;background:{CARD2};border-radius:10px;
                 border-left:3px solid {PURPLE}">
              <div style="font-size:.72rem;font-weight:600;color:{PURPLE};margin-bottom:6px">✨ HOW IT WORKS</div>
              <div style="font-size:.78rem;color:{SUB};line-height:1.7">
                1. Describe your dream in detail<br>
                2. We analyse your words<br>
                3. Get 5 specific, actionable milestones<br>
                4. Track your progress every day
              </div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Show recently added if any
        if dreams_all:
            st.markdown(f'<div style="margin-top:16px;font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{SUB}">RECENTLY ADDED</div>', unsafe_allow_html=True)
            for d in sorted(dreams_all, key=lambda x: x["created_at"], reverse=True)[:2]:
                pct = get_progress(d)
                st.markdown(f"""
                <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
                     padding:12px 14px;margin-top:8px">
                  <div style="font-size:.85rem;font-weight:600;color:{TEXT}">{d["title"]}</div>
                  {pb(pct)}
                  <div style="font-size:.68rem;color:{SUB};margin-top:4px">{pct}% complete</div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PROGRESS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Progress":
    st.markdown(f"""
    <div style="margin-bottom:20px">
      <div style="font-size:1.7rem;font-weight:800;color:{TEXT};letter-spacing:-.02em">📊 Your Progress</div>
      <div style="font-size:.88rem;color:{SUB};margin-top:4px">See how far you've come on every dream</div>
    </div>""", unsafe_allow_html=True)

    if not dreams_all:
        st.markdown(f"""
        <div style="text-align:center;padding:80px;background:{CARD};border:1px solid {BORDER};border-radius:18px">
          <div style="font-size:5rem">📊</div>
          <div style="font-size:1.1rem;font-weight:600;color:{TEXT};margin-top:16px">Nothing to track yet</div>
          <div style="font-size:.85rem;color:{SUB};margin-top:8px">Add your first dream to start tracking progress</div>
        </div>""", unsafe_allow_html=True)
    else:
        total_ms  = sum(len(d["milestones"]) for d in dreams_all)
        done_ms   = sum(sum(1 for m in d["milestones"] if m["done"]) for d in dreams_all)
        completed = sum(1 for d in dreams_all if d["milestones"] and all(m["done"] for m in d["milestones"]))
        in_prog   = sum(1 for d in dreams_all if any(m["done"] for m in d["milestones"]) and not all(m["done"] for m in d["milestones"]))

        sec("OVERALL STATS")
        c1,c2,c3,c4 = st.columns(4)
        scard(c1, str(len(dreams_all)), "Total Dreams", "purple")
        scard(c2, str(completed),       "Completed",    "green")
        scard(c3, str(in_prog),         "In Progress",  "teal")
        scard(c4, f"{int(done_ms/total_ms*100) if total_ms else 0}%", "Overall", "gold")

        sec("PROGRESS BY DREAM")
        df = pd.DataFrame([{
            "Dream": d["title"][:35]+("…" if len(d["title"])>35 else ""),
            "Progress %": get_progress(d),
            "Done": sum(1 for m in d["milestones"] if m["done"]),
            "Total": len(d["milestones"]),
        } for d in dreams_all])

        fig = px.bar(df, x="Progress %", y="Dream", orientation="h",
                     color="Progress %",
                     color_continuous_scale=[[0,"#1e1040"],[0.5,PURPLE],[1.0,PINK]],
                     text="Progress %")
        fig.update_traces(texttemplate="%{text}%", textposition="outside",
                          marker_line_width=0)
        fig.update_layout(
            plot_bgcolor=BG, paper_bgcolor=CARD,
            font=dict(family="Inter", color=SUB, size=11),
            margin=dict(l=8,r=50,t=8,b=8), height=max(260, len(dreams_all)*65),
            coloraxis_showscale=False,
            xaxis=dict(range=[0,115], gridcolor=BORDER, tickfont=dict(color=SUB)),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color=TEXT, size=12)),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Dream detail cards with images
        sec("DREAM DETAILS")
        for dream in dreams_all:
            pct     = get_progress(dream)
            ms_done = sum(1 for m in dream["milestones"] if m["done"])
            ms_total= len(dream["milestones"])
            cat     = get_category(dream["title"], dream.get("description",""))
            info    = CATEGORIES.get(cat, CATEGORIES["default"])
            color   = PINK if pct==100 else PURPLE if pct>50 else BLUE

            ic, dc = st.columns([1,3])
            with ic:
                st.markdown(f'<img src="{info["img"]}" style="width:100%;height:90px;object-fit:cover;border-radius:12px;border:1px solid {BORDER}">', unsafe_allow_html=True)
            with dc:
                st.markdown(f"""
                <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:14px 18px">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                    <div style="font-weight:700;color:{TEXT};font-size:.95rem">{dream["title"]}</div>
                    <div style="font-size:.85rem;color:{color};font-weight:700">{pct}%</div>
                  </div>
                  {pb(pct)}
                  <div style="font-size:.72rem;color:{SUB};margin-top:6px">
                    {ms_done} of {ms_total} milestones · Started {dream["created_at"][:10]}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(f'<div style="text-align:center;font-size:.72rem;color:{SUB}">✨ DreamzLab · Bring your dreams to reality · Built with 💜</div>', unsafe_allow_html=True)




