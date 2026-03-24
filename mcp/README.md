# Database Management API - MCP Server

This Model Context Protocol (MCP) server provides programmatic access to the Database Management API endpoints, enabling AI agents and tools to interact with the database management system through a standardized interface.

## Overview

The MCP server acts as a bridge between MCP-compatible AI tools (like Claude Desktop, Cline, etc.) and the Database Management FastAPI backend. It provides tools for health monitoring, user authentication, and user management operations.

## Architecture

The MCP server is organized into modular components:

```
mcp/
├── main.py              # Main MCP server entry point
├── config.py            # Configuration management
├── client.py            # HTTP client for API communication
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
└── tools/              # MCP tool modules
    ├── __init__.py
    ├── health.py        # Health monitoring tools
    ├── auth.py          # Authentication tools
    └── users.py         # User management tools
```

## Available MCP Tools

### Health Monitoring Tools

- **`check_api_health`** - Check the general health status of the database management API
- **`check_api_readiness`** - Check if the API is ready to accept requests
- **`check_api_liveness`** - Check if the API is alive and responding with timestamp

### Authentication Tools

- **`login_user`** - Authenticate a user and obtain a JWT access token (OAuth2 flow)
- **`logout_user`** - Clear the stored JWT token, effectively logging out
- **`check_auth_status`** - Check if the user is currently authenticated and token validity

### User Management Tools

- **`get_current_user`** - Get the current authenticated user's profile information
- **`create_new_user`** - Create a new user account with email and password
- **`login_user_simple`** - Alternative login method using the users/login endpoint
- **`validate_token`** - Validate the current JWT token

## Configuration

The MCP server can be configured using environment variables:

```bash
# API connection settings
API_BASE_URL=http://database-managment-api:8000/api/v1
TIMEOUT=30
```

Copy `.env.example` to `.env` and adjust the values as needed.

## Usage Example

1. **Check API Health**
   ```
   Use the check_api_health tool to verify the API is running
   ```

2. **Create a New User**
   ```
   Use create_new_user with email: "user@example.com", password: "SecurePass123!"
   ```

3. **Login**
   ```
   Use login_user with username: "user@example.com", password: "SecurePass123!"
   ```

4. **Get User Profile**
   ```
   Use get_current_user (requires authentication)
   ```

## Authentication Flow

The MCP server maintains authentication state by storing JWT tokens received from login operations. Once authenticated, subsequent calls to protected endpoints automatically include the authorization header.

1. Call `login_user` or `login_user_simple` with credentials
2. The server stores the JWT token automatically
3. Protected endpoints (like `get_current_user`) use the stored token
4. Call `logout_user` to clear the token when done

## Password Requirements

When creating new users, passwords must meet these security requirements:
- At least 8 characters long
- Contains at least one digit
- Contains at least one letter
- Contains at least one special character (!@#$%^&*()-_=+[]{}|;:,.<>?/)

## Error Handling

All MCP tools return JSON responses with a consistent structure:

```json
{
  "status": "success|error|info",
  "message": "Descriptive message",
  "data": {...},  // API response data (when applicable)
  "authenticated": true|false  // For auth-related tools
}
```

## Development

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the MCP server
python main.py
```

### Running with Docker

```bash
# Build and run via docker-compose (from project root)
docker-compose up database-managment-mcp
```

The MCP server will be available at `http://localhost:8001`

## Integration

This MCP server is designed to work with:
- Claude Desktop with MCP support
- Cline VS Code extension
- Any MCP-compatible AI tool or framework

Add the server configuration to your MCP client:

```json
{
  "mcpServers": {
    "db-management": {
      "command": "python",
      "args": ["path/to/mcp/main.py"],
      "env": {
        "API_BASE_URL": "http://localhost:8000/api/v1"
      }
    }
  }
}
```

## API Endpoint Mapping

| MCP Tool | HTTP Method | API Endpoint | Description |
|----------|-------------|--------------|-------------|
| `check_api_health` | GET | `/health` | Health check |
| `check_api_readiness` | GET | `/health/ready` | Readiness check |
| `check_api_liveness` | GET | `/health/live` | Liveness check |
| `login_user` | POST | `/auth/login` | OAuth2 login |
| `create_new_user` | POST | `/users/create` | Create user |
| `get_current_user` | GET | `/users/me` | Get user profile |
| `login_user_simple` | GET | `/users/login` | Simple login |
| `validate_token` | GET | `/users/token-check` | Validate token |

## Dependencies

- **fastmcp**: MCP server framework
- **httpx**: Async HTTP client
- **pydantic**: Data validation and settings
- **python-dotenv**: Environment variable management
- **starlette**: ASGI framework components
- **uvicorn**: ASGI server

## License

MIT License - See the main project LICENSE file for details.