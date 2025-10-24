"""
Supabase client configuration for backend
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from multiple potential locations.
# Priority: already-set env > backend/.env > project/.env > Frontend/.env > Frontend/.env.local
load_dotenv()
try:
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[2]
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "Frontend"

    # Do not override variables already set in the environment
    for dotenv_path in [
        backend_dir / ".env",
        project_root / ".env",
        frontend_dir / ".env",
        frontend_dir / ".env.local",
    ]:
        if dotenv_path.exists():
            load_dotenv(dotenv_path, override=False)
except Exception:
    # Non-fatal: proceed with whatever env is available
    pass

# Get Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL")

# Prefer service key; fall back to anon if that's all we have (limited privileges)
service_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("VITE_SUPABASE_SERVICE_KEY")
anon_key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("VITE_SUPABASE_ANON_KEY")
SUPABASE_KEY = service_key or anon_key
using_anon = service_key is None and anon_key is not None

# Initialize Supabase client
supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    if using_anon:
        print("✅ Supabase client initialized with ANON key (limited privileges)")
    else:
        print("✅ Supabase client initialized with SERVICE key")
else:
    print("⚠️  Supabase credentials not found. Database features will be disabled.")


def get_supabase_client() -> Client:
    """Get the Supabase client instance"""
    if supabase is None:
        raise Exception("Supabase client not initialized. Check your environment variables.")
    return supabase
