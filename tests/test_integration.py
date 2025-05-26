import pytest
from unittest.mock import Mock, patch
import requests
from pybleau.auth import TableauClient
from pybleau.workbooks import WorkbookManager
from pybleau.metadata import MetadataAPI


class TestIntegration:
    """Integration tests that test multiple components working together."""
    
    @patch('requests.post')
    @patch('requests.get')
    def test_full_workflow_authentication_to_workbook_listing(self, mock_get, mock_post):
        """Test complete workflow from authentication to workbook listing."""
        # Setup authentication mock
        auth_response = Mock()
        auth_response.status_code = 200
        auth_response.json.return_value = {
            "credentials": {
                "token": "auth_token_123",
                "site": {"id": "site_uuid_456"}
            }
        }
        mock_post.return_value = auth_response
        
        # Setup workbook listing mock
        workbook_response = Mock()
        workbook_response.status_code = 200
        workbook_response.json.return_value = {
            "workbooks": {
                "workbook": [
                    {"id": "wb1", "name": "Dashboard 1"},
                    {"id": "wb2", "name": "Dashboard 2"}
                ]
            }
        }
        mock_get.return_value = workbook_response
        
        # Execute workflow
        client = TableauClient("https://tableau.example.com", "token", "secret")
        assert client.authenticate()
        
        workbook_manager = WorkbookManager(client)
        workbooks = workbook_manager.list_workbooks()
        
        # Verify results
        assert len(workbooks) == 2
        assert workbooks[0]["name"] == "Dashboard 1"
        
        # Verify authentication was called
        mock_post.assert_called_once()
        
        # Verify workbook API was called with correct auth headers
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "X-Tableau-Auth" in call_args[1]["headers"]
        assert call_args[1]["headers"]["X-Tableau-Auth"] == "auth_token_123"

    @patch('requests.post')
    def test_authentication_failure_prevents_api_calls(self, mock_post):
        """Test that failed authentication prevents subsequent API calls."""
        # Setup failed authentication
        auth_response = Mock()
        auth_response.status_code = 401
        mock_post.return_value = auth_response
        
        client = TableauClient("https://tableau.example.com", "bad_token", "bad_secret")
        assert not client.authenticate()
        
        # Verify that WorkbookManager refuses to work with unauthenticated client
        with pytest.raises(ValueError, match="Client must be authenticated"):
            WorkbookManager(client)
        
        with pytest.raises(ValueError, match="Client must be authenticated"):
            MetadataAPI(client)

    @patch('requests.post')
    def test_token_expiration_simulation(self, mock_post):
        """Test handling of expired authentication tokens."""
        # First call succeeds (authentication)
        auth_response = Mock()
        auth_response.status_code = 200
        auth_response.json.return_value = {
            "credentials": {
                "token": "auth_token_123",
                "site": {"id": "site_uuid_456"}
            }
        }
        
        # Second call fails (token expired)
        expired_response = Mock()
        expired_response.status_code = 401
        expired_response.json.return_value = {
            "error": {
                "code": "401002",
                "summary": "Unauthorized",
                "detail": "Authentication token expired"
            }
        }
        
        mock_post.side_effect = [auth_response, expired_response]
        
        client = TableauClient("https://tableau.example.com", "token", "secret")
        assert client.authenticate()
        
        # Simulate API call that returns 401 (token expired)
        with patch('requests.get', return_value=expired_response):
            workbook_manager = WorkbookManager(client)
            with pytest.raises(Exception):  # Should handle token expiration
                workbook_manager.list_workbooks()

    def test_client_state_consistency(self):
        """Test that client state remains consistent across operations."""
        client = TableauClient("https://tableau.example.com", "token", "secret")
        
        # Initial state
        assert client.auth_token is None
        assert client.site_uuid is None
        assert not client.is_authenticated
        
        # Simulate successful authentication
        client.auth_token = "test_token"
        client.site_uuid = "test_site"
        
        assert client.is_authenticated
        assert "X-Tableau-Auth" in client.headers
        
        # Simulate signout
        client.auth_token = None
        client.site_uuid = None
        
        assert not client.is_authenticated
        assert "X-Tableau-Auth" not in client.headers

    @patch('requests.post')
    @patch('requests.get')
    def test_error_propagation_through_layers(self, mock_get, mock_post):
        """Test that errors propagate correctly through all layers."""
        # Setup successful authentication
        auth_response = Mock()
        auth_response.status_code = 200
        auth_response.json.return_value = {
            "credentials": {
                "token": "auth_token_123",
                "site": {"id": "site_uuid_456"}
            }
        }
        mock_post.return_value = auth_response
        
        # Setup network error for workbook API
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        
        client = TableauClient("https://tableau.example.com", "token", "secret")
        client.authenticate()
        
        workbook_manager = WorkbookManager(client)
        
        # Verify that network errors bubble up correctly
        with pytest.raises(requests.exceptions.ConnectionError):
            workbook_manager.list_workbooks()

    def test_thread_safety_simulation(self):
        """Test that the client can handle concurrent usage safely."""
        import threading
        import time
        
        client = TableauClient("https://tableau.example.com", "token", "secret")
        client.auth_token = "test_token"  # Simulate authenticated state
        client.site_uuid = "test_site"
        
        results = []
        errors = []
        
        def access_headers():
            try:
                for _ in range(100):
                    headers = client.headers
                    assert "X-Tableau-Auth" in headers
                    time.sleep(0.001)  # Simulate processing time
                results.append("success")
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads accessing client properties
        threads = [threading.Thread(target=access_headers) for _ in range(5)]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verify no race conditions occurred
        assert len(results) == 5
        assert len(errors) == 0
