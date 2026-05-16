"""
Deciora - Global Styles
Premium dark theme with electric blue + purple accents
"""
import streamlit as st

DECIORA_CSS = """
<style>
/* ── Fonts ──────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ─────────────────────────────────────── */
:root {
    --navy:       #050a1a;
    --navy-2:     #080f24;
    --navy-3:     #0d1535;
    --blue:       #4A9EF5;
    --blue-dim:   #2563b0;
    --purple:     #a78bfa;
    --purple-dim: #6d28d9;
    --white:      #f0f4ff;
    --white-dim:  #8896b3;
    --border:     rgba(74,158,245,0.15);
    --card:       rgba(13,21,53,0.7);
    --glow-blue:  0 0 30px rgba(74,158,245,0.3);
    --glow-purple:0 0 30px rgba(167,139,250,0.25);
}

/* ── Reset & Base ───────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stApp"] {
    background: var(--navy) !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Hide Streamlit Chrome ──────────────────────────────── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Main Content Area ──────────────────────────────────── */
[data-testid="stMain"] {
    background: var(--navy) !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Sidebar ────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--navy-2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}

/* ── Headings ───────────────────────────────────────────── */
h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    color: var(--white) !important;
}

/* ── Buttons ────────────────────────────────────────────── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    background: linear-gradient(135deg, #2563b0, #4A9EF5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8, #60aef9) !important;
    box-shadow: var(--glow-blue) !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs ─────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: rgba(8,15,36,0.8) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 2px rgba(74,158,245,0.2) !important;
}

/* ── File Uploader ──────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: rgba(13,21,53,0.5) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--blue) !important;
    background: rgba(74,158,245,0.05) !important;
}

/* ── Alerts ─────────────────────────────────────────────── */
.stAlert {
    background: rgba(13,21,53,0.8) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
}

/* ── Checkboxes & Radio ─────────────────────────────────── */
.stCheckbox > label,
.stRadio > label {
    color: var(--white-dim) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Tabs ───────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--navy-2) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    color: var(--white-dim) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
    padding: 0.75rem 1.25rem !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--blue) !important;
    border-bottom: 2px solid var(--blue) !important;
    background: transparent !important;
}

/* ── Progress Bar ───────────────────────────────────────── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--blue), var(--purple)) !important;
    border-radius: 4px !important;
}

/* ── Spinner ────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: var(--blue) !important;
}

/* ── Expander ───────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Dataframe ──────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* ── Selectbox ──────────────────────────────────────────── */
.stSelectbox > div > div {
    background: rgba(8,15,36,0.8) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
}

/* ── Custom Component Classes ───────────────────────────── */
.deciora-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 0.75rem 0;
    backdrop-filter: blur(10px);
}

.deciora-metric {
    background: linear-gradient(135deg,
        rgba(37,99,176,0.15),
        rgba(109,40,217,0.1));
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    text-align: center;
}

.deciora-metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--blue);
    display: block;
}

.deciora-metric-label {
    font-size: 0.78rem;
    color: var(--white-dim);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.25rem;
    display: block;
}

.badge-high {
    background: rgba(239,68,68,0.15);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.3);
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.badge-medium {
    background: rgba(251,191,36,0.15);
    color: #fbbf24;
    border: 1px solid rgba(251,191,36,0.3);
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.badge-low {
    background: rgba(74,158,245,0.15);
    color: var(--blue);
    border: 1px solid rgba(74,158,245,0.3);
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.chat-bubble-user {
    background: linear-gradient(135deg,
        rgba(37,99,176,0.3),
        rgba(74,158,245,0.2));
    border: 1px solid rgba(74,158,245,0.25);
    border-radius: 16px 16px 4px 16px;
    padding: 0.875rem 1.1rem;
    margin: 0.5rem 0;
    max-width: 80%;
    margin-left: auto;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: var(--white);
    line-height: 1.6;
}

.chat-bubble-ai {
    background: rgba(13,21,53,0.9);
    border: 1px solid var(--border);
    border-radius: 16px 16px 16px 4px;
    padding: 0.875rem 1.1rem;
    margin: 0.5rem 0;
    max-width: 85%;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: var(--white);
    line-height: 1.6;
}

.chat-ai-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--blue);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.4rem;
    display: block;
}

.sidebar-section-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--white-dim);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 0 1rem;
    margin: 1.2rem 0 0.4rem;
}

.analysis-tag {
    display: inline-block;
    background: rgba(74,158,245,0.12);
    color: var(--blue);
    border: 1px solid rgba(74,158,245,0.25);
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.15rem;
    font-family: 'Inter', sans-serif;
}

.gradient-text {
    background: linear-gradient(135deg, var(--blue), var(--purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

.exec-summary-box {
    background: linear-gradient(135deg,
        rgba(37,99,176,0.12),
        rgba(109,40,217,0.08));
    border: 1px solid rgba(74,158,245,0.2);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin: 1rem 0;
}

.exec-summary-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--blue);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.5rem;
    display: block;
}

.exec-summary-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: var(--white);
    line-height: 1.75;
}

.action-card {
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
    background: rgba(13,21,53,0.5);
    transition: border-color 0.2s;
}

.action-card:hover {
    border-color: rgba(74,158,245,0.3);
}

.action-title {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    color: var(--white);
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
}

.action-impact {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: var(--white-dim);
}

.data-health-bar {
    height: 6px;
    border-radius: 3px;
    background: rgba(74,158,245,0.1);
    margin-top: 0.5rem;
    overflow: hidden;
}

.data-health-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--blue), var(--purple));
    transition: width 0.5s ease;
}
</style>
"""


def inject_global_styles():
    st.markdown(DECIORA_CSS, unsafe_allow_html=True)