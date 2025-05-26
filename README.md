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

# PyBleau

PyBleau is a Python library for interacting with Tableau Server's REST API and creating Tableau-style visualizations.

## Features

- **Authentication**: Easy authentication with Tableau Server
- **Workbook Management**: List, download, and manage workbooks
- **Metadata API**: Query and analyze metadata using GraphQL
- **Tableau-Style Visualizations**: Create beautiful, interactive charts with a Tableau-like look and feel

## Installation

```bash
pip install pybleau
```

## Quick Start

### Authentication

```python
from pybleau.auth import TableauClient

client = TableauClient(
    server_url="https://your-tableau-server",
    username="your-username",
    password="your-password",
    site_name="your-site"
)
client.authenticate()
```

### Workbook Management

```python
from pybleau.workbooks import WorkbookManager

workbook_mgr = WorkbookManager(client)
workbooks = workbook_mgr.list_workbooks()
```

### Metadata API

```python
from pybleau.metadata import MetadataAPI

metadata = MetadataAPI(client)
result = metadata.query("""
    {
        workbooks {
            name
            owner {
                username
            }
        }
    }
""")
```

### Visualizations

Create Tableau-style visualizations using the `TableauViz` class:

```python
from pybleau.viz import TableauViz
import pandas as pd

# Create sample data
data = pd.DataFrame({
    'category': ['A', 'B', 'C'],
    'values': [10, 20, 30],
    'group': ['X', 'X', 'Y']
})

# Initialize visualization
viz = TableauViz()

# Create a bar chart
fig = viz.bar_chart(
    data=data,
    x='category',
    y='values',
    color='group',
    title='Sample Bar Chart'
)
fig.show()
```

Available chart types:
- Bar charts (vertical/horizontal, stacked/grouped)
- Line charts
- Scatter plots
- Pie charts
- Box plots

All charts feature:
- Tableau-like color palette
- Interactive tooltips
- Clean, modern design
- Customizable titles and labels
- Export to various formats (HTML, PNG, etc.)

For more examples, check out the `examples/visualization_demo.ipynb` notebook.

## Requirements

- Python 3.8+
- requests
- plotly
- pandas
- numpy

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
