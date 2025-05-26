import requests

class TableauClient:
    def __init__(self, server_url, personal_access_token_name, personal_access_token_secret):
        self.server_url = server_url
        self.token_name = personal_access_token_name
        self.token_secret = personal_access_token_secret
        self.token = None

    def authenticate(self):
        url = f"{self.server_url}/api/3.19/auth/signin"
        payload = {
            "credentials": {
                "personalAccessTokenName": self.token_name,
                "personalAccessTokenSecret": self.token_secret,
                "site": {"contentUrl": ""}
            }
        }
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        self.token = resp.json()["credentials"]["token"]
        return self.token
