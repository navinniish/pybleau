import click

@click.group()
def main():
    """Pybleau CLI - Interact with Tableau programmatically"""
    pass

@main.command()
@click.option('--token', required=True)
@click.option('--site-id', required=True)
@click.option('--server', required=True)
def list_workbooks(token, site_id, server):
    from pybleau.workbooks import WorkbookManager
    manager = WorkbookManager(token, site_id, server)
    workbooks = manager.list_workbooks()
    for wb in workbooks:
        click.echo(f"{wb['id']} - {wb['name']}")
