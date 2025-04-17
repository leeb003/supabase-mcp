"""
Supabase MCP Server - A Model Context Protocol server for Supabase database operations.
Provides tools for CRUD operations on Supabase tables via FastAPI and MCP.
"""
from dotenv import load_dotenv
load_dotenv()

import json
import os
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastmcp import FastMCP
from pydantic import BaseModel

from .supabase_client import get_supabase_client
from .tools.database import read_table_rows, create_records, update_records, delete_records
from .sse import router as sse_router
from src.db_types import ReadQuery, CreateQuery, UpdateQuery, DeleteQuery

# Load configuration
with open("config.json") as f:
    config = json.load(f)

# Initialize FastAPI
app = FastAPI(
    title=config["server"]["name"],
    version=config["server"]["version"]
)

# Initialize MCP
mcp = FastMCP(transport="stdio")

# Initialize Supabase client
supabase = get_supabase_client()
if not supabase:
    raise RuntimeError("Failed to initialize Supabase client")

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": config["server"]["version"]
    }

# Register MCP tools
mcp.tool()(read_table_rows)
mcp.tool()(create_records)
mcp.tool()(update_records)
mcp.tool()(delete_records)

# Include the SSE router
app.include_router(sse_router, prefix="/sse", tags=["sse"])

if __name__ == "__main__":
    # Start FastAPI with uvicorn
    port = int(os.getenv("SERVER_PORT", config["server"]["port"]))
    uvicorn.run(
        app,
        host=config["server"]["host"],
        port=port,
        log_level="info"
    )
