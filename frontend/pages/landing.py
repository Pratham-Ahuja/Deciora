"""
Deciora - Premium Landing Page
"""
import streamlit as st


def render_landing():
    st.markdown("""
<style>
.nav-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 3rem;
    border-bottom: 1px solid rgba(74,158,245,0.1);
    background: rgba(5,10,26,0.95);
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
}
.nav-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #f0f4ff;
    letter-spacing: 0.05em;
}
.nav-logo span {
    background: linear-gradient(135deg, #4A9EF5, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4A9EF5;
    margin-bottom: 1.5rem;
}
.hero-eyebrow::before,
.hero-eyebrow::after {
    content: '──';
    color: rgba(74,158,245,0.4);
    margin: 0 0.75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(3rem, 7vw, 6rem) !important;
    font-weight: 800 !important;
    line-height: 1.05 !important;
    color: #f0f4ff !important;
    margin: 0 0 0.5rem !important;
    letter-spacing: -0.02em;
}
.hero-tagline {
    font-family: 'Syne', sans-serif;
    font-size: clamp(1rem, 2.5vw, 1.35rem);
    color: rgba(167,139,250,0.9);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.hero-description {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    color: #8896b3;
    max-width: 560px;
    margin: 0 auto 3rem;
    line-height: 1.7;
}
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4A9EF5, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: block;
}
.stat-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #8896b3;
    margin-top: 0.25rem;
}
.feature-card {
    background: rgba(13,21,53,0.7);
    border: 1px solid rgba(74,158,245,0.12);
    border-radius: 14px;
    padding: 2rem;
    transition: all 0.3s ease;
    text-align: left;
    height: 100%;
}
.feature-card:hover {
    border-color: rgba(74,158,245,0.35);
    background: rgba(13,21,53,0.9);
    transform: translateY(-4px);
}
.feature-icon { font-size: 1.8rem; margin-bottom: 1rem; display: block; }
.feature-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #f0f4ff;
    margin-bottom: 0.4rem;
}
.feature-question {
    color: #4A9EF5;
    font-size: 0.78rem;
    font-family: 'Inter', sans-serif;
    margin-bottom: 0.5rem;
}
.feature-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
    color: #8896b3;
    line-height: 1.6;
}
.how-step {
    display: flex;
    align-items: flex-start;
    gap: 1.5rem;
    padding: 1.25rem;
    background: rgba(13,21,53,0.5);
    border: 1px solid rgba(74,158,245,0.1);
    border-radius: 12px;
    margin: 0.6rem 0;
}
.step-num {
    background: linear-gradient(135deg, #2563b0, #4A9EF5);
    color: white;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    flex-shrink: 0;
    line-height: 32px;
    text-align: center;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    color: #f0f4ff;
    margin-bottom: 0.25rem;
    font-size: 0.95rem;
}
.step-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #8896b3;
    line-height: 1.6;
}
.pricing-card {
    background: rgba(13,21,53,0.7);
    border: 1px solid rgba(74,158,245,0.15);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
}
.pricing-card.featured {
    border-color: #4A9EF5;
    background: linear-gradient(135deg,
        rgba(37,99,176,0.15),
        rgba(109,40,217,0.1));
    box-shadow: 0 0 40px rgba(74,158,245,0.15);
}
.pricing-plan {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #f0f4ff;
    margin-bottom: 0.5rem;
}
.pricing-price {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4A9EF5, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.5rem;
    display: block;
}
.pricing-feature {
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
    color: #8896b3;
    padding: 0.3rem 0;
    text-align: left;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #f0f4ff;
    text-align: center;
    margin-bottom: 0.5rem;
}
.section-sub {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    color: #8896b3;
    text-align: center;
    margin-bottom: 2.5rem;
}
.footer-bar {
    border-top: 1px solid rgba(74,158,245,0.1);
    padding: 2rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 4rem;
}
</style>
""", unsafe_allow_html=True)

    # ── NAV BAR ──────────────────────────────────────────────
    st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">🔷 <span>DECIORA</span></div>
    <div style="display:flex;gap:2rem;align-items:center;">
        <span style="font-family:Inter;font-size:0.875rem;color:#8896b3;">Features</span>
        <span style="font-family:Inter;font-size:0.875rem;color:#8896b3;">How It Works</span>
        <span style="font-family:Inter;font-size:0.875rem;color:#8896b3;">Pricing</span>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── HERO ─────────────────────────────────────────────────
    st.markdown("""
<div style="min-height:88vh;display:flex;flex-direction:column;
            align-items:center;justify-content:center;
            text-align:center;padding:5rem 2rem;">
    <div class="hero-eyebrow">AI-Powered Decision Intelligence for MSMEs</div>
    <h1 class="hero-title">
        Your Business Data,<br>
        <span style="background:linear-gradient(135deg,#4A9EF5,#a78bfa);
                     -webkit-background-clip:text;
                     -webkit-text-fill-color:transparent;">
            Decoded.
        </span>
    </h1>
    <div class="hero-tagline">Intelligence That Drives Decisions</div>
    <p class="hero-description">
        Upload your sales, inventory, or financial data and receive
        instant AI-powered insights — descriptive, diagnostic, predictive,
        and prescriptive — all in one intelligent workspace.
    </p>
</div>
""", unsafe_allow_html=True)

    # ── CTA BUTTONS ──────────────────────────────────────────
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("🚀 Start Free Analysis", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns([2, 1, 1, 2])
    with col_b:
        if st.button("About Us", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
    with col_c:
        if st.button("Feedback", use_container_width=True):
            st.session_state.page = "feedback"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── STATS ────────────────────────────────────────────────
    st.markdown('<p class="section-title">Trusted by Growing Businesses</p>',
                unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    for col, val, lbl in [
        (s1, "10K+", "Analyses Run"),
        (s2, "98%",  "Accuracy Rate"),
        (s3, "< 60s","Insight Time"),
        (s4, "4",    "Analysis Types"),
    ]:
        with col:
            st.markdown(f"""
<div style="text-align:center;padding:1rem;">
    <span class="stat-value">{val}</span>
    <div class="stat-label">{lbl}</div>
</div>""", unsafe_allow_html=True)

    # ── FEATURES ─────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Four Lenses of Intelligence</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="section-sub">From "what happened" to "what to do" — all in one workspace</p>',
                unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("📊", "Descriptive",  "What happened?",
         "Instantly understand your data — key metrics, trends, patterns, and distributions visualized."),
        ("🔍", "Diagnostic",   "Why did it happen?",
         "Identify root causes, detect anomalies, and uncover hidden correlations in your data."),
        ("📈", "Predictive",   "What may happen?",
         "AI-powered forecasts and scenario modeling to prepare your business for what comes next."),
        ("🎯", "Prescriptive", "What should you do?",
         "Prioritized action plans and recommendations tailored to your specific business context."),
    ]
    for col, (icon, title, q, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
<div class="feature-card">
    <span class="feature-icon">{icon}</span>
    <div class="feature-title">{title}</div>
    <div class="feature-question">{q}</div>
    <div class="feature-desc">{desc}</div>
</div>""", unsafe_allow_html=True)

    # ── HOW IT WORKS ─────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">How Deciora Works</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="section-sub">From raw data to strategic decisions in minutes</p>',
                unsafe_allow_html=True)

    h1, h2 = st.columns(2)
    steps = [
        ("1", "Upload Your Data",
         "Drag and drop CSV or Excel. Sales, inventory, expense, payroll — any format."),
        ("2", "AI Processes It",
         "Deciora auto-detects columns, cleans data, and classifies your dataset type."),
        ("3", "Select Analysis Types",
         "Choose Descriptive, Diagnostic, Predictive, Prescriptive — or all four."),
        ("4", "Get Instant Insights",
         "Charts, trends, forecasts, and prioritized recommendations appear instantly."),
        ("5", "Chat With Your Data",
         "Ask follow-up questions. Deciora uses Agentic RAG to answer from real data."),
        ("6", "Save & Revisit",
         "All sessions saved. Return anytime to continue or review past analysis."),
    ]
    for i, (num, title, desc) in enumerate(steps):
        with h1 if i % 2 == 0 else h2:
            st.markdown(f"""
<div class="how-step">
    <div class="step-num">{num}</div>
    <div>
        <div class="step-title">{title}</div>
        <div class="step-desc">{desc}</div>
    </div>
</div>""", unsafe_allow_html=True)

    # ── PRICING ──────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Simple Pricing</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Start free. Scale as you grow.</p>',
                unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    plans = [
        ("Starter", "Free", False, [
            "5 analyses/month",
            "CSV & Excel upload",
            "Descriptive analysis",
            "Basic charts",
            "7-day history",
        ]),
        ("Growth", "₹2,999/mo", True, [
            "Unlimited analyses",
            "All file types",
            "All 4 analysis types",
            "Agentic RAG Chat",
            "Unlimited history",
            "Priority support",
        ]),
        ("Enterprise", "Custom", False, [
            "Everything in Growth",
            "Custom integrations",
            "Team workspace",
            "API access",
            "Dedicated support",
            "On-premise option",
        ]),
    ]
    for col, (plan, price, featured, feats) in zip([p1, p2, p3], plans):
        with col:
            badge = '<div style="background:#4A9EF5;color:white;border-radius:20px;padding:0.2rem 0.8rem;font-size:0.7rem;font-weight:700;display:inline-block;margin-bottom:1rem;">MOST POPULAR</div>' if featured else ""
            feat_html = "".join([
                f'<div class="pricing-feature"><span style="color:#4A9EF5;margin-right:0.5rem;">✓</span>{f}</div>'
                for f in feats
            ])
            st.markdown(f"""
<div class="pricing-card {'featured' if featured else ''}">
    {badge}
    <div class="pricing-plan">{plan}</div>
    <span class="pricing-price">{price}</span>
    {feat_html}
</div>""", unsafe_allow_html=True)

    # ── FINAL CTA ────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
<div style="text-align:center;padding:4rem 2rem;
            background:linear-gradient(135deg,
                rgba(37,99,176,0.1),
                rgba(109,40,217,0.08));
            border-radius:20px;
            border:1px solid rgba(74,158,245,0.15);">
    <h2 style="font-family:'Syne';font-size:2.5rem;font-weight:800;
               color:#f0f4ff;margin-bottom:0.75rem;">
        Ready to Decide Smarter?
    </h2>
    <p style="font-family:'Inter';color:#8896b3;
              font-size:1rem;margin-bottom:2rem;">
        Join thousands of MSMEs making data-driven decisions with Deciora.
    </p>
</div>
""", unsafe_allow_html=True)

    cx, cy, cz = st.columns([2, 1, 2])
    with cy:
        if st.button("Get Started Free →", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    # ── FOOTER ───────────────────────────────────────────────
    st.markdown("""
<div class="footer-bar">
    <div style="font-family:'Syne';font-weight:700;color:#f0f4ff;">🔷 DECIORA</div>
    <div style="font-family:'Inter';font-size:0.8rem;color:#8896b3;">
        Intelligence That Drives Decisions
    </div>
    <div style="font-family:'Inter';font-size:0.8rem;color:#8896b3;">
        © 2025 Deciora. All rights reserved.
    </div>
</div>
""", unsafe_allow_html=True)