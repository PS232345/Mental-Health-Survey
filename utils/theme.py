"""
MindScope theme — a calm 'field notebook' aesthetic instead of a generic
corporate dashboard: warm paper background, muted sage + clay accents,
serif headings. Designed to feel appropriate for a mental-health topic —
quiet, non-clinical, human.
"""
import streamlit as st

PAPER = "#f6f1e9"
PAPER_CARD = "#fffdf8"
INK = "#2f3b30"
SAGE = "#6d8b74"
SAGE_DARK = "#4f6b56"
CLAY = "#c98a6b"
CLAY_DARK = "#a9694f"
MUTED = "#8a8578"
BORDER = "#e4dcc9"

PALETTE = [SAGE, CLAY, "#7f9c8f", "#d1a887", "#597a63", "#b9754f"]

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color: {INK};
}}

.stApp {{
    background-color: {PAPER};
    background-image: radial-gradient(circle at 1px 1px, rgba(47,59,48,0.035) 1px, transparent 0);
    background-size: 22px 22px;
}}

h1, h2, h3 {{
    font-family: 'Lora', serif !important;
    color: {INK} !important;
    letter-spacing: -0.01em;
}}

h1 {{
    font-weight: 600 !important;
    border-bottom: 2px solid {BORDER};
    padding-bottom: 0.4rem;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: {SAGE_DARK};
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] * {{
    color: #f6f1e9 !important;
}}
section[data-testid="stSidebar"] .stRadio label, section[data-testid="stSidebar"] a {{
    font-family: 'Inter', sans-serif;
}}

/* Metric cards */
div[data-testid="stMetric"] {{
    background-color: {PAPER_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 14px 16px 8px 16px;
    box-shadow: 0 1px 3px rgba(47,59,48,0.06);
}}
div[data-testid="stMetricValue"] {{
    color: {SAGE_DARK} !important;
    font-family: 'Lora', serif !important;
}}

/* Cards / containers via markdown */
.mindscope-card {{
    background-color: {PAPER_CARD};
    border: 1px solid {BORDER};
    border-left: 4px solid {SAGE};
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 14px;
    box-shadow: 0 1px 3px rgba(47,59,48,0.06);
}}
.mindscope-card.clay {{ border-left-color: {CLAY}; }}

.mindscope-quote {{
    font-family: 'Lora', serif;
    font-style: italic;
    color: {MUTED};
    border-left: 3px solid {BORDER};
    padding-left: 14px;
    margin: 10px 0;
}}

.mindscope-badge {{
    display: inline-block;
    background: {SAGE};
    color: #fff;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 6px;
}}
.mindscope-badge.clay {{ background: {CLAY}; }}

/* Buttons */
.stButton>button {{
    background-color: {SAGE};
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    padding: 0.5em 1.2em;
}}
.stButton>button:hover {{
    background-color: {SAGE_DARK};
    color: white;
}}

/* Tabs */
.stTabs [data-baseweb="tab"] {{
    font-family: 'Inter', sans-serif;
    font-weight: 600;
}}

/* Dataframe */
div[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 8px;
}}

footer {{visibility: hidden;}}
#MainMenu {{visibility: hidden;}}
</style>
"""

def inject():
    st.markdown(CSS, unsafe_allow_html=True)

def card(html, clay=False):
    cls = "mindscope-card clay" if clay else "mindscope-card"
    st.markdown(f'<div class="{cls}">{html}</div>', unsafe_allow_html=True)

def badge(text, clay=False):
    cls = "mindscope-badge clay" if clay else "mindscope-badge"
    return f'<span class="{cls}">{text}</span>'
