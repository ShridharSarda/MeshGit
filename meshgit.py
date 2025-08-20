import click
from repo import Repo

@click.group()
def cli():
    """MeshGit CLI"""
    pass

@cli.command()
def init():
    """Initialize a new repository"""
    Repo.init_repo()

@cli.command()
@click.argument("filename")
def add(filename):
    """Add file to staging area"""
    Repo.add_file(filename)

@cli.command()
@click.option("-m", "--message", required=True, help="Commit message")
def commit(message):
    """Commit staged changes"""
    Repo.commit(message)

@cli.command()
def log():
    """Show commit history"""
    Repo.show_log()

if __name__ == "__main__":
    cli()
