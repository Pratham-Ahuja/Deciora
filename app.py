"""
Deciora - Main Application Entry Point
Intelligence That Drives Decisions
"""
import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Deciora — Intelligence That Drives Decisions",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from frontend.styles import inject_global_styles
from backend.auth import is_authenticated

# ── Route to appropriate page ──────────────────────────────

def main():
    inject_global_styles()

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    if "user" not in st.session_state:
        st.session_state.user = None

    # Routing
    if is_authenticated():
        from frontend.pages.workspace import render_workspace
        render_workspace()
    else:
        page = st.session_state.get("page", "landing")
        if page == "landing":
            from frontend.pages.landing import render_landing
            render_landing()
        elif page == "login":
            from frontend.pages.auth_page import render_auth
            render_auth()
        elif page == "about":
            from frontend.pages.about import render_about
            render_about()
        elif page == "feedback":
            from frontend.pages.feedback_page import render_feedback
            render_feedback()
        else:
            from frontend.pages.landing import render_landing
            render_landing()


if __name__ == "__main__":
    main()