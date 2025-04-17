"""Database operation tools for the Supabase MCP server."""
from typing import Dict, List

from src.db_types import ReadQuery, CreateQuery, UpdateQuery, DeleteQuery
from ..config import get_supabase_client

# Initialize Supabase client
supabase = get_supabase_client()

def read_table_rows(query: ReadQuery) -> List[Dict]:
    """
    Read and filter rows from a Supabase table.
    
    Perfect for:
    - Retrieving specific records based on criteria
    - Getting all records from a table
    - Fetching only certain columns
    - Sorting and limiting results
    
    Args:
        query: ReadQuery object containing:
            - table_name: Name of the table to read from
            - columns: Optional list of columns to return
            - filters: Optional filtering criteria
            - limit: Optional maximum number of rows
            - order_by: Optional sorting criteria
    
    Returns:
        List of dictionaries representing the matching rows
    """
    db_query = supabase.table(query.table_name)
    
    if query.columns:
        db_query = db_query.select(",".join(query.columns))
    else:
        db_query = db_query.select("*")
    
    if query.filters:
        for column, value in query.filters.items():
            db_query = db_query.eq(column, value)
    
    if query.order_by:
        for column, direction in query.order_by.items():
            db_query = db_query.order(column, ascending=(direction.lower() == "asc"))
    
    if query.limit:
        db_query = db_query.limit(query.limit)
    
    return db_query.execute().data

def create_records(query: CreateQuery) -> List[Dict]:
    """
    Create one or multiple records in a Supabase table.
    
    Perfect for:
    - Inserting new data into tables
    - Batch creating multiple records at once
    - Adding new entries with validated data
    
    Args:
        query: CreateQuery object containing:
            - table_name: Name of the table to insert into
            - records: List of records to create
    
    Returns:
        List of created records with their assigned IDs
    """
    return supabase.table(query.table_name).insert(query.records).execute().data

def update_records(query: UpdateQuery) -> List[Dict]:
    """
    Update records in a Supabase table that match specific criteria.
    
    Perfect for:
    - Modifying existing records that match certain conditions
    - Batch updating multiple records
    - Safely updating data with validation
    
    Args:
        query: UpdateQuery object containing:
            - table_name: Name of the table to update
            - updates: Column-value pairs to update
            - filters: Criteria to select records to update
    
    Returns:
        List of updated records
    """
    db_query = supabase.table(query.table_name)
    update_call = db_query.update(query.updates)
    if query.filters:
        for column, value in query.filters.items():
            update_call = update_call.eq(column, value)
    return update_call.execute().data

def delete_records(query: DeleteQuery) -> List[Dict]:
    """
    Delete records from a Supabase table that match specific criteria.
    
    Perfect for:
    - Removing records that meet certain conditions
    - Batch deleting multiple records
    - Cleaning up obsolete data
    
    Warning:
    - This operation permanently removes data
    - Always double-check filter criteria
    - Consider soft deletes when appropriate
    
    Args:
        query: DeleteQuery object containing:
            - table_name: Name of the table to delete from
            - filters: Criteria to select records to delete
    
    Returns:
        List of deleted records
    """
    db_query = supabase.table(query.table_name)
    delete_call = db_query.delete()
    if query.filters:
        for column, value in query.filters.items():
            delete_call = delete_call.eq(column, value)
    return delete_call.execute().data
