import requests

class WorkbookManager:
    def __init__(self, token, site_id, server_url):
        self.token = token
        self.site_id = site_id
        self.server_url = server_url

    def list_workbooks(self):
        url = f"{self.server_url}/api/3.19/sites/{self.site_id}/workbooks"
        headers = {'X-Tableau-Auth': self.token}
        response = requests.get(url, headers=headers)
        return response.json()["workbooks"]["workbook"]
