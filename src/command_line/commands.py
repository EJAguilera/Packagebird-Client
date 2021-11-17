import click
import os
import sys
from src.file_config import File_config
from src.manifest.manifest import Manifest
from src.requests.request_stub import Request_Stub

@click.group()
def cli():
    pass

@cli.command()
@click.option('-m', '--manifest', 'manifest')
@click.pass_context
def init(ctx, manifest):
    if manifest == None:
        if not os.path.exists('manifest.json'):
            click.echo("'manifest.json' file is not found! Please navigate to directory containing the manifest file.")
            return
        local_manifest = Manifest('manifest.json')
    else:
        if not os.path.exists(manifest):
            click.echo("Specified manifest file is not found! Check spelling or navigate to directory.")
            return
        local_manifest = Manifest(manifest)
    ctx.invoke(request, manifest=local_manifest, registry='http:///localhost:4040/')
    pass

@cli.command()
# @click.option('-m', '--manifest', 'manifest')
# @click.option('-r', '--registry', 'registry')
@click.option('-p', '--project', 'project')
@click.pass_context
def request(ctx, project):
    requester = Request_Stub()
    # with click.progressbar(length=len(manifest.dependencies()), label='Loading packages...') as bar:
    #    for dependency in manifest.dependencies():
    response = requester.make_request('http://localhost:4040/',project)
    with click.progressbar(length=len(response), label='Loading packages...') as bar:
        for package in response:
            ctx.invoke(config, name=package)
            bar.update(1)
    pass

@cli.command()
@click.option('-p', '--package', 'name')
def config(name):
    File_config.File_config.create_package(name)
    pass
