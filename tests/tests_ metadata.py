import pytest
from unittest.mock import Mock, patch
from pybleau.metadata import MetadataAPI
from pybleau.auth import TableauClient


class TestMetadataAPI:
    """Comprehensive tests for Metadata API functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.mock_client = Mock(spec=TableauClient)
        self.mock_client.server_url = "https://tableau.example.com"
        self.mock_client.auth_token = "test_auth_token"
        self.mock_client.headers = {"X-Tableau-Auth": "test_auth_token"}
        self.mock_client.is_authenticated = True
        
        self.metadata_api = MetadataAPI(self.mock_client)

    @patch('requests.post')
    def test_query_success(self, mock_post):
        """Test successful GraphQL query execution."""
        query = """
        {
            workbooks {
                id
                name
                description
            }
        }
        """
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "workbooks": [
                    {"id": "1", "name": "Sales Dashboard", "description": "Sales data"},
                    {"id": "2", "name": "Finance Report", "description": "Financial metrics"}
                ]
            }
        }
        mock_post.return_value = mock_response
        
        result = self.metadata_api.query(query)
        
        # Verify GraphQL endpoint was called
        expected_url = f"{self.mock_client.server_url}/api/metadata/graphql"
        mock_post.assert_called_once_with(
            expected_url,
            headers=self.mock_client.headers,
            json={"query": query}
        )
        
        # Verify response
        assert "workbooks" in result["data"]
        assert len(result["data"]["workbooks"]) == 2

    @patch('requests.post')
    def test_query_with_variables(self, mock_post):
        """Test GraphQL query with variables."""
        query = """
        query GetWorkbook($workbookId: ID!) {
            workbook(id: $workbookId) {
                id
                name
                owner {
                    username
                }
            }
        }
        """
        variables = {"workbookId": "123"}
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "workbook": {
                    "id": "123",
                    "name": "Test Workbook",
                    "owner": {"username": "testuser"}
                }
            }
        }
        mock_post.return_value = mock_response
        
        result = self.metadata_api.query(query, variables)
        
        # Verify variables were included in request
        mock_post.assert_called_once_with(
            f"{self.mock_client.server_url}/api/metadata/graphql",
            headers=self.mock_client.headers,
            json={"query": query, "variables": variables}
        )

    @patch('requests.post')
    def test_query_syntax_error(self, mock_post):
        """Test handling of GraphQL syntax errors."""
        invalid_query = "{ invalid syntax }"
        
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "errors": [
                {
                    "message": "Syntax Error: Expected Name, found }",
                    "locations": [{"line": 1, "column": 10}]
                }
            ]
        }
        mock_post.return_value = mock_response
        
        with pytest.raises(ValueError, match="GraphQL syntax error"):
            self.metadata_api.query(invalid_query)

    @patch('requests.post')
    def test_query_field_error(self, mock_post):
        """Test handling of GraphQL field errors."""
        query = "{ nonexistentField }"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "errors": [
                {
                    "message": "Cannot query field 'nonexistentField' on type 'Query'",
                    "path": ["nonexistentField"]
                }
            ]
        }
        mock_post.return_value = mock_response
        
        with pytest.raises(ValueError, match="GraphQL execution error"):
            self.metadata_api.query(query)

    def test_query_empty_string(self):
        """Test query with empty string."""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            self.metadata_api.query("")

    def test_query_none(self):
        """Test query with None."""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            self.metadata_api.query(None)

    @patch('requests.post')
    def test_complex_nested_query(self, mock_post):
        """Test complex nested GraphQL query."""
        complex_query = """
        {
            workbooks(first: 10) {
                id
                name
                description
                createdAt
                updatedAt
                owner {
                    id
                    username
                    email
                }
                project {
                    id
                    name
                    description
                }
                sheets {
                    id
                    name
                    index
                    datasources {
                        id
                        name
                        hasExtracts
                        extractLastRefreshTime
                        tables {
                            id
                            name
                            schema
                            columns {
                                id
                                name
                                dataType
                                isNullable
                            }
                        }
                    }
                }
                tags {
                    id
                    name
                }
            }
        }
        """
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "workbooks": [
                    {
                        "id": "wb1",
                        "name": "Complex Dashboard",
                        "description": "A complex dashboard",
                        "createdAt": "2023-01-01T00:00:00Z",
                        "updatedAt": "2023-01-02T00:00:00Z",
                        "owner": {
                            "id": "user1",
                            "username": "analyst",
                            "email": "analyst@company.com"
                        },
                        "project": {
                            "id": "proj1",
                            "name": "Analytics",
                            "description": "Analytics project"
                        },
                        "sheets": [
                            {
                                "id": "sheet1",
                                "name": "Overview",
                                "index": 0,
                                "datasources": [
                                    {
                                        "id": "ds1",
                                        "name": "Sales Data",
                                        "hasExtracts": True,
                                        "extractLastRefreshTime": "2023-01-01T12:00:00Z",
                                        "tables": [
                                            {
                                                "id": "table1",
                                                "name": "sales_fact",
                                                "schema": "dbo",
                                                "columns": [
                                                    {
                                                        "id": "col1",
                                                        "name": "sales_amount",
                                                        "dataType": "REAL",
                                                        "isNullable": False
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "tags": [
                            {"id": "tag1", "name": "sales"},
                            {"id": "tag2", "name": "dashboard"}
                        ]
                    }
                ]
            }
        }
        mock_post.return_value = mock_response
        
        result = self.metadata_api.query(complex_query)
        
        # Verify deep nested data structure
        workbook = result["data"]["workbooks"][0]
        assert workbook["name"] == "Complex Dashboard"
        assert workbook["owner"]["email"] == "analyst@company.com"
        assert len(workbook["sheets"]) == 1
        assert len(workbook["tags"]) == 2
        
        sheet = workbook["sheets"][0]
        assert len(sheet["datasources"]) == 1
        
        datasource = sheet["datasources"][0]
        assert datasource["hasExtracts"] is True
        assert len(datasource["tables"]) == 1
        
        table = datasource["tables"][0]
        assert len(table["columns"]) == 1
        assert table["columns"][0]["dataType"] == "REAL"

    @patch('requests.post')
    def test_rate_limiting_handling(self, mock_post):
        """Test handling of rate limiting responses."""
        query = "{ workbooks { id name } }"
        
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "60"}
        mock_post.return_value = mock_response
        
        with pytest.raises(Exception, match="Rate limited"):
            self.metadata_api.query(query)

    @patch('requests.post')
    def test_server_error_handling(self, mock_post):
        """Test handling of server errors."""
        query = "{ workbooks { id name } }"
        
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        with pytest.raises(Exception, match="Server error"):
            self.metadata_api.query(query)

    def test_unauthenticated_client(self):
        """Test MetadataAPI with unauthenticated client."""
        unauthenticated_client = Mock()
        unauthenticated_client.is_authenticated = False
        
        with pytest.raises(ValueError, match="Client must be authenticated"):
            MetadataAPI(unauthenticated_client)
