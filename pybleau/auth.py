"""
Authentication module for Tableau Server/Cloud REST API.
"""

import requests
import json
from typing import Optional, Dict, Any


class TableauClient:
    """Client for authenticating with Tableau Server/Cloud using Personal Access Tokens."""
    
    def __init__(self, server_url: str, token_name: str, token_secret: str, site_id: str = ""):
        """
        Initialize the Tableau client.
        
        Args:
            server_url: The base URL of your Tableau Server (e.g., 'https://your-server.com')
            token_name: Your Personal Access Token name
            token_secret: Your Personal Access Token secret
            site_id: Site ID (use empty string for default site)
        """
        self.server_url = server_url.rstrip('/')
        self.token_name = token_name
        self.token_secret = token_secret
        self.site_id = site_id
        self.auth_token: Optional[str] = None
        self.site_uuid: Optional[str] = None
        self.api_version = "3.8"
        
        # Validate inputs
        if not server_url or not server_url.startswith(('http://', 'https://')):
            raise ValueError("Server URL must be a valid HTTP/HTTPS URL")
        if not token_name:
            raise ValueError("Token name cannot be empty")
        if not token_secret:
            raise ValueError("Token secret cannot be empty")
    
    @property
    def is_authenticated(self) -> bool:
        """Check if the client is currently authenticated."""
        return self.auth_token is not None
    
    @property
    def headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests."""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["X-Tableau-Auth"] = self.auth_token
        return headers
    
    def authenticate(self) -> bool:
        """
        Authenticate with Tableau Server using Personal Access Token.
        
        Returns:
            True if authentication successful, False otherwise
            
        Raises:
            requests.exceptions.RequestException: For network-related errors
        """
        url = f"{self.server_url}/api/{self.api_version}/auth/signin"
        
        # Prepare the authentication payload
        payload = {
            "credentials": {
                "personalAccessTokenCredentials": {
                    "tokenName": self.token_name,
                    "tokenValue": self.token_secret,
                    "site": {
                        "contentUrl": self.site_id
                    }
                }
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                data = response.json()
                credentials = data.get("credentials", {})
                self.auth_token = credentials.get("token")
                site_info = credentials.get("site", {})
                self.site_uuid = site_info.get("id")
                return True
            else:
                print(f"Authentication failed: {response.status_code}")
                if response.status_code == 401:
                    try:
                        error_data = response.json()
                        print(f"Error: {error_data}")
                    except:
                        pass
                return False
                
        except requests.exceptions.RequestException:
            # Re-raise network exceptions for proper error handling
            raise
        except Exception as e:
            print(f"Unexpected error during authentication: {e}")
            return False
    
    def signout(self) -> bool:
        """
        Sign out from Tableau Server.
        
        Returns:
            True if signout successful or not authenticated, False otherwise
        """
        if not self.is_authenticated:
            return True
        
        url = f"{self.server_url}/api/{self.api_version}/auth/signout"
        
        try:
            response = requests.post(url, headers=self.headers)
            
            # Clear authentication state regardless of response
            self.auth_token = None
            self.site_uuid = None
            
            return response.status_code == 204
            
        except requests.exceptions.RequestException:
            # Clear state even if signout request fails
            self.auth_token = None
            self.site_uuid = None
            return False
    
    def __str__(self) -> str:
        """String representation that doesn't expose secrets."""
        auth_status = "authenticated" if self.is_authenticated else "not authenticated"
        return f"TableauClient(server={self.server_url}, site={self.site_id}, {auth_status})"
    
    def __repr__(self) -> str:
        """Detailed representation for debugging."""
        return (f"TableauClient(server_url='{self.server_url}', "
                f"token_name='{self.token_name}', "
                f"site_id='{self.site_id}', "
                f"authenticated={self.is_authenticated})")
