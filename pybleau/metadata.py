import requests

class MetadataAPI:
    """API client for Tableau Metadata API."""

    def __init__(self, client):
        """Initialize MetadataAPI with a TableauClient instance."""
        if not client.is_authenticated:
            raise ValueError("Client must be authenticated")
        self.client = client

    def query(self, query, variables=None):
        """
        Execute a GraphQL query against the Metadata API.

        Args:
            query (str): GraphQL query string
            variables (dict, optional): Variables for the GraphQL query

        Returns:
            dict: JSON response from the API

        Raises:
            ValueError: If query is empty or contains syntax errors
            Exception: For rate limiting or server errors
        """
        if not query:
            raise ValueError("Query cannot be empty")

        headers = self.client.headers
        url = f"{self.client.server_url}/api/metadata/graphql"
        
        json_data = {"query": query}
        if variables:
            json_data["variables"] = variables

        response = requests.post(url, headers=headers, json=json_data)

        if response.status_code == 429:
            raise Exception(f"Rate limited. Retry after {response.headers.get('Retry-After', 'unknown')} seconds")
        elif response.status_code >= 500:
            raise Exception(f"Server error: {response.text}")
        elif response.status_code == 400:
            error_data = response.json()
            if "errors" in error_data:
                raise ValueError("GraphQL syntax error: " + str(error_data["errors"]))
            raise ValueError(f"Bad request: {response.text}")
        
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            raise ValueError("GraphQL execution error: " + str(data["errors"]))
            
        return data