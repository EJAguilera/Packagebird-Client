import os
import sys

class file_config:
    def __init__(self) -> None:
        pass

    def create_dir(file_name: str) -> bool:
        os.mkdir(file_name)
        return True