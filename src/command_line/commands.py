import click

from src.file_config import File_config
from src.manifest.manifest import Manifest
from src.requests.request_stub import Request_Stub

@click.group()
def cli():
    pass

@cli.command()
@click.pass_context
def init(ctx):
    local_manifest = Manifest('sample_manifest.json')
    ctx.invoke(request, manifest=local_manifest, registry='http:///localhost:4040/')
    pass

@cli.command()
@click.option('-m', '--manifest', 'manifest')
@click.option('-r', '--registry', 'registry')
@click.pass_context
def request(ctx, manifest, registry):
    requester = Request_Stub()
    with click.progressbar(length=len(manifest.dependencies()), label='Loading packages...') as bar:
        for dependency in manifest.dependencies():
            # click.echo(f'Loading {dependency}')
            response = requester.make_request('http://localhost:4040/',dependency)
            ctx.invoke(config, name=response)
            bar.update(1)
    pass

@cli.command()
@click.option('-p', '--package', 'name')
def config(name):
    File_config.File_config.create_package(name)
    pass
