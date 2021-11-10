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
        
        os.mkdir(f'packages/{name}')
        os.mkdir(f'packages/{name}/src')

        filename = f'{name}.pkg'
        manifest = 'manifest.json'
        src_file = 'src.java'

        with open(os.path.join(f'packages/{name}', filename), 'w') as package:
            package.write(f'Fill in later...')
        
        with open(os.path.join(f'packages/{name}', manifest), 'w') as manifest:
            manifest.write('{"name":"'+name+'"}')
        
        with open(os.path.join(f'packages/{name}/src', src_file), 'w') as file:
            file.write("class src_file { public static void main(String args) { /* Stub */ } }")

        

if __name__=='__main__':
    File_config.create_package('Sample')
    File_config.create_package('Meta')
