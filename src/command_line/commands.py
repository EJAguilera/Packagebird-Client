import click
import os
import sys
import tarfile
from src.file_config import File_config
from src.manifest.manifest import Manifest
from src.requests.request_stub import Request_Stub
from src.fileserver.fileserver_client import FileTransfer
from src.command_line.utils import Utils
from src.package_operations.package_operations import PackageOperations 

@click.group()
def cli():
    # The entry point for the command line interface
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
@click.option('-p', '--project', 'project')
@click.pass_context
def request(ctx, project):
    requester = Request_Stub()
    response = requester.make_request('http://localhost:4040/',project)
    with click.progressbar(length=len(response), label='Loading packages...') as bar:
        for package in response:
            ctx.invoke(addpackage, name=package, version=1)
            bar.update(1)
    pass

# Add package to the development directory
@cli.command()
@click.option('-p', '--package', 'name')
@click.option('-v', '--version', 'version')
@click.pass_context
def addpackage(ctx, name, version):
    # Makes the packages directory
    if not os.path.isdir('packages'):
        click.echo("Creating packages directory...")
        os.mkdir('packages')
    os.chdir('packages')
    
    # Create Package Directory
    os.mkdir(f'{name}')
    os.chdir(f'{name}')

    # Download the archived package
    fileservice = FileTransfer()
    request_string = f'{name}-v{version}.tar.gz'
    fileservice.download('127.0.0.1', '50051', f'{request_string}')

    # Extract the contents
    with tarfile.open(request_string, 'r:gz') as archive:
        try:
            archive.extractall(path='.')
        except tarfile.ReadError:
            click.echo('Empty file found.')
    
    # Remove the archive file
    os.remove(request_string)

    # Move back to the development root directory
    os.chdir('..')
    os.chdir('..')

# Gets packages associated with a project
@cli.command()
@click.option('-p', '--project', 'project')
@click.pass_context
def setup(ctx, project):
    fileservice = FileTransfer()
    utils = Utils()
    packages_strings = utils.project_packages(project)
    for package_addr in packages_strings:
        package_name = package_addr[0]
        package_version = package_addr[1]
        ctx.invoke(addpackage, name=package_name, version=package_version)

def filter_contents(tarinfo):
    if tarinfo.name == 'packages':
        return None
    else:
        return tarinfo

# Create package from a development directory
@cli.command()
@click.option('--debug', is_flag=True)
@click.pass_context
def createpackage(ctx, debug):
    # Get packages and location
    project_name = os.path.basename(os.getcwd())
    version = 1
    message = f'Project Name: {project_name}, version: {version}'
    print(message)

    # Package name
    package_name = f'{project_name}-v{version}.tar.gz'

    # Add the contents
    with tarfile.open(package_name, 'w:gz', format=tarfile.GNU_FORMAT) as tar:
        for directory, directorynames, filenames in os.walk("."):
            for file in filenames:
                if (debug):
                    click.echo(f'Directory Visited: {directory}')

                if "/packages/" not in directory and "\\packages\\" not in directory and "./packages/" not in directory:
                    if (debug):
                        click.echo(f'Visited directory and file not in packages. File reached is {file}.')
                    
                    if file != package_name:
                        tar.add(os.path.join(directory, file))
                    else:
                        if (debug):
                            click.echo(f'File {file} is the temp client tar file, should not be bundled.')
                elif debug:
                    click.echo(f'File visited in packages directory! Directory is {directory}, file is {file}')
                    


    # Upload to server
    if (not debug):
        fileservice = FileTransfer()
        fileservice.upload('127.0.0.1', '50051', package_name)
    os.remove(package_name)

# List out packages on server
@cli.command()
@click.pass_context
def listpackages(ctx):
    packageoperations = PackageOperations()
    packagelist = packageoperations.list_packages('127.0.0.1','50051')
    click.echo(f'{packagelist.list}')

# Call the test method on the server
@cli.command()
@click.option('-p', '--package', 'name')
@click.option('-v', '--version', 'version')
@click.pass_context
def testpackage(ctx, name, version):
    packageoperations = PackageOperations()
    request_string = f'{name}-v{version}'
    response = packageoperations.test_package('127.0.0.1', '50051', request_string)
    click.echo(f'{response.response}')

# Call the build method on the server
@cli.command()
@click.option('-p', '--package', 'name')
@click.option('-v', '--version', 'version')
@click.pass_context
def buildpackage(ctx, name, version):
    packageoperations = PackageOperations()
    request_string = f'{name}-v{version}'
    response = packageoperations.build_package('127.0.0.1', '50051', request_string)
    click.echo(f'{response.response}')

