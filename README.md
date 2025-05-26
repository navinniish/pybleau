# pybleau

**pybleau** is a Python wrapper for Tableau's REST and Metadata APIs.

## Features

- ✅ Authenticate using Tableau Personal Access Token
- 📊 List and manage workbooks
- 🧠 Run GraphQL queries via Metadata API
- 🔁 CLI integration

## CLI Usage

```bash
pybleau auth --server https://your-server --token-name mytoken --token-secret mysecret
pybleau list-workbooks --server https://your-server --site-id site123 --token <token>


## Usage

```python
from pybleau.auth import TableauClient

client = TableauClient("https://your-server", "your-token-name", "your-token-secret")
client.authenticate()
