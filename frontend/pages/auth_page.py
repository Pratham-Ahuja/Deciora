"""
Deciora - Authentication Page (Login / Signup)
"""
import streamlit as st
from backend.auth import sign_in, sign_up


def render_auth():
    st.markdown("""
<style>
.auth-wrapper {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}
.auth-card {
    background: rgba(13,21,53,0.85);
    border: 1px solid rgba(74,158,245,0.2);
    border-radius: 20px;
    padding: 3rem;
    max-width: 480px;
    width: 100%;
    backdrop-filter: blur(20px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.auth-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.25rem;
    color: #f0f4ff;
}
.auth-logo span {
    background: linear-gradient(135deg, #4A9EF5, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.auth-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: #8896b3;
    text-align: center;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

    # ── Back Button ───────────────────────────────────────────
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Home"):
            st.session_state.page = "landing"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Auth Card ─────────────────────────────────────────────
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown("""
<div class="auth-logo">🔷 <span>DECIORA</span></div>
<div class="auth-tagline">Intelligence That Drives Decisions</div>
""", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign In", "Create Account"])

        with tab1:
            render_login()

        with tab2:
            render_signup()


def render_login():
    st.markdown("<br>", unsafe_allow_html=True)

    email = st.text_input(
        "Email Address",
        placeholder="you@company.com",
        key="login_email"
    )
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Your password",
        key="login_password"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Sign In →", use_container_width=True, key="login_btn"):
        if not email or not password:
            st.error("Please enter your email and password.")
            return

        with st.spinner("Signing in..."):
            result = sign_in(email.strip(), password)

        if result["success"]:
            st.session_state.user = result["user"]
            st.session_state.access_token = result["access_token"]
            st.session_state.page = "workspace"
            st.success("Welcome back! Loading your workspace...")
            st.rerun()
        else:
            st.error(f"❌ {result['error']}")


def render_signup():
    st.markdown("<br>", unsafe_allow_html=True)

    email = st.text_input(
        "Email Address",
        placeholder="you@company.com",
        key="signup_email"
    )
    company = st.text_input(
        "Company / Business Name",
        placeholder="Acme Pvt. Ltd.",
        key="signup_company"
    )
    biz_type = st.selectbox(
        "Business Type",
        [
            "Retail",
            "Manufacturing",
            "Services",
            "E-commerce",
            "Restaurant / Food",
            "Healthcare",
            "Education",
            "Logistics",
            "Real Estate",
            "Other",
        ],
        key="signup_biztype",
    )
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Min. 8 characters",
        key="signup_password"
    )
    confirm = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Repeat password",
        key="signup_confirm"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Create Account →", use_container_width=True, key="signup_btn"):
        if not email or not company or not password:
            st.error("Please fill in all required fields.")
            return
        if password != confirm:
            st.error("Passwords do not match.")
            return
        if len(password) < 8:
            st.error("Password must be at least 8 characters.")
            return

        with st.spinner("Creating your account..."):
            result = sign_up(
                email.strip(),
                password,
                company.strip(),
                biz_type
            )

        if result["success"]:
            st.success("✅ Account created! Please check your email to verify, then sign in.")
        else:
            st.error(f"❌ {result['error']}")