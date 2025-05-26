import requests

def query_metadata(token, server_url, query):
    headers = {
        'X-Tableau-Auth': token,
        'Content-Type': 'application/json'
    }
    response = requests.post(
        f"{server_url}/api/metadata/graphql",
        headers=headers,
        json={"query": query}
    )
    return response.json()
