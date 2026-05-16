"""
Deciora - About Us Page
"""
import streamlit as st


def render_about():
    st.markdown("""
<style>
.about-value-card {
    background: rgba(13,21,53,0.5);
    border-left: 3px solid #4A9EF5;
    padding: 1.25rem 1.5rem;
    border-radius: 0 10px 10px 0;
    margin: 0.75rem 0;
}
.about-story-card {
    background: rgba(13,21,53,0.7);
    border: 1px solid rgba(74,158,245,0.12);
    border-radius: 14px;
    padding: 2rem;
    height: 100%;
}
</style>
""", unsafe_allow_html=True)

    # ── Back Button ───────────────────────────────────────────
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Home"):
            st.session_state.page = "landing"
            st.rerun()

    # ── Hero ─────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center;padding:3rem 2rem 2rem;">
    <div style="font-family:'Syne';font-size:0.72rem;font-weight:600;
                letter-spacing:0.2em;text-transform:uppercase;
                color:#4A9EF5;margin-bottom:0.75rem;">
        Our Story
    </div>
    <h1 style="font-family:'Syne';font-size:2.8rem;font-weight:800;
               color:#f0f4ff;margin-bottom:0.75rem;line-height:1.15;">
        Built for the Businesses<br>That Build the Economy
    </h1>
    <p style="font-family:'Inter';font-size:1rem;color:#8896b3;
              max-width:580px;margin:0 auto;line-height:1.8;">
        MSMEs are the backbone of every economy, yet they've always lacked
        access to the kind of intelligent analytics that large enterprises
        take for granted. Deciora changes that.
    </p>
</div>
""", unsafe_allow_html=True)

    # ── Mission & Vision ──────────────────────────────────────
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""
<div style="background:linear-gradient(135deg,
                rgba(37,99,176,0.15),rgba(109,40,217,0.1));
            border:1px solid rgba(74,158,245,0.2);
            border-radius:14px;padding:2rem;height:100%;">
    <div style="font-size:2rem;margin-bottom:1rem;">🎯</div>
    <div style="font-family:'Syne';font-size:1.15rem;font-weight:700;
                color:#f0f4ff;margin-bottom:0.75rem;">Our Mission</div>
    <p style="font-family:'Inter';color:#8896b3;line-height:1.8;font-size:0.9rem;">
        To democratize decision intelligence for every MSME — making
        world-class AI analytics accessible without needing a data science
        team, complex BI tools, or expensive consultants.
        <br><br>
        Every business owner deserves to make decisions backed by data,
        not just instinct.
    </p>
</div>
""", unsafe_allow_html=True)

    with m2:
        st.markdown("""
<div style="background:linear-gradient(135deg,
                rgba(109,40,217,0.1),rgba(37,99,176,0.15));
            border:1px solid rgba(167,139,250,0.2);
            border-radius:14px;padding:2rem;height:100%;">
    <div style="font-size:2rem;margin-bottom:1rem;">🔭</div>
    <div style="font-family:'Syne';font-size:1.15rem;font-weight:700;
                color:#f0f4ff;margin-bottom:0.75rem;">Our Vision</div>
    <p style="font-family:'Inter';color:#8896b3;line-height:1.8;font-size:0.9rem;">
        A world where every MSME — from a Mumbai textile trader to a
        Nairobi agribusiness — has the same analytical power as
        Fortune 500 companies.
        <br><br>
        Intelligence that doesn't just inform, but actively drives
        better decisions every single day.
    </p>
</div>
""", unsafe_allow_html=True)

    # ── Company Story ─────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
<div style="font-family:'Syne';font-size:1.5rem;font-weight:800;
            color:#f0f4ff;text-align:center;margin-bottom:1.5rem;">
    The Deciora Story
</div>
""", unsafe_allow_html=True)

    _, story_col, _ = st.columns([1, 4, 1])
    with story_col:
        st.markdown("""
<div class="about-value-card">
    <div style="font-family:'Syne';font-weight:700;color:#f0f4ff;
                margin-bottom:0.4rem;">The Problem We Saw</div>
    <div style="font-family:'Inter';font-size:0.875rem;
                color:#8896b3;line-height:1.8;">
        Small and mid-sized businesses generate enormous amounts of
        operational data — sales records, expense sheets, inventory logs —
        but lack the tools to extract meaningful insights from it.
        Traditional BI tools are expensive, complex, and built for
        enterprise scale.
    </div>
