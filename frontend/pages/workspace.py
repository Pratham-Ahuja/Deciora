"""
Deciora - Main Workspace Page
Intelligent analysis workspace with Agentic RAG chat
"""
import json
import streamlit as st
import plotly.graph_objects as go

from backend.auth import sign_out, get_user_profile
from backend.data_processor import (
    load_dataframe, clean_dataframe, classify_data
)
from backend.ai_engine import (
    generate_insights, generate_charts,
    chat_with_data, generate_session_title
)
from backend.session_manager import (
    create_session, get_user_sessions, update_session,
    save_insights, get_insights, save_message,
    get_chat_history
)

ANALYSIS_LABELS = {
    "descriptive":  "📊 Descriptive",
    "diagnostic":   "🔍 Diagnostic",
    "predictive":   "📈 Predictive",
    "prescriptive": "🎯 Prescriptive",
}


# ── Entry Point ────────────────────────────────────────────

def render_workspace():
    user = st.session_state.get("user")
    if not user:
        st.session_state.page = "landing"
        st.rerun()
        return

    user_id = user.id
    _init_state()

    with st.sidebar:
        render_sidebar(user_id, user)

    render_main(user_id)


# ── State Init ─────────────────────────────────────────────

def _init_state():
    defaults = {
        "current_session_id": None,
        "workspace_df": None,
        "workspace_classification": None,
        "workspace_insights": None,
        "workspace_charts": None,
        "chat_history": [],
        "analysis_done": False,
        "uploaded_file_name": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── Sidebar ────────────────────────────────────────────────

def render_sidebar(user_id: str, user):
    st.markdown("""
<style>
.sb-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: #e8f0ff;
    padding: 1.25rem 1rem 1rem;
    border-bottom: 1px solid rgba(74,158,245,0.1);
    letter-spacing: 0.04em;
}
.sb-logo span {
    background: linear-gradient(135deg, #4A9EF5, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sb-section {
    font-size: 0.65rem;
    font-weight: 600;
    color: #4a5880;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 1rem 1rem 0.3rem;
}
.sb-user-box {
    border-top: 1px solid rgba(74,158,245,0.1);
    padding: 0.875rem 1rem;
    margin-top: auto;
}
.sb-user-name {
    font-size: 0.8rem;
    font-weight: 500;
    color: #c8d8f0;
}
.sb-user-email {
    font-size: 0.7rem;
    color: #4a5880;
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

    # Logo
    st.markdown('<div class="sb-logo">🔷 <span>DECIORA</span></div>',
                unsafe_allow_html=True)

    # New Analysis
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ New Analysis", use_container_width=True):
        _clear_workspace()
        st.rerun()

    # Sessions
    st.markdown('<div class="sb-section">Recent Sessions</div>',
                unsafe_allow_html=True)

    sessions = get_user_sessions(user_id)
    if not sessions:
        st.markdown(
            '<div style="padding:0.5rem 1rem;color:#4a5880;font-size:0.78rem;">'
            'No sessions yet.</div>',
            unsafe_allow_html=True
        )
    else:
        for sess in sessions[:15]:
            is_active = st.session_state.current_session_id == sess["session_id"]
            label = f"{'▶ ' if is_active else ''}{sess['analysis_name'][:28]}"
            if st.button(label, key=f"sess_{sess['session_id']}",
                         use_container_width=True):
                _load_session(sess["session_id"])
                st.rerun()

    # Spacer
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Feedback button
    if st.button("📬 Feedback", use_container_width=True):
        st.session_state.page = "feedback"
        st.rerun()

    # User profile
    profile = get_user_profile(user_id)
    email   = getattr(user, "email", profile.get("email", ""))
    company = profile.get("company_name", "My Account")

    st.markdown(f"""
<div class="sb-user-box">
    <div class="sb-user-name">{company}</div>
    <div class="sb-user-email">{email}</div>
</div>
""", unsafe_allow_html=True)

    if st.button("Logout →", use_container_width=True):
        sign_out()
        st.rerun()


# ── Helpers ────────────────────────────────────────────────

def _clear_workspace():
    keys = [
        "current_session_id", "workspace_df",
        "workspace_classification", "workspace_insights",
        "workspace_charts", "chat_history",
        "analysis_done", "uploaded_file_name",
    ]
    for k in keys:
        st.session_state[k] = None if k != "chat_history" else []
    st.session_state.analysis_done = False


def _load_session(session_id: str):
    st.session_state.current_session_id = session_id

    insight_data = get_insights(session_id)
    if insight_data:
        st.session_state.workspace_insights = insight_data.get("insights")
        st.session_state.workspace_charts   = insight_data.get("charts")
        st.session_state.analysis_done      = True
    else:
        st.session_state.workspace_insights = None
        st.session_state.workspace_charts   = None
        st.session_state.analysis_done      = False

    st.session_state.chat_history      = get_chat_history(session_id)
    st.session_state.workspace_df      = None
    st.session_state.workspace_classification = None


# ── Main Area ──────────────────────────────────────────────

def render_main(user_id: str):
    st.markdown("""
<div style="padding:1.75rem 2.5rem 1rem;
            border-bottom:1px solid rgba(74,158,245,0.1);">
    <h1 style="font-family:'Syne';font-size:1.5rem;
               font-weight:800;color:#f0f4ff;margin:0;">
        Analysis Workspace
    </h1>
    <p style="font-family:'Inter';color:#8896b3;
              font-size:0.85rem;margin:0.25rem 0 0;">
        Upload → Process → Analyse → Chat with your data
    </p>
</div>
""", unsafe_allow_html=True)

    if st.session_state.analysis_done and st.session_state.workspace_insights:
        render_insights_section()
        render_chat_section(user_id)
        st.markdown("---")
        st.markdown(
            '<p style="font-family:Syne;font-size:0.9rem;'
            'color:#8896b3;">🔄 Run new analysis on this session</p>',
            unsafe_allow_html=True
        )
        render_upload_section(user_id)
    else:
        render_upload_section(user_id)
        if st.session_state.workspace_df is not None:
            render_analysis_selection(user_id)
        if st.session_state.analysis_done and st.session_state.workspace_insights:
            render_insights_section()
            render_chat_section(user_id)


# ── Upload Section ─────────────────────────────────────────

def render_upload_section(user_id: str):
    st.markdown("""
<div style="padding:0 2.5rem;">
<h3 style="font-family:'Syne';font-size:1rem;font-weight:700;
           color:#f0f4ff;margin:1.5rem 0 0.4rem;">
    📁 Step 1 — Upload Your Data
</h3>
<p style="font-family:'Inter';font-size:0.82rem;color:#8896b3;margin-bottom:1rem;">
    CSV or Excel (.xlsx, .xls) · Max 50MB · Any column names or format
</p>
</div>
""", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop your file here",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed",
    )

    if uploaded is not None:
        # Skip reprocessing same file
        if uploaded.name == st.session_state.get("uploaded_file_name"):
            return

        file_bytes = uploaded.read()

        if len(file_bytes) / (1024 * 1024) > 50:
            st.error("File exceeds 50MB limit.")
            return

        with st.spinner("🔄 Processing your data..."):
            try:
                df             = load_dataframe(file_bytes, uploaded.name)
                df             = clean_dataframe(df)
                classification = classify_data(df)

                st.session_state.workspace_df             = df
                st.session_state.workspace_classification = classification
                st.session_state.uploaded_file_name       = uploaded.name

                cl = classification
                st.markdown(f"""
<div style="background:rgba(13,21,53,0.7);
            border:1px solid rgba(74,158,245,0.15);
            border-radius:12px;padding:1.25rem 1.5rem;margin-top:1rem;">
    <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1rem;">
        <span style="font-size:1.2rem;">✅</span>
        <div>
            <div style="font-family:'Syne';font-weight:700;
                        color:#f0f4ff;">{uploaded.name}</div>
            <div style="font-family:'Inter';font-size:0.75rem;
                        color:#4A9EF5;">{cl['data_type']}</div>
        </div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;">
        <div class="deciora-metric">
            <span class="deciora-metric-value">{cl['total_rows']:,}</span>
            <span class="deciora-metric-label">Rows</span>
        </div>
        <div class="deciora-metric">
            <span class="deciora-metric-value">{cl['total_columns']}</span>
            <span class="deciora-metric-label">Columns</span>
        </div>
        <div class="deciora-metric">
            <span class="deciora-metric-value">{len(cl['numeric_columns'])}</span>
            <span class="deciora-metric-label">Numeric</span>
        </div>
        <div class="deciora-metric">
            <span class="deciora-metric-value">{cl['missing_pct']}%</span>
            <span class="deciora-metric-label">Missing</span>
        </div>
    </div>
    <div style="margin-top:1rem;">
        <div style="font-family:'Inter';font-size:0.7rem;
                    color:#8896b3;margin-bottom:0.4rem;">
            DETECTED COLUMNS
        </div>
        <div>
            {"".join([f'<span class="analysis-tag">{c}</span>'
                      for c in cl["columns"][:15]])}
        </div>
    </div>
    {"" if not cl.get("column_intents") else f'''
    <div style="margin-top:0.75rem;">
        <div style="font-family:Inter;font-size:0.7rem;
                    color:#8896b3;margin-bottom:0.4rem;">
            COLUMN MAPPING
        </div>
        <div>
            {"".join([
                f'<span style="font-family:Inter;font-size:0.75rem;'
                f'color:#a78bfa;margin-right:0.75rem;">'
                f'{intent.upper()} → {col}</span>'
                for intent, col in cl["column_intents"].items()
                if intent != "id"
            ])}
        </div>
    </div>'''}
</div>
""", unsafe_allow_html=True)

                with st.expander("👁 Preview Data"):
                    st.dataframe(df.head(10), use_container_width=True)

            except Exception as e:
                st.error(f"❌ Could not process file: {str(e)}")
                st.session_state.workspace_df = None


# ── Analysis Selection ─────────────────────────────────────

def render_analysis_selection(user_id: str):
    st.markdown("""
<div style="padding:0 2.5rem;">
<h3 style="font-family:'Syne';font-size:1rem;font-weight:700;
           color:#f0f4ff;margin:2rem 0 0.4rem;">
    🧠 Step 2 — Select Analysis Type(s)
</h3>
<p style="font-family:'Inter';font-size:0.82rem;
          color:#8896b3;margin-bottom:1rem;">
    Select one or more. AI will run each on your data.
</p>
</div>
""", unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns(4)
    checks = {}
    with col_a:
        checks["descriptive"]  = st.checkbox("📊 Descriptive\nWhat happened?",  value=True)
    with col_b:
        checks["diagnostic"]   = st.checkbox("🔍 Diagnostic\nWhy it happened?")
    with col_c:
        checks["predictive"]   = st.checkbox("📈 Predictive\nWhat may happen?")
    with col_d:
        checks["prescriptive"] = st.checkbox("🎯 Prescriptive\nWhat to do?")

    selected = [k for k, v in checks.items() if v]

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn, _ = st.columns([2, 4])
    with col_btn:
        if st.button(
            "⚡ Generate Insights",
            use_container_width=True,
            disabled=not selected
        ):
            if selected:
                _run_analysis(user_id, selected)


# ── Run Analysis ───────────────────────────────────────────

def _run_analysis(user_id: str, analysis_types: list):
    df             = st.session_state.workspace_df
    classification = st.session_state.workspace_classification

    progress = st.progress(0, text="🤖 Initializing AI engine...")

    try:
        # Create session
        if not st.session_state.current_session_id:
            sess = create_session(user_id, "New Analysis", analysis_types)
            if not sess["success"]:
                st.error("Could not create session.")
                return
            session_id = sess["session"]["session_id"]
            st.session_state.current_session_id = session_id
        else:
            session_id = st.session_state.current_session_id

        progress.progress(20, text="📊 Generating insights with GPT-4o...")
        insights = generate_insights(df, classification, analysis_types)

        progress.progress(55, text="📈 Building charts...")
        charts = generate_charts(df, classification)

        progress.progress(75, text="💾 Saving to workspace...")

        # Extract recommendations
        recommendations = []
        if "prescriptive" in insights.get("analyses", {}):
            actions = insights["analyses"]["prescriptive"].get("top_actions", [])
            recommendations = [a.get("action", "") for a in actions]

        save_insights(session_id, insights, charts, recommendations)

        # Update session name
        title = insights.get(
            "session_title",
            generate_session_title(df, classification, analysis_types)
        )
        update_session(
            session_id,
            analysis_name=title,
            analysis_type=analysis_types,
            status="completed"
        )

        progress.progress(100, text="✅ Done!")

        st.session_state.workspace_insights = insights
        st.session_state.workspace_charts   = charts
        st.session_state.analysis_done      = True

        progress.empty()
        st.rerun()

    except Exception as e:
        progress.empty()
        st.error(f"❌ Analysis failed: {str(e)}")
        st.info("Check your OpenAI API key and Supabase connection.")


# ── Insights Section ───────────────────────────────────────

def render_insights_section():
    insights = st.session_state.workspace_insights
    charts   = st.session_state.workspace_charts or []

    if not insights:
        return

    st.markdown("""
<div style="padding:0 2.5rem;">
<h3 style="font-family:'Syne';font-size:1.2rem;font-weight:800;
           color:#f0f4ff;margin:2rem 0 0.5rem;">
    ✨ AI-Generated Insights
</h3>
""", unsafe_allow_html=True)

    # Executive Summary
    if exec_sum := insights.get("executive_summary"):
        st.markdown(f"""
<div class="exec-summary-box">
    <span class="exec-summary-label">Executive Summary</span>
    <div class="exec-summary-text">{exec_sum}</div>
</div>
""", unsafe_allow_html=True)

    # Data Health Score
    if health := insights.get("data_health"):
        score = health.get("score", 0)
        color = (
            "#4ade80" if score >= 70 else
            "#fbbf24" if score >= 40 else
            "#f87171"
        )
        st.markdown(f"""
<div style="display:flex;align-items:center;gap:1rem;
            padding:0.875rem 1.25rem;
            background:rgba(13,21,53,0.7);
            border:1px solid rgba(74,158,245,0.1);
            border-radius:10px;margin:0.75rem 0;">
    <div style="font-family:'Syne';font-size:2rem;
                font-weight:800;color:{color};">{score}</div>
    <div>
        <div style="font-family:'Syne';font-weight:700;
                    color:#f0f4ff;font-size:0.875rem;">
            Data Health Score
        </div>
        <div style="font-family:'Inter';font-size:0.75rem;color:#8896b3;">
            {" · ".join(health.get("strengths", [])[:2])}
        </div>
    </div>
    <div style="margin-left:auto;">
        <div class="data-health-bar" style="width:120px;">
            <div class="data-health-fill" style="width:{score}%;"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # Analysis Tabs
    analyses  = insights.get("analyses", {})
    tab_keys  = [k for k in ["descriptive","diagnostic","predictive","prescriptive"]
                 if k in analyses]
    tab_labels = [ANALYSIS_LABELS[k] for k in tab_keys]

    if tab_labels:
        tabs = st.tabs(tab_labels)
        for tab, key in zip(tabs, tab_keys):
            with tab:
                _render_analysis_tab(key, analyses[key])

    # Charts
    if charts:
        st.markdown("""
<div style="margin:1.5rem 0 0.75rem;">
    <div style="font-family:'Syne';font-size:1rem;
                font-weight:700;color:#f0f4ff;">
        📈 Data Visualizations
    </div>
</div>
""", unsafe_allow_html=True)
        chart_cols = st.columns(2)
        for i, chart in enumerate(charts[:4]):
            with chart_cols[i % 2]:
                try:
                    fig = go.Figure(json.loads(chart["figure"]))
                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                        config={"displayModeBar": False}
                    )
                except Exception:
                    pass

    st.markdown("</div>", unsafe_allow_html=True)


def _render_analysis_tab(key: str, data: dict):
    """Render individual analysis tab content."""
    if key == "descriptive":
        if summary := data.get("summary"):
            st.markdown(
                f'<p style="font-family:Inter;color:#c4d0e8;'
                f'line-height:1.75;margin-bottom:1rem;">{summary}</p>',
                unsafe_allow_html=True
            )
        metrics = data.get("key_metrics", [])
        if metrics:
            cols = st.columns(min(len(metrics), 4))
            for col, m in zip(cols, metrics):
                with col:
                    trend_icon  = "↑" if m.get("trend") == "up" else \
                                  "↓" if m.get("trend") == "down" else "→"
                    trend_color = "#4ade80" if m.get("trend") == "up" else \
                                  "#f87171" if m.get("trend") == "down" else "#fbbf24"
                    st.markdown(f"""
<div class="deciora-metric">
    <span class="deciora-metric-value">{m['value']}</span>
    <span class="deciora-metric-label">
        {m['label']}
        <span style="color:{trend_color}"> {trend_icon}</span>
    </span>
</div>""", unsafe_allow_html=True)

        for p in data.get("patterns", []):
            st.markdown(
                f'<div style="padding:0.4rem 0;font-family:Inter;'
                f'font-size:0.875rem;color:#8896b3;">'
                f'<span style="color:#4A9EF5;margin-right:0.5rem;">→</span>{p}</div>',
                unsafe_allow_html=True
            )

    elif key == "diagnostic":
        if causes := data.get("root_causes"):
            st.markdown("**Root Causes**")
            for c in causes:
                st.markdown(
                    f'<div style="padding:0.4rem 0;font-family:Inter;'
                    f'font-size:0.875rem;color:#c4d0e8;">'
                    f'<span style="color:#f87171;margin-right:0.5rem;">⚠</span>{c}</div>',
                    unsafe_allow_html=True
                )
        if anomalies := data.get("anomalies"):
            st.markdown("**Anomalies**")
            for a in anomalies:
                st.markdown(
                    f'<div style="padding:0.4rem 0;font-family:Inter;'
                    f'font-size:0.875rem;color:#c4d0e8;">'
                    f'<span style="color:#fbbf24;margin-right:0.5rem;">◆</span>{a}</div>',
                    unsafe_allow_html=True
                )
        if corr := data.get("correlations"):
            st.markdown("**Correlations**")
            for c in corr:
                st.markdown(
                    f'<div style="padding:0.4rem 0;font-family:Inter;'
                    f'font-size:0.875rem;color:#c4d0e8;">'
                    f'<span style="color:#4A9EF5;margin-right:0.5rem;">⟷</span>{c}</div>',
                    unsafe_allow_html=True
                )

    elif key == "predictive":
        if forecast := data.get("forecast_summary"):
            st.markdown(
                f'<p style="font-family:Inter;color:#c4d0e8;'
                f'line-height:1.75;margin-bottom:1rem;">{forecast}</p>',
                unsafe_allow_html=True
            )
        for pred in data.get("predictions", []):
            dir_icon  = "↑" if pred.get("direction") == "up" else "↓"
            dir_color = "#4ade80" if pred.get("direction") == "up" else "#f87171"
            st.markdown(f"""
<div class="action-card">
    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">
        <span style="font-size:1rem;color:{dir_color};">{dir_icon}</span>
        <div class="action-title">{pred.get('metric','')}</div>
        <span style="font-size:0.75rem;color:#8896b3;margin-left:auto;">
            Confidence: {pred.get('confidence','')}
        </span>
    </div>
    <div class="action-impact">{pred.get('reasoning','')}</div>
</div>""", unsafe_allow_html=True)

        if risks := data.get("risks", []):
            st.markdown("**⚠ Risks**")
            for r in risks:
                st.markdown(
                    f'<div style="padding:0.3rem 0;font-family:Inter;'
                    f'font-size:0.875rem;color:#fbbf24;">'
                    f'<span style="margin-right:0.5rem;">▸</span>{r}</div>',
                    unsafe_allow_html=True
                )

    elif key == "prescriptive":
        for action in data.get("top_actions", []):
            priority     = action.get("priority", "MEDIUM")
            badge_class  = (
                "badge-high"   if priority == "HIGH"   else
                "badge-medium" if priority == "MEDIUM" else
                "badge-low"
            )
            st.markdown(f"""
<div class="action-card">
    <div style="display:flex;align-items:center;
                gap:0.75rem;margin-bottom:0.4rem;">
        <span class="{badge_class}">{priority}</span>
        <div class="action-title">{action.get('action','')}</div>
    </div>
    <div class="action-impact">
        Expected Impact: {action.get('expected_impact','')}
    </div>
</div>""", unsafe_allow_html=True)

        if quick_wins := data.get("quick_wins", []):
            st.markdown("**⚡ Quick Wins**")
            for qw in quick_wins:
                st.markdown(
                    f'<div style="padding:0.3rem 0;font-family:Inter;'
                    f'font-size:0.875rem;color:#4ade80;">'
                    f'<span style="margin-right:0.5rem;">✓</span>{qw}</div>',
                    unsafe_allow_html=True
                )


# ── Chat Section ───────────────────────────────────────────

def render_chat_section(user_id: str):
    session_id     = st.session_state.current_session_id
    df             = st.session_state.workspace_df
    classification = st.session_state.workspace_classification
    insights       = st.session_state.workspace_insights

    st.markdown("""
<div style="padding:0 2.5rem;margin-top:2rem;">
<div style="border-top:1px solid rgba(74,158,245,0.1);padding-top:1.75rem;">
<h3 style="font-family:'Syne';font-size:1rem;font-weight:700;
           color:#f0f4ff;margin-bottom:0.25rem;">
    💬 Chat With Your Data
</h3>
<p style="font-family:'Inter';font-size:0.8rem;color:#8896b3;margin-bottom:1rem;">
    Agentic RAG — AI queries your actual data before answering
</p>
""", unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-bubble-user">{msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-bubble-ai">'
                f'<span class="chat-ai-label">Deciora AI</span>'
                f'{msg["content"]}</div>',
                unsafe_allow_html=True
            )

    # Suggested questions
    if not st.session_state.chat_history:
        st.markdown(
            '<div style="font-family:Inter;font-size:0.72rem;'
            'color:#8896b3;margin-bottom:0.5rem;">SUGGESTED QUESTIONS</div>',
            unsafe_allow_html=True
        )
        suggestions = [
            "What are the top revenue drivers?",
            "Where are the biggest cost inefficiencies?",
            "What does next quarter look like?",
            "What should I prioritize right now?",
        ]
        s1, s2 = st.columns(2)
        for i, s in enumerate(suggestions):
            with s1 if i % 2 == 0 else s2:
                if st.button(s, key=f"sugg_{i}"):
                    _process_chat(s, session_id, df, classification, insights)
                    st.rerun()

    # Chat input
    col_inp, col_send = st.columns([5, 1])
    with col_inp:
        user_msg = st.text_input(
            "Ask anything...",
            placeholder="Why are profits falling? / What will revenue look like next month?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with col_send:
        if st.button("Send →", use_container_width=True):
            if user_msg and user_msg.strip():
                _process_chat(
                    user_msg.strip(),
                    session_id, df, classification, insights
                )
                st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)


def _process_chat(
    message: str,
    session_id: str,
    df,
    classification: dict,
    insights: dict,
):
    """Process chat message through Agentic RAG."""
    if not message:
        return

    # Add user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": message,
    })
    if session_id:
        save_message(session_id, "user", message)

    # Generate AI response
    if df is None:
        ai_response = (
            "I don't have access to your data in this session. "
            "Please re-upload your file to continue analysis, "
            "or I can answer from the previously generated insights."
        )
    else:
        with st.spinner("🤖 Analyzing your data..."):
            ai_response = chat_with_data(
                message, df, classification, insights,
                st.session_state.chat_history[:-1]
            )

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": ai_response,
    })
    if session_id:
        save_message(session_id, "assistant", ai_response)