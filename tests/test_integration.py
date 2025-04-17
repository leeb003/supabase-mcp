"""Integration tests for the Supabase MCP server."""
import os
import pytest
from supabase import Client

from src.supabase_client import get_supabase_client
from src.db_types import ReadQuery, CreateQuery, UpdateQuery, DeleteQuery
from src.tools.database import read_table_rows, create_records, update_records, delete_records

@pytest.fixture
def supabase_client() -> Client:
    """Get Supabase client for testing."""
    client = get_supabase_client()
    if not client:
        pytest.skip("Supabase client not available")
    return client

def test_read_table_rows_integration(supabase_client):
    """Test reading rows from a table."""
    query = ReadQuery(
        table_name="users",
        columns=["id", "email"],
        limit=5
    )
    result = read_table_rows(query)
    assert isinstance(result, list)
    if result:
        assert "id" in result[0]
        assert "email" in result[0]

def test_create_records_integration(supabase_client):
    """Test creating records in a table."""
    # Clean up any existing test user before running the test
    delete_query = DeleteQuery(
        table_name="users",
        filters={"email": "test@example.com"}
    )
    delete_records(delete_query)

    test_user = {
        "email": "test@example.com",
        "name": "Test User"
    }
    query = CreateQuery(
        table_name="users",
        records=[test_user]
    )
    result = create_records(query)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["email"] == test_user["email"]
    
    # Clean up
    delete_query = DeleteQuery(
        table_name="users",
        filters={"email": test_user["email"]}
    )
    delete_records(delete_query)


def test_update_records_integration(supabase_client):
    """Test updating records in a table."""
    # Clean up any existing test user before running the test
    delete_query = DeleteQuery(
        table_name="users",
        filters={"email": "update_test@example.com"}
    )
    delete_records(delete_query)

    # First create a test record
    test_user = {
        "email": "update_test@example.com",
        "name": "Update Test"
    }
    create_query = CreateQuery(
        table_name="users",
        records=[test_user]
    )
    created = create_records(create_query)
    
    # Update the record
    update_query = UpdateQuery(
        table_name="users",
        updates={"name": "Updated Name"},
        filters={"email": test_user["email"]}
    )
    result = update_records(update_query)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["name"] == "Updated Name"
    
    # Clean up
    delete_query = DeleteQuery(
        table_name="users",
        filters={"email": test_user["email"]}
    )
    delete_records(delete_query)


def test_delete_records_integration(supabase_client):
    """Test deleting records from a table."""
    # Clean up any existing test user before running the test
    delete_query = DeleteQuery(
        table_name="users",
        filters={"email": "delete_test@example.com"}
    )
    delete_records(delete_query)

    # First create a test record
    test_user = {
        "email": "delete_test@example.com",
        "name": "Delete Test"
    }
    create_query = CreateQuery(
        table_name="users",
        records=[test_user]
    )
    created = create_records(create_query)
    
    # Delete the record
    delete_query = DeleteQuery(
        table_name="users",
        filters={"email": test_user["email"]}
    )
    result = delete_records(delete_query)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["email"] == test_user["email"]
