"""
Deciora - Configuration & Supabase Client
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# ── Core Settings ──────────────────────────────────────────
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
STORAGE_BUCKET = os.environ.get("SUPABASE_STORAGE_BUCKET", "deciora-files")
MAX_FILE_SIZE_MB = int(os.environ.get("MAX_FILE_SIZE_MB", 50))
APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY", "deciora-dev-secret-key")

# ── Supabase Clients ───────────────────────────────────────
def get_supabase_client() -> Client:
    """Public client for user-context operations."""
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_supabase_admin() -> Client:
    """Service role client for admin operations."""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Singleton clients
supabase: Client = get_supabase_client()
supabase_admin: Client = get_supabase_admin()