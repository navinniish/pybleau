import requests
from typing import Dict, List, Optional, Union

class WorkbookManager:
    API_VERSION = "3.8"  # Class constant for API version

    def __init__(self, client):
        """Initialize WorkbookManager with a TableauClient instance."""
        if not client.is_authenticated:
            raise ValueError("Client must be authenticated")
        self.client = client
        self.site_id = client.site_uuid
        self.server_url = client.server_url

    def _transform_tags(self, tags_data: Optional[Dict]) -> List[str]:
        """Transform tags data from API response format to list of strings."""
        if not tags_data or "tag" not in tags_data:
            return []
        return [tag["label"] for tag in tags_data["tag"]]

    def _transform_views(self, views_data: Optional[Dict]) -> List[Dict]:
        """Transform views data from API response format to list of views."""
        if not views_data or "view" not in views_data:
            return []
        return views_data["view"]

    def _transform_workbook(self, workbook: Dict) -> Dict:
        """Transform a workbook object to match expected format."""
        if "tags" in workbook:
            workbook["tags"] = self._transform_tags(workbook["tags"])
        if "views" in workbook:
            workbook["views"] = self._transform_views(workbook["views"])
        return workbook

    def _handle_response(self, response: requests.Response) -> None:
        """Handle common response status codes and raise appropriate exceptions."""
        if response.status_code == 401:
            error_data = response.json().get("error", {})
            error_detail = error_data.get("detail", "Authentication failed")
            raise Exception(f"Authentication error: {error_detail}")
        elif response.status_code == 403:
            error_data = response.json().get("error", {})
            error_detail = error_data.get("detail", "Insufficient permissions")
            raise PermissionError(error_detail)
        response.raise_for_status()

    def list_workbooks(self, **kwargs) -> List[Dict]:
        """
        List all workbooks the authenticated user has access to.
        
        Args:
            **kwargs: Optional filters and pagination parameters
                     (e.g., pageSize, pageNumber, filter, etc.)
        
        Returns:
            List of workbook dictionaries
        
        Raises:
            requests.exceptions.RequestException: For network-related errors
            PermissionError: When access is denied
            ValueError: For invalid parameters
            Exception: For authentication errors
        """
        url = f"{self.server_url}/api/{self.API_VERSION}/sites/{self.site_id}/workbooks"
        params = kwargs

        try:
            response = requests.get(url, headers=self.client.headers, params=params)
            self._handle_response(response)
            
            data = response.json()
            
            # Handle empty response
            if "workbooks" not in data or "workbook" not in data["workbooks"]:
                return []
                
            workbooks = data["workbooks"]["workbook"]
            return [self._transform_workbook(wb) for wb in workbooks]
            
        except requests.exceptions.RequestException as e:
            # Re-raise the original exception to preserve the error type
            raise

    def get_workbook(self, workbook_id: str) -> Dict:
        """
        Get details of a specific workbook by ID.
        
        Args:
            workbook_id: The ID of the workbook to retrieve
        
        Returns:
            Dictionary containing workbook details
        
        Raises:
            ValueError: For invalid workbook ID or if workbook is not found
            requests.exceptions.RequestException: For network-related errors
            Exception: For authentication errors
        """
        if not isinstance(workbook_id, str) or not workbook_id.strip():
            raise ValueError("Invalid workbook ID")
            
        url = f"{self.server_url}/api/{self.API_VERSION}/sites/{self.site_id}/workbooks/{workbook_id.strip()}"
        
        try:
            response = requests.get(url, headers=self.client.headers)
            
            if response.status_code == 404:
                raise ValueError(f"Workbook not found: {workbook_id}")
                
            self._handle_response(response)
            workbook = response.json()["workbook"]
            return self._transform_workbook(workbook)
        except requests.exceptions.RequestException as e:
            # Re-raise the original exception to preserve the error type
            raise
