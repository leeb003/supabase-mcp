"""Type definitions for the Supabase MCP server."""
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field

# Type definitions
JsonValue = Union[str, int, float, bool, None]
FilterDict = Dict[str, JsonValue]

class TableQuery(BaseModel):
    """Base model for table operations with common fields."""
    table_name: str = Field(..., description="Name of the table to operate on")

class ReadQuery(TableQuery):
    """Model for read operations."""
    columns: Optional[List[str]] = Field(None, description="List of columns to return. If None, returns all columns")
    filters: Optional[FilterDict] = Field(None, description="Column-value pairs for filtering rows")
    limit: Optional[int] = Field(None, description="Maximum number of rows to return")
    order_by: Optional[Dict[str, str]] = Field(None, description="Column to sort by with direction ('asc' or 'desc')")

class CreateQuery(TableQuery):
    """Model for create operations."""
    records: List[Dict[str, JsonValue]] = Field(..., description="List of records to insert")

class UpdateQuery(TableQuery):
    """Model for update operations."""
    updates: Dict[str, JsonValue] = Field(..., description="Column-value pairs to update")
    filters: FilterDict = Field(..., description="Column-value pairs to filter records to update")

class DeleteQuery(TableQuery):
    """Model for delete operations."""
    filters: FilterDict = Field(..., description="Column-value pairs to filter records to delete")
