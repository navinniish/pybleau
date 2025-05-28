import nbformat as nbf

# Create a new notebook
nb = nbf.v4.new_notebook()

# Title and introduction
nb.cells.append(nbf.v4.new_markdown_cell("""# PyBleau Tableau Integration Demo

This notebook demonstrates how to interact with Tableau Server/Cloud using PyBleau's integration features. You'll learn how to:
1. Authenticate with Tableau Server
2. List available workbooks
3. Get detailed workbook information
4. Manage workbook sessions"""))

# Authentication Setup
nb.cells.append(nbf.v4.new_markdown_cell("""## 1. Authentication Setup

First, we need to set up authentication using Personal Access Tokens. You'll need:
- Tableau Server URL
- Personal Access Token name
- Personal Access Token secret
- Site ID (optional, use empty string for default site)"""))

nb.cells.append(nbf.v4.new_code_cell("""from pybleau.auth import TableauClient
from pybleau.workbooks import WorkbookManager

# Replace these with your actual Tableau Server details
SERVER_URL = "https://your-tableau-server.com"
TOKEN_NAME = "your_token_name"
TOKEN_SECRET = "your_token_secret"
SITE_ID = ""  # Leave empty for default site

# Create and authenticate the client
client = TableauClient(
    server_url=SERVER_URL,
    token_name=TOKEN_NAME,
    token_secret=TOKEN_SECRET,
    site_id=SITE_ID
)

# Authenticate
if client.authenticate():
    print("Successfully authenticated with Tableau Server!")
else:
    print("Authentication failed. Please check your credentials.")"""))

# List Workbooks
nb.cells.append(nbf.v4.new_markdown_cell("""## 2. List Available Workbooks

Once authenticated, we can list all workbooks the user has access to:"""))

nb.cells.append(nbf.v4.new_code_cell("""# Create a WorkbookManager instance
workbook_mgr = WorkbookManager(client)

# List all workbooks
try:
    workbooks = workbook_mgr.list_workbooks()
    print(f"Found {len(workbooks)} workbooks:")
    for wb in workbooks:
        print(f"- {wb.get('name', 'Unnamed')} (ID: {wb.get('id', 'Unknown')})")
except Exception as e:
    print(f"Error listing workbooks: {e}")"""))

# Get Workbook Details
nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Get Detailed Workbook Information

We can get detailed information about a specific workbook using its ID:"""))

nb.cells.append(nbf.v4.new_code_cell("""# Replace with an actual workbook ID from the list above
WORKBOOK_ID = "your_workbook_id"

try:
    workbook = workbook_mgr.get_workbook(WORKBOOK_ID)
    print("Workbook Details:")
    print(f"Name: {workbook.get('name', 'Unnamed')}")
    print(f"Owner: {workbook.get('owner', {}).get('name', 'Unknown')}")
    print(f"Project: {workbook.get('project', {}).get('name', 'Unknown')}")
    print(f"Tags: {', '.join(workbook.get('tags', []))}")
    
    # List views in the workbook
    print("\\nViews:")
    for view in workbook.get('views', []):
        print(f"- {view.get('name', 'Unnamed View')}")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")"""))

# Clean Up
nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Clean Up

Always sign out when you're done to clean up the session:"""))

nb.cells.append(nbf.v4.new_code_cell("""if client.signout():
    print("Successfully signed out!")
else:
    print("Error during sign out.")"""))

# Additional Features
nb.cells.append(nbf.v4.new_markdown_cell("""## Additional Features

PyBleau's Tableau integration supports:
1. Authentication using Personal Access Tokens
2. Listing and filtering workbooks
3. Retrieving detailed workbook information
4. Secure session management
5. Error handling for common scenarios

The integration uses Tableau's REST API version 3.8 and handles:
- Authentication errors
- Permission issues
- Network-related errors
- Data transformation from API responses"""))

# Add metadata
nb.metadata = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "codemirror_mode": {
            "name": "ipython",
            "version": 3
        },
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.8"
    }
}

# Write the notebook to a file
with open('examples/tableau_integration_demo.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f) 