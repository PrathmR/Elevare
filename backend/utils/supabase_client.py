"""
Supabase client configuration for backend
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Get Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # Use service key for backend

# Initialize Supabase client
supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase client initialized")
else:
    print("⚠️  Supabase credentials not found. Database features will be disabled.")


def get_supabase_client() -> Client:
    """Get the Supabase client instance"""
    if supabase is None:
        raise Exception("Supabase client not initialized. Check your environment variables.")
    return supabase
