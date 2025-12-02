# supabase_helpers.py
"""
Minimal helper to create and expose a Supabase client.
Set SUPABASE_URL and SUPABASE_KEY (service_role or anon) in environment.
Install: pip install supabase
Exports:
    supabase  -> supabase client or None
You can also add bespoke helper functions (RPC wrappers) here.
"""
import os
from typing import Optional

try:
    from supabase import create_client  # pip package "supabase"
except Exception:
    create_client = None
from dotenv import load_dotenv
load_dotenv()


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = None

if create_client and SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        # Keep supabase None but don't crash import — database.py will check and raise if needed.
        supabase = None

# Optional helper example (you can extend this file with app-specific wrappers)
def get_planos(limit: int = 100):
    if not supabase:
        raise RuntimeError("Supabase client not configured")
    resp = supabase.table("plano").select("*").limit(limit).execute()
    return getattr(resp, "data", None) or resp
