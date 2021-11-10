import json
from pathlib import Path

class Manifest:

    """Takes a passed file from the system and map properties to class variables."""
    def __init__(self, file) -> None:
        self.manifest = self.file_parse(file)
        self.registry = self.manifest['registry']
    
    """Parses JSON-formatted file into dictionary."""
    def file_parse(self, file: str) -> object:
        return json.loads(Path(file).read_text())

    """Returns list of dependencies"""
    def dependencies(self) -> object:
        dependencies = []
        for entry in self.manifest['dependencies']:
            dependencies.append(f"{entry['name']}-v{entry['version']}")
        return dependencies
