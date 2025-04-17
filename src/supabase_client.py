"""Supabase client configuration and authentication."""
import logging
import os
from typing import Optional

import httpx
from supabase import Client, create_client
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseConfig(BaseModel):
    """Configuration for Supabase client."""
    url: str = Field(..., description="Supabase project URL")
    key: str = Field(..., description="Supabase service role key")
    # access_token: str = Field(..., description="Personal access token for management API")

# def validate_access_token(access_token: str) -> bool:
#     """
#     Validate Supabase access token by attempting to list projects.
    
#     Args:
#         access_token: Personal access token to validate
        
#     Returns:
#         bool: True if token is valid, False otherwise
#     """
#     try:
#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Content-Type": "application/json"
#         }
#         response = httpx.get(
#             "https://api.supabase.com/v1/projects",
#             headers=headers
#         )
#         return response.status_code == 200
#     except Exception as e:
#         logger.error(f"Failed to validate access token: {str(e)}")
#         return False

def get_supabase_client() -> Optional[Client]:
    """
    Create and return a Supabase client using only project URL and service role key.

    Returns:
        Optional[Client]: Authenticated Supabase client or None if validation fails

    Raises:
        ValueError: If required environment variables are missing
    """
    try:
        config = SupabaseConfig(
            url=os.getenv("SUPABASE_PROJECT_URL", ""),
            key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        )
    except ValueError as e:
        logger.error(f"Missing required environment variables: {str(e)}")
        raise

    # Access token validation is not required for standard client usage
    try:
        client = create_client(config.url, config.key)
        logger.info("Successfully created Supabase client")
        return client
    except Exception as e:
        logger.error(f"Failed to create Supabase client: {str(e)}")
        return None
