import click

from src.file_config import File_config

@click.group()
def cli():
    pass

@cli.command()
@click.option('-p', '--package', 'name')
def config(name):
    File_config.File_config.create_package(name)
    pass
