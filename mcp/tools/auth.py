import json
from fastmcp import FastMCP
from client import api_client

def register_auth_tools(mcp: FastMCP):
    """Register all authentication-related MCP tools"""

    @mcp.tool()
    async def login_user(username: str, password: str) -> str:
        """Authenticate a user and obtain a JWT access token. Username should be an email address."""
        try:
            # The API expects form data for OAuth2PasswordRequestForm
            import httpx
            from config import settings

            async with httpx.AsyncClient(timeout=settings.timeout) as client:
                response = await client.post(
                    f"{settings.api_base_url}/auth/login",
                    data={"username": username, "password": password},
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
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
                # Store the token in the client for future authenticated requests
                token = result["data"].get("access_token")
                if token:
                    api_client.set_token(token)
                    return json.dumps({
                        "status": "success",
                        "message": "Login successful. Token has been stored for authenticated requests.",
                        "data": {
                            "access_token": token,
                            "token_type": result["data"].get("token_type", "bearer")
                        }
                    }, indent=2)
                else:
                    return json.dumps({
                        "status": "error",
                        "message": "Login succeeded but no token received",
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
                "message": f"Failed to login: {str(e)}"
            }, indent=2)

    @mcp.tool()
    async def logout_user() -> str:
        """Clear the stored JWT token, effectively logging out the user"""
        try:
            api_client.set_token("")
            return json.dumps({
                "status": "success",
                "message": "Successfully logged out. Authentication token cleared."
            }, indent=2)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to logout: {str(e)}"
            }, indent=2)

    @mcp.tool()
    async def check_auth_status() -> str:
        """Check if the user is currently authenticated and if the token is valid"""
        try:
            if not api_client.token:
                return json.dumps({
                    "status": "info",
                    "message": "Not authenticated. No token stored.",
                    "authenticated": False
                }, indent=2)

            # Try to access a protected endpoint to verify token validity
            result = await api_client.make_request("GET", "/users/token-check")

            if result["success"]:
                return json.dumps({
                    "status": "success",
                    "message": "Authentication token is valid",
                    "authenticated": True,
                    "data": result["data"]
                }, indent=2)
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Authentication token is invalid or expired (status {result['status_code']})",
                    "authenticated": False,
                    "data": result["data"]
                }, indent=2)

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to check authentication status: {str(e)}",
                "authenticated": False
            }, indent=2)