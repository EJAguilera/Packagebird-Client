import os
import sys
import click

class File_config:
    def __init__(self) -> None:
        pass

    def create_dir(file_name: str) -> bool:
        os.mkdir(file_name)
        return True
    
    def create_package_dir() -> bool:
        if os.path.isdir('packages'):
            return False
        else:
            os.mkdir('packages')
            return True
    
    def create_package(name: str) -> bool:
        if File_config.create_package_dir():
            click.echo("Creating packages directory...")
        
        os.mkdir(f'packages/{name}_pkg')

        filename = f'{name}.pkg'
        manifest = 'manifest.json'

        with open(os.path.join(f'packages/{name}_pkg', filename), 'w') as package:
            package.write(f'Fill in later...')
        
        with open(os.path.join(f'packages/{name}_pkg', manifest), 'w') as manifest:
            manifest.write('{"name":"'+name+'"}')

if __name__=='__main__':
    File_config.create_package('Sample')
    File_config.create_package('Meta')
