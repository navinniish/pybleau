pybleau is a lightweight Python wrapper for Tableau's REST and Metadata APIs, designed to simplify automation and integration tasks with Tableau.

🚀 Features
✅ Authenticate using Tableau Personal Access Tokens (PAT)

📊 List and manage Tableau workbooks

🧠 Run GraphQL queries using the Metadata API

🔁 Easy-to-use CLI integration

🔧 CLI Usage
bash
Copy
Edit
# Authenticate using Personal Access Token
pybleau auth --server https://your-server --token-name mytoken --token-secret mysecret

# List workbooks on a Tableau site
pybleau list-workbooks --server https://your-server --site-id site123 --token <token>
🐍 Python Usage
python
Copy
Edit
from pybleau.auth import TableauClient

client = TableauClient("https://your-server", "your-token-name", "your-token-secret")
client.authenticate()
📌 Coming Soon
Publish workbook support

Extract and download data sources

Schedule refresh tasks

More CLI utilities and error handling

📫 Contributions
Contributions, bug reports, and feature suggestions are welcome! Please open an issue or submit a pull request.
