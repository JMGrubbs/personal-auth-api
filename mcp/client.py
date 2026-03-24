import httpx
import json
from typing import Dict, Any, Optional
from config import settings

class APIClient:
    def __init__(self):
        self.base_url = settings.api_base_url
        self.timeout = settings.timeout
        self.token: Optional[str] = None

    def set_token(self, token: str):
        """Set the JWT token for authenticated requests"""
        self.token = token

    def get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {"Content-Type": "application/json"}
        if include_auth and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        include_auth: bool = True
    ) -> Dict[str, Any]:
        """Make HTTP request to the API"""
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers(include_auth)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

        try:
            return {
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "success": 200 <= response.status_code < 300
            }
        except json.JSONDecodeError:
            return {
                "status_code": response.status_code,
                "data": {"message": response.text},
                "success": 200 <= response.status_code < 300
            }

# Global client instance
api_client = APIClient()