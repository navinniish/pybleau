import pytest
import requests
from unittest.mock import Mock, patch
from pybleau.auth import TableauClient


class TestTableauClient:
    """Comprehensive tests for TableauClient authentication."""
    
    def setup_method(self):
        """Setup test fixtures before each test method."""
        self.server_url = "https://tableau.example.com"
        self.token_name = "test_token"
        self.token_secret = "test_secret_123"
        self.site_id = "test_site"
        
        self.client = TableauClient(
            server_url=self.server_url,
            token_name=self.token_name,
            token_secret=self.token_secret,
            site_id=self.site_id
        )

    def test_client_initialization_valid_params(self):
        """Test client initializes correctly with valid parameters."""
        assert self.client.server_url == self.server_url
        assert self.client.token_name == self.token_name
        assert self.client.token_secret == self.token_secret
        assert self.client.site_id == self.site_id
        assert self.client.auth_token is None
        assert self.client.site_uuid is None

    def test_client_initialization_invalid_server_url(self):
        """Test client raises error with invalid server URL."""
        invalid_urls = [
            "not-a-url",
            "ftp://invalid.com",
            "",
            None,
            "http://",
            "https://",
        ]
        
        for invalid_url in invalid_urls:
            with pytest.raises(ValueError):
                TableauClient(invalid_url, "token", "secret")

    def test_client_initialization_empty_credentials(self):
        """Test client raises error with empty credentials."""
        with pytest.raises(ValueError, match="Token name cannot be empty"):
            TableauClient(self.server_url, "", "secret")
            
        with pytest.raises(ValueError, match="Token secret cannot be empty"):
            TableauClient(self.server_url, "token", "")

    @patch('requests.post')
    def test_authenticate_success(self, mock_post):
        """Test successful authentication."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "credentials": {
                "token": "auth_token_123",
                "site": {
                    "id": "site_uuid_456"
                }
            }
        }
        mock_post.return_value = mock_response
        
        result = self.client.authenticate()
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        assert call_args[0][0] == f"{self.server_url}/api/3.8/auth/signin"
        assert "personalAccessTokenCredentials" in str(call_args[1]['json'])
        
        # Verify client state is updated
        assert self.client.auth_token == "auth_token_123"
        assert self.client.site_uuid == "site_uuid_456"
        assert result is True

    @patch('requests.post')
    def test_authenticate_network_error(self, mock_post):
        """Test authentication fails gracefully on network error."""
        mock_post.side_effect = requests.exceptions.ConnectionError("Network error")
        
        with pytest.raises(requests.exceptions.ConnectionError):
            self.client.authenticate()
        
        # Ensure client state remains clean
        assert self.client.auth_token is None
        assert self.client.site_uuid is None

    @patch('requests.post')
    def test_authenticate_invalid_credentials(self, mock_post):
        """Test authentication with invalid credentials."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {
                "code": "401000",
                "summary": "Signin Error",
                "detail": "Invalid credentials"
            }
        }
        mock_post.return_value = mock_response
        
        result = self.client.authenticate()
        
        assert result is False
        assert self.client.auth_token is None

    def test_headers_property_without_auth(self):
        """Test headers property when not authenticated."""
        headers = self.client.headers
        assert "X-Tableau-Auth" not in headers
        assert headers["Content-Type"] == "application/json"

    def test_headers_property_with_auth(self):
        """Test headers property when authenticated."""
        self.client.auth_token = "test_token"
        headers = self.client.headers
        
        assert headers["X-Tableau-Auth"] == "test_token"
        assert headers["Content-Type"] == "application/json"

    def test_is_authenticated_property(self):
        """Test is_authenticated property."""
        assert not self.client.is_authenticated
        
        self.client.auth_token = "test_token"
        assert self.client.is_authenticated
        
        self.client.auth_token = None
        assert not self.client.is_authenticated

    @patch('requests.post')
    def test_signout_success(self, mock_post):
        """Test successful signout."""
        # Setup authenticated client
        self.client.auth_token = "test_token"
        self.client.site_uuid = "test_site"
        
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        result = self.client.signout()
        
        # Verify signout request
        expected_url = f"{self.server_url}/api/3.8/auth/signout"
        mock_post.assert_called_once_with(
            expected_url,
            headers={"X-Tableau-Auth": "test_token", "Content-Type": "application/json"}
        )
        
        # Verify client state is cleared
        assert self.client.auth_token is None
        assert self.client.site_uuid is None
        assert result is True

    def test_signout_when_not_authenticated(self):
        """Test signout when not authenticated."""
        result = self.client.signout()
        assert result is True  # Should succeed silently

    def test_string_representation(self):
        """Test string representation doesn't expose secrets."""
        client_str = str(self.client)
        assert self.token_secret not in client_str
        assert self.server_url in client_str
        assert "not authenticated" in client_str
        
        # Test when authenticated
        self.client.auth_token = "test_token"
        client_str = str(self.client)
        assert "authenticated" in client_str
