# pybleau

**pybleau** is a Python wrapper for Tableau's REST and Metadata APIs.

## Features
- Authenticate using personal access token
- List and publish workbooks
- Query Tableau metadata

## Usage

```python
from pybleau.auth import TableauClient

client = TableauClient("https://your-server", "your-token-name", "your-token-secret")
client.authenticate()
