"""
Deciora - Authentication Module
Handles login, signup, logout via Supabase Auth
"""
import streamlit as st
from backend.config import supabase


def sign_up(email: str, password: str, company_name: str, business_type: str) -> dict:
    """Register a new user."""
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        if res.user:
            # Update profile
            supabase.table("users").upsert({
                "id": res.user.id,
                "email": email,
                "company_name": company_name,
                "business_type": business_type,
            }).execute()
            return {"success": True, "user": res.user}
        return {"success": False, "error": "Signup failed. Please try again."}
    except Exception as e:
        err = str(e)
        if "already registered" in err.lower() or "duplicate" in err.lower():
            return {"success": False, "error": "An account with this email already exists."}
        return {"success": False, "error": err}


def sign_in(email: str, password: str) -> dict:
    """Authenticate an existing user."""
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        if res.user and res.session:
            return {
                "success": True,
                "user": res.user,
                "session": res.session,
                "access_token": res.session.access_token,
            }
        return {"success": False, "error": "Invalid credentials."}
    except Exception as e:
        err = str(e)
        if "invalid" in err.lower() or "credentials" in err.lower():
            return {"success": False, "error": "Incorrect email or password."}
        return {"success": False, "error": err}


def sign_out():
    """Log out the current user."""
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def get_user_profile(user_id: str) -> dict:
    """Fetch user profile from DB."""
    try:
        res = supabase.table("users").select("*").eq("id", user_id).single().execute()
        return res.data or {}
    except Exception:
        return {}


def is_authenticated() -> bool:
    """Check if user is authenticated in current session."""
    return (
        "user" in st.session_state
        and st.session_state.user is not None
        and "access_token" in st.session_state
    )