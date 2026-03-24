import json
from fastmcp import FastMCP
from client import api_client

def register_health_tools(mcp: FastMCP):
    """Register all health-related MCP tools"""

    @mcp.tool()
    async def check_api_health() -> str:
        """Check the general health status of the database management API"""
        try:
            result = await api_client.make_request("GET", "/health", include_auth=False)
            if result["success"]:
                return json.dumps({
                    "status": "success",
                    "message": "API is healthy",
                    "data": result["data"]
                }, indent=2)
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Health check failed with status {result['status_code']}",
                    "data": result["data"]
                }, indent=2)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to check API health: {str(e)}"
            }, indent=2)

    @mcp.tool()
    async def check_api_readiness() -> str:
        """Check if the database management API is ready to accept requests"""
        try:
            result = await api_client.make_request("GET", "/health/ready", include_auth=False)
            if result["success"]:
                return json.dumps({
                    "status": "success",
                    "message": "API is ready",
                    "data": result["data"]
                }, indent=2)
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Readiness check failed with status {result['status_code']}",
                    "data": result["data"]
                }, indent=2)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to check API readiness: {str(e)}"
            }, indent=2)

    @mcp.tool()
    async def check_api_liveness() -> str:
        """Check if the database management API is alive and responding with timestamp"""
        try:
            result = await api_client.make_request("GET", "/health/live", include_auth=False)
            if result["success"]:
                return json.dumps({
                    "status": "success",
                    "message": "API is alive",
                    "data": result["data"]
                }, indent=2)
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Liveness check failed with status {result['status_code']}",
                    "data": result["data"]
                }, indent=2)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to check API liveness: {str(e)}"
            }, indent=2)