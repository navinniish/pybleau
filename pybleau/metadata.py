import requests

def query_metadata(token, server_url, query):
    """
    Query Tableau Metadata API using GraphQL.

    Args:
        token (str): Tableau authentication token.
        server_url (str): Tableau server URL.
        query (str): GraphQL query string.

    Returns:
        dict: JSON response from the API.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    headers = {
        'X-Tableau-Auth': token,
        'Content-Type': 'application/json'
    }
    response = requests.post(
        f"{server_url}/api/metadata/graphql",
        headers=headers,
        json={"query": query}
    )
    response.raise_for_status()  # Raises an error for bad responses
    return response.json()