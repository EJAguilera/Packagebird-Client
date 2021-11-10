import click

from src.file_config import File_config
from src.manifest.manifest import Manifest

@click.group()
def cli():
    pass

@cli.command()
@click.pass_context
def init(ctx):
    manifest = Manifest('sample_manifest.json')
    for dependency in manifest.dependencies():
        click.echo(f'Loading {dependency} package...')
        ctx.invoke(config, name=dependency)
    pass

@cli.command()
@click.option('-p', '--package', 'name')
def config(name):
    File_config.File_config.create_package(name)
    pass
