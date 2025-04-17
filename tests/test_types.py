"""Tests for the Supabase MCP server type definitions."""
import pytest
from src.db_types import ReadQuery, CreateQuery, UpdateQuery, DeleteQuery

def test_read_query_validation():
    """Test ReadQuery validation."""
    # Test valid query
    query = ReadQuery(
        table_name="users",
        columns=["id", "name"],
        filters={"active": True},
        order_by={"created_at": "desc"},
        limit=10
    )
    assert query.table_name == "users"
    assert query.columns == ["id", "name"]
    assert query.filters == {"active": True}
    assert query.order_by == {"created_at": "desc"}
    assert query.limit == 10

    # Test minimal query
    query = ReadQuery(table_name="users")
    assert query.table_name == "users"
    assert query.columns is None
    assert query.filters is None
    assert query.order_by is None
    assert query.limit is None

def test_create_query_validation():
    """Test CreateQuery validation."""
    query = CreateQuery(
        table_name="users",
        records=[
            {"name": "John", "email": "john@example.com"},
            {"name": "Jane", "email": "jane@example.com"}
        ]
    )
    assert query.table_name == "users"
    assert len(query.records) == 2

def test_update_query_validation():
    """Test UpdateQuery validation."""
    query = UpdateQuery(
        table_name="users",
        updates={"status": "active"},
        filters={"email": "john@example.com"}
    )
    assert query.table_name == "users"
    assert query.updates == {"status": "active"}
    assert query.filters == {"email": "john@example.com"}

def test_delete_query_validation():
    """Test DeleteQuery validation."""
    query = DeleteQuery(
        table_name="users",
        filters={"status": "inactive"}
    )
    assert query.table_name == "users"
    assert query.filters == {"status": "inactive"}
