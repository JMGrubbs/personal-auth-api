import json
from fastmcp import FastMCP
from client import api_client

def register_users_tools(mcp: FastMCP):
    """Register all user management MCP tools"""

    @mcp.tool()
    async def get_current_user() -> str:
        """Get the current authenticated user's profile information"""
        try:
            result = await api_client.make_request("GET", "/users/me")

            if result["success"]:
                return json.dumps({
                    "status": "success",
                    "message": "Successfully retrieved user profile",
                    "data": result["data"]
                }, indent=2)
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Failed to get user profile with status {result['status_code']}",
                    "data": result["data"]
                }, indent=2)

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to get current user: {str(e)}"
            }, indent=2)

    @mcp.tool()
    async def create_new_user(email: str, password: str) -> str:
        """Create a new user account with email and password. Password must meet security requirements: at least 8 characters, contains digit, letter, and special character."""
        try:
            user_data = {
                "email": email,
                "password": password
            }

            result = await api_client.make_request("POST", "/users/create", data=user_data, include_auth=False)

            if result["success"]:
                return json.dumps({
                    "status": "success",
                    "message": "User account created successfully",
                    "data": result["data"]
                }, indent=2)
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Failed to create user with status {result['status_code']}",
                    "data": result["data"]
                }, indent=2)

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to create user: {str(e)}"
            }, indent=2)

    @mcp.tool()
    async def login_user_simple(email: str, password: str) -> str:
        """Simple user login that returns a token. This uses the users/login endpoint which expects a GET request with JSON body."""
        try:
            import httpx
            from config import settings

            # The /users/login endpoint uses GET with JSON body (unusual but matches the API)
            login_data = {
                "email": email,
                "password": password
            }

            async with httpx.AsyncClient(timeout=settings.timeout) as client:
                response = await client.request(
                    method="GET",
                    url=f"{settings.api_base_url}/users/login",
                    json=login_data,
                    headers={"Content-Type": "application/json"}
                )

                result = {
                    "status_code": response.status_code,
                    "success": 200 <= response.status_code < 300
                }

                try:
                    result["data"] = response.json()
                except json.JSONDecodeError:
                    result["data"] = {"message": response.text}

            if result["success"]:
                # Store the token if available
                token = result["data"].get("token")
                if token:
                    api_client.set_token(token)
                    return json.dumps({
                        "status": "success",
                        "message": "Login successful. Token has been stored for authenticated requests.",
                        "data": result["data"]
                    }, indent=2)
                else:
                    return json.dumps({
                        "status": "success",
                        "message": "Login response received",
                        "data": result["data"]
                    }, indent=2)
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Login failed with status {result['status_code']}",
                    "data": result["data"]
                }, indent=2)

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to login user: {str(e)}"
            }, indent=2)

    @mcp.tool()
    async def validate_token() -> str:
        """Validate the current JWT token by checking against the API"""
        try:
            if not api_client.token:
                return json.dumps({
                    "status": "error",
                    "message": "No authentication token stored. Please login first.",
                    "valid": False
                }, indent=2)

            result = await api_client.make_request("GET", "/users/token-check")

            if result["success"]:
                return json.dumps({
                    "status": "success",
                    "message": "Token is valid",
                    "valid": True,
                    "data": result["data"]
                }, indent=2)
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Token validation failed with status {result['status_code']}",
                    "valid": False,
                    "data": result["data"]
                }, indent=2)

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to validate token: {str(e)}",
                "valid": False
            }, indent=2)