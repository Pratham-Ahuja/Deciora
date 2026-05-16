"""
Deciora - Session Management & RAG Memory
Handles CRUD for analysis sessions, insights, and chat messages
"""
import json
import uuid
from datetime import datetime
from backend.config import supabase


# ── Session CRUD ───────────────────────────────────────────

def create_session(user_id: str, name: str = "New Analysis", analysis_types: list = None) -> dict:
    """Create a new analysis session."""
    try:
        res = supabase.table("analysis_sessions").insert({
            "user_id": user_id,
            "analysis_name": name,
            "analysis_type": analysis_types or [],
            "status": "active",
        }).execute()
        return {"success": True, "session": res.data[0] if res.data else {}}
    except Exception as e:
        return {"success": False, "error": str(e)}


def update_session(session_id: str, **kwargs) -> dict:
    """Update session fields."""
    try:
        res = supabase.table("analysis_sessions").update({
            **kwargs,
            "updated_at": datetime.utcnow().isoformat(),
        }).eq("session_id", session_id).execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_user_sessions(user_id: str) -> list:
    """Fetch all sessions for a user ordered by recency."""
    try:
        res = supabase.table("analysis_sessions")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("updated_at", desc=True)\
            .limit(50)\
            .execute()
        return res.data or []
    except Exception:
        return []


def get_session(session_id: str) -> dict:
    """Fetch a single session."""
    try:
        res = supabase.table("analysis_sessions")\
            .select("*")\
            .eq("session_id", session_id)\
            .single()\
            .execute()
        return res.data or {}
    except Exception:
        return {}


def delete_session(session_id: str) -> bool:
    """Delete a session and all related data."""
    try:
        supabase.table("analysis_sessions")\
            .delete()\
            .eq("session_id", session_id)\
            .execute()
        return True
    except Exception:
        return False


# ── Insights CRUD ──────────────────────────────────────────

def save_insights(
    session_id: str,
    insights: dict,
    charts: list,
    recommendations: list
) -> dict:
    """Save generated insights to DB."""
    try:
        existing = supabase.table("insights")\
            .select("insight_id")\
            .eq("session_id", session_id)\
            .execute()

        payload = {
            "session_id": session_id,
            "generated_insights": json.dumps(insights),
            "charts_data": json.dumps(charts),
            "recommendations": json.dumps(recommendations),
        }

        if existing.data:
            insight_id = existing.data[0]["insight_id"]
            res = supabase.table("insights")\
                .update(payload)\
                .eq("insight_id", insight_id)\
                .execute()
        else:
            res = supabase.table("insights")\
                .insert(payload)\
                .execute()

        return {"success": True, "data": res.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_insights(session_id: str) -> dict:
    """Fetch insights for a session."""
    try:
        res = supabase.table("insights")\
            .select("*")\
            .eq("session_id", session_id)\
            .single()\
            .execute()
        if res.data:
            d = res.data
            return {
                "insights": json.loads(d["generated_insights"])
                if d["generated_insights"] else {},
                "charts": json.loads(d["charts_data"])
                if d["charts_data"] else [],
                "recommendations": json.loads(d["recommendations"])
                if d["recommendations"] else [],
            }
        return {}
    except Exception:
        return {}


# ── Chat Messages CRUD ─────────────────────────────────────

def save_message(
    session_id: str,
    sender_type: str,
    content: str,
    metadata: dict = None
) -> dict:
    """Save a chat message."""
    try:
        res = supabase.table("chat_messages").insert({
            "session_id": session_id,
            "sender_type": sender_type,
            "message_content": content,
            "metadata": json.dumps(metadata) if metadata else None,
        }).execute()
        return {"success": True, "data": res.data[0] if res.data else {}}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_chat_history(session_id: str) -> list:
    """Fetch all chat messages for a session ordered by time."""
    try:
        res = supabase.table("chat_messages")\
            .select("*")\
            .eq("session_id", session_id)\
            .order("timestamp", desc=False)\
            .execute()
        messages = []
        for row in (res.data or []):
            messages.append({
                "role": "user" if row["sender_type"] == "user" else "assistant",
                "content": row["message_content"],
                "timestamp": row["timestamp"],
            })
        return messages
    except Exception:
        return []


def get_session_context(session_id: str) -> dict:
    """
    Get full session context for RAG —
    insights + chat history in one call.
    """
    return {
        "insights": get_insights(session_id),
        "chat_history": get_chat_history(session_id),
        "session": get_session(session_id),
    }


# ── Feedback ───────────────────────────────────────────────

def submit_feedback(
    user_id: str,
    feedback_type: str,
    message: str,
    email: str = None
) -> dict:
    """Submit user feedback."""
    try:
        res = supabase.table("feedback").insert({
            "user_id": user_id,
            "feedback_type": feedback_type,
            "message": message,
            "email": email,
        }).execute()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}