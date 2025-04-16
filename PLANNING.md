# Supabase MCP Server Planning Document

## Project Overview
The goal is to develop a Python-based **Supabase MCP Server** that enables Large Language Models (LLMs) to interact with Supabase projects via the Model Context Protocol (MCP). This server will act as a middleware layer, translating AI-driven requests from MCP-compatible clients (e.g., Cursor, Windsurf, Cline) into Supabase operations, such as database queries, schema management, and Management API calls. The project prioritizes ease of setup, safety, and extensibility.

## Objectives
- **Core Functionality**: Implement MCP tools for database CRUD operations, schema management, and Supabase Management API access.
- **Safety**: Include read-only modes, SQL query validation, and transaction handling to prevent destructive operations.
- **Compatibility**: Ensure seamless integration with MCP clients supporting the stdio protocol.
- **Extensibility**: Design a modular architecture for adding tools (e.g., edge function invocation, storage management) in future iterations.
- **MVP Scope**: Deliver a functional server with basic database operations and authentication within 4-6 weeks.

## Scope
### In-Scope
- Authentication via Supabase personal access tokens.
- Tools for:
  - Executing SQL queries (SELECT, INSERT, UPDATE, DELETE).
  - Managing database schemas (CREATE, ALTER, DROP).
  - Accessing Supabase Management API (e.g., list projects, create tables).
- Read-only mode and basic SQL query validation.
- Configuration via environment variables and a `config.json` file.
- Support for local and remote Supabase instances.
- Integration with MCP clients like Cursor and Windsurf.

### Out-of-Scope (MVP)
- Edge function invocation (planned for v0.4.0).
- Storage management (planned for v0.5.0).
- OAuth 2.0 authentication (awaiting MCP spec updates).
- Session pooling for database connections (transaction pooling only).
- Advanced schema discovery (e.g., triggers, views).

## Technology Stack
- **Language**: Python 3.11+ for its Supabase SDK and ecosystem.
- **Framework**: FastAPI for building the MCP server with async support.
- **Database Client**: Supabase Python SDK (`supabase-py`) and `psycopg2` for direct Postgres access.
- **Configuration**: `python-dotenv` for environment variables, JSON for config files.
- **MCP Protocol**: Implement stdio protocol for client communication.
- **Dependencies**: `pydantic` for data validation, `uv` or `pipx` for package management.
- **Testing**: `pytest` for unit and integration tests.
- **Logging**: `logging` module for debugging and monitoring.

## Architecture
- **Server**: A FastAPI application exposing MCP tools as endpoints, handling requests from clients via stdio.
- **Tools**: Modular Python classes defining MCP tools (e.g., `query_table`, `create_table`).
- **Authentication**: Validate Supabase access tokens or service role keys.
- **Database Connection**: Use Supabase SDK for API calls and `psycopg2` for direct SQL execution.
- **Safety Layer**: Validate SQL queries for risk levels (safe, write, destructive) and enforce read-only modes.
- **Configuration**: Load settings from `.env` and `config.json` for flexibility.

## Risks and Mitigation
- **Risk**: MCP client compatibility issues.
  - **Mitigation**: Test with Cursor, Windsurf, and Cline; follow MCP spec v0.3.6.
- **Risk**: SQL injection or unsafe queries.
  - **Mitigation**: Implement query validation and read-only modes.
- **Risk**: Supabase SDK limitations for advanced features.
  - **Mitigation**: Use `psycopg2` for direct Postgres access as a fallback.
- **Risk**: OAuth support delays due to MCP spec updates.
  - **Mitigation**: Start with access tokens, plan OAuth integration for v0.4.0.

## Success Metrics
- Successful connection to Supabase from Cursor/Windsurf with green status.
- Execute 10+ SQL queries without errors.
- Create and manage 5+ tables via AI prompts.
- 90% test coverage for core tools.
- Positive feedback from 10+ GitHub users within 3 months.