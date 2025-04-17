# Initial Tasks for Supabase MCP Server Project

This document outlines the initial tasks to kick off the development of the Python-based Supabase MCP Server. These tasks focus on setting up the project, implementing core authentication, and building a minimal query tool.


### Task 1: Project Setup

- **Description**: Initialize the project repository and configure the development environment.

- **Subtasks**:

  - Create a GitHub repository (`supabase-mcp-server-python`).

  - Set up a Python 3.11+ virtual environment using `uv` or `venv`.

  - Install core dependencies: `fastapi`, `uvicorn`, `supabase-py`, `psycopg2`, `python-dotenv`, `pydantic`, `pytest`.

  - Create a basic project structure:

    ```
    supabase-mcp-server/
    ├── src/
    │   ├── server.py        # FastAPI server
    │   ├── tools/           # MCP tool definitions
    │   ├── config.py        # Configuration loader
    │   └── types.py         # Pydantic models
    ├── tests/
    ├── .env.example
    ├── config.json.example
    ├── README.md
    ├── requirements.txt
    └── pyproject.toml
    ```

  - Initialize `README.md` with project overview and setup instructions.

  - Configure `pytest` for testing.

- **Assignee**: Developer

- **Estimated Time**: 8 hours

- **Deliverable**: Functional project skeleton with dependencies installed.

### Task 2: Environment Configuration

- **Description**: Implement configuration loading for Supabase credentials and server settings.

- **Subtasks**:

  - Create `.env.example` with:

    ```
    SUPABASE_URL=your_project_url
    SUPABASE_KEY=your_service_role_key
    SERVER_PORT=3000
    ```

  - Create `config.json.example` with:

    ```json
    {
      "server": {
        "name": "supabase-mcp-server",
        "version": "0.1.0",
        "port": 3000,
        "host": "localhost"
      }
    }
    ```

  - Implement `src/config.py` to load environment variables and JSON config using `python-dotenv` and `pydantic`.

  - Validate required fields (e.g., `SUPABASE_URL`).

- **Deliverable**: Configuration module with environment and JSON loading.

### Task 3: FastAPI Server Setup

- **Description**: Set up a basic FastAPI server to handle MCP client requests via stdio.
- **Subtasks**:
  - Create `src/server.py` with a FastAPI app.
  - Implement a `/health` endpoint for server status.
  - Configure `uvicorn` to run the server with stdio support for MCP clients.
  - Test server startup with `python -m src.server`.
- **Deliverable**: Running FastAPI server with health check endpoint.

### Task 4: Authentication with Supabase

- **Description**: Implement authentication using Supabase personal access tokens.
- **Subtasks**:
  - Initialize Supabase client in `src/supabase_client.py` using `supabase-py` with `SUPABASE_URL` and `SUPABASE_KEY`.
  - Create a function to validate the access token by calling the Supabase Management API (e.g., list projects).
  - Handle authentication errors with clear logging.
  - Write unit tests for token validation.
- **Deliverable**: Authenticated Supabase client with validated access token.

### Task 5: Basic Query Tool

- **Description**: Implement an MCP tool for executing simple SELECT queries.

- **Subtasks**:

  - Define a `query_table` tool in `src/tools/query_table.py` using Pydantic models:

    ```python
    from pydantic import BaseModel
    
    class QueryTableInput(BaseModel):
        schema: str = "public"
        table: str
        select: str = "*"
        where: list[dict] = []
    
    class QueryTableOutput(BaseModel):
        data: list[dict]
        error: str | None
    ```

  - Implement tool logic to:

    - Validate input (e.g., schema and table names).
    - Construct SQL query using `psycopg2`.
    - Execute query in read-only mode.
    - Return results or errors.

  - Expose the tool via a FastAPI endpoint compatible with MCP stdio.

  - Write integration tests with a local Supabase instance (use `npx supabase start`).

- **Deliverable**: Functional `query_table` tool with test coverage.

### Task 6: MCP Client Integration Test

- **Description**: Test the server with Cursor to ensure compatibility.

- **Subtasks**:

  - Create a `.cursor/mcp.json` file for testing:

    ```json
    {
      "mcpServers": {
        "supabase": {
          "command": "python",
          "args": ["-m", "src.server"],
          "env": {}
        }
      }
    }
    ```

  - Launch Cursor, navigate to Settings/MCP, and verify green status.

  - Test a simple query (e.g., “List all users”) via Cursor’s interface.

  - Document setup instructions in `README.md`.

- **Deliverable**: Verified Cursor integration with setup guide.

## Next Steps

- Add tools for INSERT/UPDATE/DELETE, implement transaction handling.
- Introduce schema management tools (CREATE/ALTER) and query validation.
- Regularly update `README.md` and solicit GitHub feedback.