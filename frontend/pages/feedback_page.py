"""
Deciora - Feedback Page
"""
import streamlit as st
from backend.session_manager import submit_feedback


def render_feedback():
    st.markdown("""
<style>
.feedback-contact-card {
    background: rgba(13,21,53,0.5);
    border: 1px solid rgba(74,158,245,0.1);
    border-radius: 10px;
    padding: 1.25rem;
    text-align: center;
    height: 100%;
}
.feedback-update-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(74,158,245,0.07);
}
.feedback-update-item:last-child {
    border-bottom: none;
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
<div style="text-align:center;padding:2.5rem 2rem 1.5rem;">
    <div style="font-family:'Syne';font-size:0.72rem;font-weight:600;
                letter-spacing:0.2em;text-transform:uppercase;
                color:#4A9EF5;margin-bottom:0.75rem;">
        We're Listening
    </div>
    <h1 style="font-family:'Syne';font-size:2.5rem;font-weight:800;
               color:#f0f4ff;margin-bottom:0.75rem;">
        Share Your Feedback
    </h1>
    <p style="font-family:'Inter';color:#8896b3;
              max-width:480px;margin:0 auto;line-height:1.7;">
        Help us build the best decision intelligence platform for MSMEs.
        Every submission shapes Deciora's roadmap.
    </p>
</div>
""", unsafe_allow_html=True)

    # ── Form + Sidebar ────────────────────────────────────────
    form_col, side_col = st.columns([3, 2])

    with form_col:
        st.markdown("""
<div style="background:rgba(13,21,53,0.7);
            border:1px solid rgba(74,158,245,0.15);
            border-radius:16px;padding:2rem;">
""", unsafe_allow_html=True)

        feedback_type = st.selectbox(
            "Feedback Type",
            ["suggestion", "bug", "feature_request", "general"],
            format_func=lambda x: {
                "suggestion":      "💡 Suggestion",
                "bug":             "🐛 Bug Report",
                "feature_request": "✨ Feature Request",
                "general":         "💬 General Feedback",
            }.get(x, x),
        )

        email = st.text_input(
            "Your Email (optional)",
            placeholder="we'll reply here if needed",
            key="feedback_email",
        )

        message = st.text_area(
            "Your Message",
            placeholder="Tell us what you think, what's broken, "
                        "or what you'd love to see in Deciora...",
            height=150,
            key="feedback_message",
        )

        rating = st.select_slider(
            "Overall Experience",
            options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
            value="⭐⭐⭐⭐",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Submit Feedback →", use_container_width=True):
            if not message.strip():
                st.error("Please write a message before submitting.")
            else:
                user    = st.session_state.get("user")
                user_id = user.id if user else None

                result = submit_feedback(
                    user_id=user_id,
                    feedback_type=feedback_type,
                    message=f"[Rating: {rating}]\n{message.strip()}",
                    email=email.strip() if email else None,
                )

                if result.get("success"):
                    st.success(
                        "✅ Thank you! Your feedback has been submitted. "
                        "We review every submission."
                    )
                    st.balloons()
                else:
                    st.error(
                        f"Could not submit: {result.get('error', 'Unknown error')}"
                    )

        st.markdown("</div>", unsafe_allow_html=True)

    with side_col:
        # Contact Info
        st.markdown("""
<div style="background:rgba(13,21,53,0.6);
            border:1px solid rgba(74,158,245,0.1);
            border-radius:14px;padding:1.5rem;margin-bottom:1rem;">
    <div style="font-family:'Syne';font-size:0.85rem;font-weight:700;
                color:#f0f4ff;margin-bottom:1rem;">Contact Us</div>
""", unsafe_allow_html=True)

        contacts = [
            ("📧", "Email",    "support@deciora.ai"),
            ("🐦", "Twitter",  "@DecioraAI"),
            ("💼", "LinkedIn", "Deciora"),
        ]
        for icon, label, val in contacts:
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:0.75rem;
            padding:0.6rem 0;
            border-bottom:1px solid rgba(74,158,245,0.07);">
    <div style="width:30px;height:30px;border-radius:6px;
                background:rgba(74,158,245,0.1);
                display:flex;align-items:center;
                justify-content:center;font-size:14px;
                flex-shrink:0;">{icon}</div>
    <div>
        <div style="font-family:'Inter';font-size:0.7rem;color:#4a5880;">
            {label}
        </div>
        <div style="font-family:'Inter';font-size:0.82rem;color:#c8d8f0;">
            {val}
        </div>
    </div>
</div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Recent Updates
        st.markdown("""
<div style="background:rgba(13,21,53,0.6);
            border:1px solid rgba(74,158,245,0.1);
            border-radius:14px;padding:1.5rem;">
    <div style="font-family:'Syne';font-size:0.85rem;font-weight:700;
                color:#f0f4ff;margin-bottom:1rem;">Recent Updates</div>
""", unsafe_allow_html=True)

        updates = [
            ("#4ade80", "Multi-file analysis now in beta",         "New"),
            ("#f87171", "Fixed chart rendering on large datasets", "Fix"),
            ("#a78bfa", "PDF export — on roadmap (38 requests)",   "Soon"),
            ("#4A9EF5", "Tally & Zoho integration — Q3 planned",   "Q3"),
        ]
        for color, text, tag in updates:
            st.markdown(f"""
<div class="feedback-update-item">
    <div style="width:7px;height:7px;border-radius:50%;
                background:{color};margin-top:4px;flex-shrink:0;"></div>
    <div style="font-family:'Inter';font-size:0.8rem;
                color:#8896b3;line-height:1.5;flex:1;">{text}</div>
    <span style="font-size:0.68rem;font-weight:600;
                 padding:2px 7px;border-radius:20px;
                 background:rgba(74,158,245,0.1);
                 color:#4A9EF5;white-space:nowrap;">{tag}</span>
</div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)