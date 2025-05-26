import pytest
from unittest.mock import Mock, patch
from pybleau.workbooks import WorkbookManager
from pybleau.auth import TableauClient


class TestWorkbookManager:
    """Comprehensive tests for WorkbookManager."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.mock_client = Mock(spec=TableauClient)
        self.mock_client.server_url = "https://tableau.example.com"
        self.mock_client.auth_token = "test_auth_token"
        self.mock_client.site_uuid = "test_site_uuid"
        self.mock_client.is_authenticated = True
        self.mock_client.headers = {
            "X-Tableau-Auth": "test_auth_token",
            "Content-Type": "application/json"
        }
        
        self.workbook_manager = WorkbookManager(self.mock_client)

    def test_initialization_with_authenticated_client(self):
        """Test WorkbookManager initializes with authenticated client."""
        assert self.workbook_manager.client == self.mock_client

    def test_initialization_with_unauthenticated_client(self):
        """Test WorkbookManager raises error with unauthenticated client."""
        unauthenticated_client = Mock()
        unauthenticated_client.is_authenticated = False
        
        with pytest.raises(ValueError, match="Client must be authenticated"):
            WorkbookManager(unauthenticated_client)

    @patch('requests.get')
    def test_list_workbooks_success(self, mock_get):
        """Test successful workbook listing."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "workbooks": {
                "workbook": [
                    {
                        "id": "workbook1",
                        "name": "Sales Dashboard",
                        "contentUrl": "sales-dashboard",
                        "createdAt": "2023-01-01T00:00:00Z",
                        "updatedAt": "2023-01-02T00:00:00Z",
                        "project": {"id": "project1", "name": "Default"},
                        "owner": {"id": "user1", "name": "John Doe"},
                        "tags": {"tag": [{"label": "sales"}, {"label": "dashboard"}]}
                    },
                    {
                        "id": "workbook2",
                        "name": "Finance Report",
                        "contentUrl": "finance-report",
                        "createdAt": "2023-01-03T00:00:00Z",
                        "updatedAt": "2023-01-04T00:00:00Z",
                        "project": {"id": "project2", "name": "Finance"},
                        "owner": {"id": "user2", "name": "Jane Smith"},
                        "tags": None
                    }
                ]
            },
            "pagination": {
                "pageNumber": "1",
                "pageSize": "100",
                "totalAvailable": "2"
            }
        }
        mock_get.return_value = mock_response
        
        workbooks = self.workbook_manager.list_workbooks()
        
        # Verify request
        expected_url = f"{self.mock_client.server_url}/api/3.8/sites/{self.mock_client.site_uuid}/workbooks"
        mock_get.assert_called_once_with(expected_url, headers=self.mock_client.headers, params={})
        
        # Verify response parsing
        assert len(workbooks) == 2
        assert workbooks[0]["name"] == "Sales Dashboard"
        assert workbooks[1]["name"] == "Finance Report"
        assert workbooks[0]["tags"] == ["sales", "dashboard"]
        assert workbooks[1]["tags"] == []

    @patch('requests.get')
    def test_list_workbooks_with_filters(self, mock_get):
        """Test workbook listing with filters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"workbooks": {"workbook": []}}
        mock_get.return_value = mock_response
        
        filters = {
            "filter": "name:eq:Dashboard",
            "sort": "name:asc",
            "pageSize": "50",
            "pageNumber": "2"
        }
        
        self.workbook_manager.list_workbooks(**filters)
        
        # Verify filters are passed as query parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]["params"] == filters

    @patch('requests.get')
    def test_list_workbooks_empty_response(self, mock_get):
        """Test workbook listing with empty response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"workbooks": {}}
        mock_get.return_value = mock_response
        
        workbooks = self.workbook_manager.list_workbooks()
        
        assert workbooks == []

    @patch('requests.get')
    def test_list_workbooks_network_error(self, mock_get):
        """Test workbook listing handles network errors."""
        mock_get.side_effect = ConnectionError("Network unreachable")
        
        with pytest.raises(ConnectionError):
            self.workbook_manager.list_workbooks()

    @patch('requests.get')
    def test_list_workbooks_permission_denied(self, mock_get):
        """Test workbook listing handles permission errors."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "error": {
                "code": "403000",
                "summary": "Forbidden",
                "detail": "Insufficient permissions"
            }
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(PermissionError, match="Insufficient permissions"):
            self.workbook_manager.list_workbooks()

    @patch('requests.get')
    def test_get_workbook_success(self, mock_get):
        """Test successful individual workbook retrieval."""
        workbook_id = "workbook123"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "workbook": {
                "id": workbook_id,
                "name": "Test Workbook",
                "description": "A test workbook",
                "contentUrl": "test-workbook",
                "showTabs": True,
                "size": "1024000",
                "views": {
                    "view": [
                        {"id": "view1", "name": "Sheet 1"},
                        {"id": "view2", "name": "Sheet 2"}
                    ]
                }
            }
        }
        mock_get.return_value = mock_response
        
        workbook = self.workbook_manager.get_workbook(workbook_id)
        
        # Verify request
        expected_url = f"{self.mock_client.server_url}/api/3.8/sites/{self.mock_client.site_uuid}/workbooks/{workbook_id}"
        mock_get.assert_called_once_with(expected_url, headers=self.mock_client.headers)
        
        # Verify response
        assert workbook["id"] == workbook_id
        assert workbook["name"] == "Test Workbook"
        assert len(workbook["views"]) == 2

    @patch('requests.get')
    def test_get_workbook_not_found(self, mock_get):
        """Test workbook retrieval when workbook doesn't exist."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "error": {
                "code": "404000",
                "summary": "Not Found",
                "detail": "Workbook not found"
            }
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Workbook not found"):
            self.workbook_manager.get_workbook("nonexistent")

    def test_get_workbook_invalid_id(self):
        """Test workbook retrieval with invalid ID."""
        invalid_ids = [None, "", "   ", 123, []]
        
        for invalid_id in invalid_ids:
            with pytest.raises((ValueError, TypeError)):
                self.workbook_manager.get_workbook(invalid_id)

    @patch('requests.get')
    def test_list_workbooks_pagination_stress_test(self, mock_get):
        """Stress test pagination handling."""
        # Simulate large dataset with multiple pages
        def mock_response_side_effect(url, **kwargs):
            page_num = int(kwargs.get('params', {}).get('pageNumber', 1))
            
            if page_num <= 3:
                return Mock(
                    status_code=200,
                    json=lambda: {
                        "workbooks": {
                            "workbook": [
                                {"id": f"wb_{page_num}_{i}", "name": f"Workbook {page_num}-{i}"}
                                for i in range(100)
                            ]
                        },
                        "pagination": {
                            "pageNumber": str(page_num),
                            "pageSize": "100",
                            "totalAvailable": "300"
                        }
                    }
                )
            else:
                return Mock(status_code=404)
        
        mock_get.side_effect = mock_response_side_effect
        
        # Test getting specific page
        workbooks = self.workbook_manager.list_workbooks(pageNumber="2")
        assert len(workbooks) == 100
        assert workbooks[0]["id"] == "wb_2_0"

    @patch('requests.get')
    def test_concurrent_requests_simulation(self, mock_get):
        """Simulate handling concurrent requests."""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"workbooks": {"workbook": []}}
                mock_get.return_value = mock_response
                
                # Simulate network delay
                time.sleep(0.1)
                result = self.workbook_manager.list_workbooks()
                results.append(result)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = [threading.Thread(target=make_request) for _ in range(5)]
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Verify all requests succeeded
        assert len(results) == 5
        assert len(errors) == 0
