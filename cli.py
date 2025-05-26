import click

@click.group()
def main():
    """Pybleau CLI - Interact with Tableau programmatically"""
    pass

@main.command()
@click.option('--server', required=True, help='Tableau Server URL')
@click.option('--token-name', required=True)
@click.option('--token-secret', required=True)
def auth(server, token_name, token_secret):
    from pybleau.auth import TableauClient
    client = TableauClient(server, token_name, token_secret)
    token = client.authenticate()
    click.echo(f"Authenticated. Token: {token}")
