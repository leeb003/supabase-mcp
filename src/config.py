"""Configuration management for the Supabase MCP server."""
import os
from supabase import Client, create_client

def get_supabase_client() -> Client:
    """
    Create and return a Supabase client using environment variables.
    
    Returns:
        Supabase Client instance
    
    Raises:
        ValueError: If required environment variables are not set
    """
    url = os.getenv("SUPABASE_PROJECT_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError(
            "Missing required environment variables. "
            "Please set SUPABASE_PROJECT_URL and SUPABASE_SERVICE_ROLE_KEY"
        )
    
    return create_client(url, key)