</div>

<div class="about-value-card" style="border-left-color:#a78bfa;">
    <div style="font-family:'Syne';font-weight:700;color:#f0f4ff;
                margin-bottom:0.4rem;">The Solution We Built</div>
    <div style="font-family:'Inter';font-size:0.875rem;
                color:#8896b3;line-height:1.8;">
        Deciora combines the simplicity of a chat interface with the
        depth of enterprise analytics. Upload your data, get instant
        AI insights across four dimensions of analysis, and have
        natural conversations with your business data — all powered
        by Agentic RAG that queries your real data before answering.
    </div>
</div>

<div class="about-value-card" style="border-left-color:#4ade80;">
    <div style="font-family:'Syne';font-weight:700;color:#f0f4ff;
                margin-bottom:0.4rem;">The Impact We're Creating</div>
    <div style="font-family:'Inter';font-size:0.875rem;
                color:#8896b3;line-height:1.8;">
        Businesses using Deciora report 40% faster decision cycles,
        25% reduction in operational inefficiencies, and the confidence
        that every major business decision is backed by real intelligence
        — not guesswork.
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Core Values ───────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
<div style="font-family:'Syne';font-size:1.5rem;font-weight:800;
            color:#f0f4ff;text-align:center;margin-bottom:1.5rem;">
    Our Core Values
</div>
""", unsafe_allow_html=True)

    v1, v2, v3 = st.columns(3)
    values = [
        ("⚡", "Radical Simplicity",
         "Intelligence should feel effortless. We hide complexity behind clarity so any founder can use it."),
        ("🔐", "Trust & Transparency",
         "Your data is yours. We never train on your business data, never share it, never monetize it."),
        ("🌍", "Democratization",
         "World-class analytics for every business — regardless of size, budget, or technical knowledge."),
    ]
    for col, (icon, title, desc) in zip([v1, v2, v3], values):
        with col:
            st.markdown(f"""
<div style="background:rgba(13,21,53,0.7);
            border:1px solid rgba(74,158,245,0.12);
            border-radius:12px;padding:2rem;
            text-align:center;height:100%;">
    <div style="font-size:2rem;margin-bottom:1rem;">{icon}</div>
    <div style="font-family:'Syne';font-weight:700;
                color:#f0f4ff;margin-bottom:0.6rem;">{title}</div>
    <div style="font-family:'Inter';font-size:0.85rem;
                color:#8896b3;line-height:1.7;">{desc}</div>
</div>""", unsafe_allow_html=True)

    # ── Stats ─────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
<div style="background:linear-gradient(135deg,
                rgba(37,99,176,0.08),rgba(109,40,217,0.06));
            border:1px solid rgba(74,158,245,0.12);
            border-radius:16px;padding:2.5rem 2rem;text-align:center;">
    <div style="font-family:'Syne';font-size:1.3rem;font-weight:700;
                color:#f0f4ff;margin-bottom:2rem;">
        Deciora by the Numbers
    </div>
""", unsafe_allow_html=True)

    n1, n2, n3, n4 = st.columns(4)
    for col, val, lbl in [
        (n1, "10K+",  "Analyses Run"),
        (n2, "98%",   "Data Accuracy"),
        (n3, "< 60s", "Insight Generation"),
        (n4, "4",     "Analysis Dimensions"),
    ]:
        with col:
            st.markdown(f"""
<div style="text-align:center;">
    <span style="font-family:'Syne';font-size:2rem;font-weight:800;
                 background:linear-gradient(135deg,#4A9EF5,#a78bfa);
                 -webkit-background-clip:text;
                 -webkit-text-fill-color:transparent;
                 display:block;">{val}</span>
    <div style="font-family:'Inter';font-size:0.82rem;
                color:#8896b3;margin-top:0.25rem;">{lbl}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
<div style="text-align:center;padding:3rem 2rem;">
    <h3 style="font-family:'Syne';font-size:2rem;font-weight:800;
               color:#f0f4ff;margin-bottom:1rem;">
        Ready to Try Deciora?
    </h3>
    <p style="font-family:'Inter';color:#8896b3;margin-bottom:2rem;">
        No credit card required. Start your first analysis in 60 seconds.
    </p>
</div>
""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("Start Free Analysis →", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()