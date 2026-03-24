from fastmcp import FastMCP
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

# Load environment variables
load_dotenv()

# Import tool registration functions
from tools import register_health_tools, register_auth_tools, register_users_tools

# Create MCP server instance
app = FastMCP(name="Database Management API MCP Server")

# Register all tools
register_health_tools(app)
register_auth_tools(app)
register_users_tools(app)

if __name__ == "__main__":
    app.run(
        transport="http",
        host="127.0.0.1",
        port=8001,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_credentials=True,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
                expose_headers=["Mcp-Session-Id", "mcp-session-id"],
            )
        ]
    )